from typing import Union

from src.database.db import DB, cur


class DBTransport:
    r"""API для чтения из\записи в таблицу 'transport' БД"""

    @staticmethod
    def get_home_stop_id(user_id: int) -> Union[int, None]:
        """Возвращает идентификатор остановки дома или None"""

        DB.exec_command(f'SELECT HomeStopId FROM transport WHERE UserId={user_id}', False)

        try:
            return cur.fetchone()[0]
        except IndexError:
            return None

    @staticmethod
    def save_home_stop_id(user_id: int, home_stop_id: int) -> bool:
        """Сохраняет идентификатор остановки дома"""

        return DB.exec_command(
            f"INSERT INTO transport (UserId, HomeStopId) "
            f"VALUES ({user_id}, {home_stop_id}) "
            f"ON DUPLICATE KEY UPDATE HomeStopId='{home_stop_id}'"
        )

    @staticmethod
    def get_university_stop_id(user_id: int) -> Union[int, None]:
        """Возвращает идентификатор остановки университета или None"""

        DB.exec_command(f'SELECT UniversityStopId FROM transport WHERE UserId={user_id}', False)

        try:
            return cur.fetchone()[0]
        except IndexError:
            return None

    @classmethod
    def save_university_stop_id(cls, user_id: int, university_stop_id: int) -> bool:
        """Сохраняет идентификатор остановки университета"""

        return DB.exec_command(
            f"INSERT INTO transport (UserId, UniversityStopId) "
            f"VALUES ({user_id}, {university_stop_id}) "
            f"ON DUPLICATE KEY UPDATE  UniversityStopId='{university_stop_id}'"
        )
