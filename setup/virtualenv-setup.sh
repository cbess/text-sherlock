# global
# Created by: Christopher Bess
# It is recomm. not to run this script using sudo, it is used as needed.
#
# user$: sh virtualenv-setup.sh

echo "Setting up virtualenv and pip - installing with sudo"
sudo easy_install pip
sudo pip install virtualenv

PROJROOT=$(cd $(dirname $0) && cd .. && pwd)

# adjust permission (allow it to be executed)
chmod +x ${PROJROOT}/main.py

# if on a Mac exec below line (maybe)
# ARCHFLAGS="-arch i386 -arch x86_64"

# setup sherlock environment
mkdir -p ${PROJROOT}/data/indexes
virtualenv ${PROJROOT}/sherlock_env --distribute --no-site-packages

echo "Installing sherlock dependencies"
${PROJROOT}/sherlock_env/bin/pip install -r ${PROJROOT}/setup/requirements.txt

# confirm installation by showing version information
# echo "Sherlock version information"
${PROJROOT}/sherlock_env/bin/python ${PROJROOT}/main.py -v

echo "Sherlock install finished"