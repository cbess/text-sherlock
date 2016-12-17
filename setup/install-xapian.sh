# Install xapian support
# works best with virtualenv

echo "Installing xapian"
# xapian support
curl -o xapian.tar.xz https://oligarchy.co.uk/xapian/1.4.2/xapian-core-1.4.2.tar.xz
tar -xvzf xapian.tar.xz
cd xapian*/
./configure --disable-dependency-tracking --disable-assertions
make
sudo make install

cd ..

echo "Installing xapian python bindings"
# bindings
curl -o xapian-bindings.tar.xz https://oligarchy.co.uk/xapian/1.4.2/xapian-bindings-1.4.2.tar.xz
tar -xvzf xapian-bindings.tar.xz
cd xapian-bindings*/
./configure --with-python --disable-debug --disable-dependency-tracking --without-csharp --without-tcl --without-php
make
sudo make install

cd ..

# clean up
echo "Clean up xapian install files"
rm -rf xapian*

echo "Done."
