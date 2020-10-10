import pymysql

con = pymysql.connect('sql7.freesqldatabase.com', 'sql7369933',
                      'xWUCnPAEmW', 'sql7369933')

cur = con.cursor()


class Users:
    @staticmethod
    def contains(id):
        cur.execute(str.format('SELECT * FROM users WHERE UserId={0}', id))
        return cur.fetchone()

    @staticmethod
    def create_new(id):
        command = str.format("INSERT INTO users UserId VALUES ('{0}')", id)
        cur.execute(command)

    @staticmethod
    def update_full_name(id, full_name):
        pass

    @staticmethod
    def update_dorm(id, new_dom):
        pass
