# -*- coding: utf-8 -*-
from src.database.db import cur, DB


class DBGroups:
    @staticmethod
    def get_all():
        DB.exec_command('SELECT * FROM groups', False)
        return cur.fetchall()

    @staticmethod
    def get(user_id):
        DB.exec_command(f'SELECT GroupName FROM groups WHERE UserId={user_id}', False)
        return cur.fetchone()

    @staticmethod
    def add_or_update(user_id, group):
        command = f"INSERT INTO groups (UserId, GroupName) VALUES({user_id},'{group}') ON DUPLICATE KEY UPDATE" \
                  f" GroupName='{group}'"
        return DB.exec_command(command)
