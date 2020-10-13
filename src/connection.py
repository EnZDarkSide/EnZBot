import pymysql
import json


def get_local_con():
    return pymysql.connect('localhost', 'enzbot', 'password', 'enzbotdb')


def get_global_con():
    with open('settings.json') as connections_file:
        connection = json.load(connections_file)
    return pymysql.connect(connection['host'], connection['login'], connection['pass'], connection['database'])
