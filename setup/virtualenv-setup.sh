# global
# Created by: Christopher Bess
# It is NOT recommended to run this script using sudo, it is used as needed.
#
# user$: sh virtualenv-setup.sh

if ! [ -x "$(command -v python3)" ]; then
    echo "Python 3+ required."
    exit 1
fi

if ! [ -x "$(command -v pip)" ]; then
    echo "Setting up pip - installing with sudo"
    
    sudo easy_install pip
fi

PROJ_ROOT=$(cd $(dirname $0) && cd .. && pwd)

# adjust permission (allow it to be executed)
chmod +x ${PROJ_ROOT}/main.py

# if on a Mac exec below line (maybe)
# ARCHFLAGS="-arch i386 -arch x86_64"

VENV_ROOT=${PROJ_ROOT}/sherlock_env

# setup sherlock environment
mkdir -p ${PROJ_ROOT}/data/indexes
python3 -m venv ${VENV_ROOT}

echo "Installing sherlock dependencies"
${VENV_ROOT}/bin/pip install --upgrade pip
${VENV_ROOT}/bin/pip install -r ${PROJ_ROOT}/setup/requirements.txt

# confirm installation by showing version information
# echo "Sherlock version information"
${VENV_ROOT}/bin/python ${PROJ_ROOT}/main.py -v

echo "Sherlock install finished"