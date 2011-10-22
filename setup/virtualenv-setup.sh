# global
# Created by: Christopher Bess
# It is recomm. not to run this script using sudo, it is used as needed.
#
# Run this script from this `setup` directory.
#
# user$: sh ./virtualenv-setup.sh

echo "Setting up virtualenv and pip"
sudo easy_install pip
sudo pip install virtualenv

# adjust permission (allow it to be executed)
chmod +x ../main.py

# if on a Mac exec below line (maybe)
# ARCHFLAGS="-arch i386 -arch x86_64"

# setup sherlock environment
mkdir -p ../data/indexes
virtualenv ../sherlock_env --distribute --no-site-packages
source ../sherlock_env/bin/activate

echo "Installing sherlock dependencies"
../sherlock_env/bin/pip install -r requirements.txt

# confirm installation by showing version information
echo "Sherlock version information"
../sherlock_env/bin/python ./main.py -v

echo "Done, sherlock install finished"