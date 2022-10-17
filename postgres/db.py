from contextlib import AsyncExitStack
import asyncpg
from datetime import datetime


class Connection:

    def __init__(self, user: str, pwd: str, db: str, host: str):
        self.exit_stack = AsyncExitStack()
        self.user = user
        self.pwd = pwd
        self.db = db
        self.host = host
        self.conn = None

    async def __aenter__(self):
        self.conn = await asyncpg.connect(
            user=self.user,
            password=self.pwd,
            database=self.db,
            host=self.host)
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()


class DB:

    def __init__(self, conn: Connection = None):
        self.conn = conn

    async def add_user(self, account_data: dict):
        async with self.conn as conn:
            await conn.execute('''
            INSERT INTO account(first_name, last_name, email, hashed_password, account_role)
            VALUES($1, $2, $3, $4, $5)
            ''',
                               account_data.get('first_name'),
                               account_data.get('last_name'),
                               account_data.get('email'),
                               account_data.get('password'),
                               account_data.get('account_role'))

    async def deactivate_user(self, user_id: int):
        async with self.conn as conn:
            await conn.execute('''
            UPDATE account
                SET active = False
                WHERE account_id = $1
            ''',
                               user_id)

    async def add_course(self, course_data: dict):
        async with self.conn as conn:
            await conn.execute('''
            INSERT INTO 
                course(name, workload, created_by, related_topics)
            VALUES
                ($1, $2, $3, $4)
            ''',
                               course_data.get('name'),
                               course_data.get('workload'),
                               course_data.get('created_by'),
                               course_data.get('related_topics'))

    async def deactivate_course(self, course_id: int):
        async with self.conn as conn:
            await conn.execute('''
            UPDATE course
                SET active = false
                WHERE course_id = $1
            ''',
                               course_id)

    async def add_session(self, session_data: dict):
        async with self.conn as conn:
            await conn.execute('''
            INSERT INTO 
                session(start_date, end_date, account_id)
            VALUES
                ($1, $2, $3)
            ''',
                               session_data.get('start_date'),
                               session_data.get('account_id'))

    async def add_enrollments(self, enrollment_data: dict):
        async with self.conn as conn:
            res = await conn.execute('''
            INSERT INTO 
                enrollment(account_id, course_id, session_id, enrollment_date)
            VALUES
                ($1, $2, $3, $4)
            ''',
                                     enrollment_data.get('account_id'),
                                     enrollment_data.get('course_id'),
                                     enrollment_data.get('session_id'))
            return res

    async def search(self, table: str, column: str, value: str):
        async with self.conn as conn:
            res = await conn.fetch(f"SELECT * FROM {table} where {column} = '{value}'")

            if res:
                data = [dict(result) for result in res]
                if table == 'account':
                    # it returns just one user
                    return data[0]
                return data
            return None

