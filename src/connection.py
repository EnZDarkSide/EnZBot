import pymysql


def get_local_con():
    return pymysql.connect('localhost', 'root', '', 'enzbotdb')


def get_global_con():
    return pymysql.connect('VH282.spaceweb.ru', 'enzdarksid', 'cRM6JRT1Bobx', 'enzdarksid')