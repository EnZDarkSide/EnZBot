# -*- coding: utf-8 -*-
from src.database.db import cur, DB


class DBPortal:
    @staticmethod
    def get_all():
        DB.exec_command('SELECT * FROM portal', False)
        return cur.fetchall()

    @staticmethod
    def get(user_id):
        DB.exec_command(f'SELECT Login, Password, Subjects FROM portal WHERE UserId={user_id}', False)
        return cur.fetchone()

    @staticmethod
    def get_subjects(user_id) -> str:
        DB.exec_command(f'SELECT Subjects FROM portal WHERE UserId={user_id}', False)
        return cur.fetchone()

    @staticmethod
    def add_or_update(user_id, login, password):
        command = f"INSERT INTO portal (UserId, Login, Password) VALUES({user_id}, '{login}', '{password}')" \
                  f" ON DUPLICATE KEY UPDATE" \
                  f" Login='{login}', Password='{password}'"
        return DB.exec_command(command)

    @staticmethod
    def update_subjects(user_id, subjects: []):
        subj_str = ','.join(subjects)
        command = f"UPDATE portal SET Subjects='{subj_str}' WHERE UserId='{user_id}'"
        return DB.exec_command(command)
