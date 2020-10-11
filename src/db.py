import pymysql

from src.connection import get_global_con, get_local_con

con = get_local_con()
# con = get_global_con()

cur = con.cursor()


class Users:

    @staticmethod
    def get_all():
        Users.exec_command('SELECT * FROM users', False)
        return cur.fetchall()

    @staticmethod
    def contains(user_id):
        Users.exec_command(f'SELECT * FROM users WHERE UserId={user_id}', False)
        return cur.fetchone()

    @staticmethod
    def add(user_id):
        command = f"INSERT INTO users(UserId) VALUES ({user_id})"
        return Users.exec_command(command)

    @staticmethod
    def add(user_id, full_name):
        command = f"INSERT INTO users(UserId, FullName) VALUES ({user_id}, '{full_name}')"
        return Users.exec_command(command)

    # @staticmethod
    # def update_full_name(user_id, full_name):
    #     command = f"UPDATE users SET FullName='{full_name}' WHERE Id='{user_id}'"
    #     return Users.exec_command(command)

    @staticmethod
    def update_address(user_id, address):
        command = f"INSERT INTO addresses (UserId, Address) VALUES({user_id},'{address}') ON DUPLICATE KEY UPDATE" \
                  f" Address='{address}'"
        return Users.exec_command(command)

    @staticmethod
    def exec_command(command, to_commit=True):
        try:
            affected_rows = cur.execute(command)

            if to_commit:
                con.commit()

            print(f'affected rows: {affected_rows}')
            print(f'command: {command}')
            return True
        except Exception as e:
            print(e)
            return False
