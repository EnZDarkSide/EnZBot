from src.database.db import DB, cur


class DBTransport:
    @staticmethod
    def get_home_stop_id(user_id: int) -> int:
        DB.exec_command(f'SELECT HomeStopId FROM transport WHERE UserId={user_id}', False)
        return int(cur.fetchone())

    @staticmethod
    def save_home_stop_id(user_id: int, home_stop_id: int) -> bool:
        return DB.exec_command(
            f"INSERT INTO transport (UserId, HomeStopId) "
            f"VALUES ({user_id}, {home_stop_id}) "
            f"ON DUPLICATE KEY UPDATE HomeStopId='{home_stop_id}'"
        )

    @staticmethod
    def get_university_stop_id(user_id: int) -> int:
        DB.exec_command(f'SELECT UniversityStopId FROM transport WHERE UserId={user_id}', False)
        return int(cur.fetchone())

    @classmethod
    def save_university_stop_id(cls, user_id: int, university_stop_id: int) -> bool:
        return DB.exec_command(
            f"INSERT INTO transport (UserId, HomeStopId) "
            f"VALUES ({user_id}, {university_stop_id}) "
            f"ON DUPLICATE KEY UPDATE HomeStopId='{university_stop_id}'"
        )
