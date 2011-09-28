# global
# Created by: Christopher Bess
# if no pip or virtualenv, uncomment the two lines below
#sudo easy_install pip
#sudo pip install virtualenv

# local
# if on a Mac exec below line (maybe)
# ARCHFLAGS="-arch i386 -arch x86_64"
mkdir ../data && ../data/indexes
virtualenv ../sherlock_env --distribute --no-site-packages
source ../sherlock_env/bin/activate
pip install -r requirements.txt
