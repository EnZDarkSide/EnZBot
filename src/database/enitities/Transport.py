from src.database.db import DB


class DBTransport:
    @staticmethod
    def save_home_stop_id(user_id: int, home_stop_id: int) -> bool:
        return DB.exec_command(
            f"INSERT INTO transport (UserId, HomeStopId) "
            f"VALUES ({user_id}, {home_stop_id}) "
            f"ON DUPLICATE KEY UPDATE HomeStopId='{home_stop_id}'"
        )
