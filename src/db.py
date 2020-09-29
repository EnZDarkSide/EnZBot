import pymysql

con = pymysql.connect('localhost', 'root',
                      '', 'enzbotdb')

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
    def update_dom(id, new_dom):
        pass
