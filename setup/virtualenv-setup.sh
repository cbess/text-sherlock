# global
# Created by: Christopher Bess
# It is recomm. not to run this script using sudo, it is used as needed.

echo "Setting up virtualenv and pip"
sudo easy_install pip
sudo pip install virtualenv

# local
# if on a Mac exec below line (maybe)
# ARCHFLAGS="-arch i386 -arch x86_64"
mkdir -p ../data/indexes
virtualenv ../sherlock_env --distribute --no-site-packages
source ../sherlock_env/bin/activate

echo "Installing sherlock dependencies"
../sherlock_env/bin/pip install -r requirements.txt

echo "Done, sherlock install finished"