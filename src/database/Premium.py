from src.database.db import cur, DB


class DBPremium:
    @staticmethod
    def get_all():
        DB.exec_command('SELECT * FROM premium', False)
        return cur.fetchall()

    @staticmethod
    def contains(user_id):
        DB.exec_command(f'SELECT * FROM premium WHERE UserId={user_id}', False)
        return cur.fetchone()

    @staticmethod
    def add_or_update(user_id, expiration_date):
        command = f"INSERT INTO premium (UserId, ExpirationDate) VALUES({user_id},'{expiration_date}') ON DUPLICATE KEY UPDATE" \
                  f" ExpirationDate='{expiration_date}'"
        return DB.exec_command(command)
