# Install xapian support
# works best with virtualenv

echo "Installing xapian"
# xapian support
curl -o xapian.tar.gz https://oligarchy.co.uk/xapian/1.2.7/xapian-core-1.2.7.tar.gz
tar -xvzf xapian.tar.gz
cd xapian*/
./configure --disable-dependency-tracking --disable-assertions
make
sudo make install

cd ..

echo "Installing xapian python bindings"
# bindings
curl -o xapian-bindings.tar.gz https://oligarchy.co.uk/xapian/1.2.7/xapian-bindings-1.2.7.tar.gz
tar -xvzf xapian-bindings.tar.gz
cd xapian-bindings*/
./configure --with-python --disable-debug --disable-dependency-tracking --without-csharp --without-tcl --without-php
make
sudo make install

cd ..

# clean up
echo "Clean up xapian install files"
rm -rf xapian*

echo "Done."
