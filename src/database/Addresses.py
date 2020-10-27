from src.database.db import cur, DB


class DBAddresses:
    @staticmethod
    async def get_all():
        await DB.exec_command('SELECT * FROM addresses', False)
        return cur.fetchall()

    @staticmethod
    async def contains(user_id):
        await DB.exec_command(f'SELECT * FROM addresses WHERE UserId={user_id}', False)
        return cur.fetchone()

    @staticmethod
    async def add_or_update(user_id, address):
        command = f"INSERT INTO addresses (UserId, Address) VALUES({user_id},'{address}') ON DUPLICATE KEY UPDATE" \
                  f" Address='{address}'"
        return await DB.exec_command(command)

    @staticmethod
    async def set_home_tram_stop(user_id, stop):
        command = f"INSERT INTO addresses (UserId, Home) VALUES({user_id},'{stop}') ON DUPLICATE KEY UPDATE" \
                  f" Home='{stop}'"
        return await DB.exec_command(command)

    @staticmethod
    async def set_university_tram_stop(user_id, stop):
        command = f"INSERT INTO addresses (UserId, University) VALUES({user_id},'{stop}') ON DUPLICATE KEY UPDATE" \
                  f" University='{stop}'"
        return await DB.exec_command(command)
