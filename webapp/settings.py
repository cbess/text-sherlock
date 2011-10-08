from core import settings as core_settings

DEBUG = core_settings.DEBUG
SECRET_KEY = 'dev_key_77h7h7h7'
CSRF_ENABLED = True
CSRF_SESSION_LKEY = 'dev_key_f87a8ewf8awe77=+'

# import local settings (override above settings)
# from webapp.local_settings import *