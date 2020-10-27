# -*- coding: utf-8 -*-
from src.database.db import cur, DB


class DBGroups:
    @staticmethod
    async def get_all():
        await DB.exec_command('SELECT * FROM groups', False)
        return cur.fetchall()

    @staticmethod
    async def get(user_id):
        await DB.exec_command(f'SELECT GroupName FROM groups WHERE UserId={user_id}', False)
        return cur.fetchone()

    @staticmethod
    async def add_or_update(user_id, group):
        command = f"INSERT INTO groups (UserId, GroupName) VALUES({user_id},'{group}') ON DUPLICATE KEY UPDATE" \
                  f" GroupName='{group}'"
        return await DB.exec_command(command)
