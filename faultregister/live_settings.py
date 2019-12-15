import os

from .settings import *
import django_heroku

#
# DATABASES = {
#     'default': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': os.environ.get('DBNAME'),
#         'USER': os.environ.get('DBUSER'),
#         'PASSWORD': os.environ.get('DBPASS'),
#         'HOST': os.environ.get('DBHOST'),
#         "PORT": "",
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#             'isolation_level': 'READ UNCOMMITTED'
#         }
#     }
# }
#
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
DEBUG = True
django_heroku.settings(locals())
