from src.database.db import cur, DB


class DBAddresses:
    @staticmethod
    def get_all():
        DB.exec_command('SELECT * FROM addresses', False)
        return cur.fetchall()

    @staticmethod
    def contains(user_id):
        DB.exec_command(f'SELECT * FROM addresses WHERE UserId={user_id}', False)
        return cur.fetchone()

    @staticmethod
    def add_or_update(user_id, address):
        command = f"INSERT INTO addresses (UserId, Address) VALUES({user_id},'{address}') ON DUPLICATE KEY UPDATE" \
                  f" Address='{address}'"
        return DB.exec_command(command)

    @staticmethod
    def set_home_tram_stop(user_id, stop):
        command = f"INSERT INTO addresses (UserId, Home) VALUES({user_id},'{stop}') ON DUPLICATE KEY UPDATE" \
                  f" Home='{stop}'"
        return DB.exec_command(command)

    @staticmethod
    def set_university_tram_stop(user_id, stop):
        command = f"INSERT INTO addresses (UserId, University) VALUES({user_id},'{stop}') ON DUPLICATE KEY UPDATE" \
                  f" University='{stop}'"
        return DB.exec_command(command)
