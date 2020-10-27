from src.database.db import cur, DB


class DBPremium:
    @staticmethod
    async def get_all():
        await DB.exec_command('SELECT * FROM premium', False)
        return cur.fetchall()

    @staticmethod
    async def contains(user_id):
        await DB.exec_command(f'SELECT * FROM premium WHERE UserId={user_id}', False)
        return cur.fetchone()

    @staticmethod
    async def add_or_update(user_id, expiration_date):
        command = f"INSERT INTO premium (UserId, ExpirationDate) VALUES({user_id},'{expiration_date}') ON DUPLICATE KEY UPDATE" \
                  f" ExpirationDate='{expiration_date}'"
        return await DB.exec_command(command)
