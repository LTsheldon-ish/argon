# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from argo_conf import ConfigDB,ConfigCache,ConfigBase

'''  MySQL setting '''

HOST = ConfigDB.host
PORT = ConfigDB.port
USER = ConfigDB.user
PASSWD = ConfigDB.passwd
DBNAME = ConfigDB.dbname

''' Cache settting '''

CHOST = ConfigCache.host
CPORT = ConfigCache.port


''' Other setting '''

SQL_TPL_DIR = ConfigBase.data_dir
BASE_TABLE = [ 'attachead','boardhead','sectionhead','user','userattr']
