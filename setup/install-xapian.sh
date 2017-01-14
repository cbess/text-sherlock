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
tar -xzf xapian.tar.xz
cd xapian-core*/
./configure --prefix=$VIRTUAL_ENV --disable-dependency-tracking --disable-assertions
make && make install

cd ..

echo "Installing xapian python bindings"
# bindings
curl -o xapian-bindings.tar.xz https://oligarchy.co.uk/xapian/$VERSION/xapian-bindings-$VERSION.tar.xz
tar -xzf xapian-bindings.tar.xz
cd xapian-bindings*/
./configure --prefix=$VIRTUAL_ENV --with-python --disable-dependency-tracking
make && make install

cd ..

# clean up
echo "Clean up xapian install files"
rm -rf xapian*

echo "Done."
