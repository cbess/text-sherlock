#!/usr/bin/env bash
set -ev

# Install xapian support
# expects a virtualenv

if [ -z "$VIRTUAL_ENV" ]
then
    echo "Must be in a virtualenv..."
    echo "Execute:"
    echo "\$ source sherlock_env/bin/activate"
    exit
fi

VERSION=1.4.2 # or 1.2.24

echo "Installing xapian core"
# xapian support
curl -o xapian.tar.xz https://oligarchy.co.uk/xapian/$VERSION/xapian-core-$VERSION.tar.xz
tar -xf xapian.tar.xz
cd xapian-core*/
./configure --prefix=$VIRTUAL_ENV --disable-dependency-tracking --disable-assertions
make && make install

cd ..

echo "Installing xapian python bindings"
PYV=`python -c "import sys;t='{v[0]}'.format(v=list(sys.version_info[:1]));sys.stdout.write(t)";`

if [ $PYV = "2" ]; then
    PYTHON_FLAG=--with-python
else
    PYTHON_FLAG=--with-python3
fi

# bindings
curl -o xapian-bindings.tar.xz https://oligarchy.co.uk/xapian/$VERSION/xapian-bindings-$VERSION.tar.xz
tar -xf xapian-bindings.tar.xz
cd xapian-bindings*/
./configure --prefix=$VIRTUAL_ENV $PYTHON_FLAG --disable-dependency-tracking
make && make install

cd ..

# clean up
echo "Clean up xapian install files"
rm -rf xapian*

# test
echo "Testing Xapian..."
python -c "import xapian"

echo "Done."
