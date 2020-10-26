import json
import os

import pymysql


def get_local_con():
    return pymysql.connect(host='localhost', user='enzbot', password='password',
                           db='enzbotdb')


def get_global_con():
    with open('../../settings.json') as connections_file:
        connection = json.load(connections_file)
    return pymysql.connect(host=connection['host'], user=connection['login'], password=connection['pass'],
                           db=connection['database'], charset='cp1251')
