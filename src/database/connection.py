import os

import pymysql
from vbml import Pattern

pattern = Pattern('mysql://<login>:<pass>@<host>/<database>?reconnect=true')


def get_local_con():
    return pymysql.connect(host='localhost', user='enzbot', password='password',
                           db='enzbotdb')


def get_global_con():
    pattern(os.environ["CLEARDB_DATABASE_URL"])
    connection = pattern.dict()
    return pymysql.connect(host=connection['host'], user=connection['login'], password=connection['pass'],
                           db=connection['database'], charset='cp1251')
