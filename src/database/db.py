from src.database.connection import get_global_con

# con = get_local_con()
con = get_global_con()

cur = con.cursor()


class DB:
    @staticmethod
    async def exec_command(command, to_commit=True):
        try:
            affected_rows = await cur.execute(command)

            if to_commit:
                con.commit()

            print(f'affected rows: {affected_rows}')
            print(f'command: {command}')
            return True
        except Exception as e:
            print(f'command: {command}')
            print(e)
            return False
