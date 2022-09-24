from contextlib import AsyncExitStack
import asyncpg

from dotenv import load_dotenv
import os
load_dotenv()

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


class Client:

    def __init__(self, conn: Connection = None):
        self.conn = conn

    async def add_user(self, user_data):
        async with self.conn as conn:
            res = await conn.execute('''
            INSERT INTO users(user_id, email, password, created_date)
            VALUES($1, $2, $3, $4)
            ''',
                                     user_data.get('user_id'),
                                     user_data.get('email'),
                                     user_data.get('password'),
                                     user_data.get('created_date'))
        return res

    async def add_course(self, course_data):
        async with self.conn as conn:
            res = await conn.execute('''
            INSERT INTO 
                courses(course_id, course_name, active, created_date, workload, related_topics, created_by)
            VALUES
                ($1, $2, $3, $4, $5, $6, $7)
            ''',
                                     course_data.get('course_id'),
                                     course_data.get('course_name'),
                                     course_data.get('active'),
                                     course_data.get('created_date'),
                                     course_data.get('workload'),
                                     course_data.get('related_topics'),
                                     course_data.get('created_by'))
            return res

    async def add_session(self, session_data):
        async with self.conn as conn:
            res = await conn.execute('''
            INSERT INTO 
                courses(course_id, course_name, active, created_date, workload, related_topics, created_by)
            VALUES
                ($1, $2, $3, $4)
            ''',
                                     session_data.get('session_id'),
                                     session_data.get('user_id'),
                                     session_data.get('start_date'),
                                     session_data.get('end_date'))
            return res

    async def add_enrollments(self, enrollment_data):
        async with self.conn as conn:
            res = await conn.execute('''
            INSERT INTO 
                courses(course_id, course_name, active, created_date, workload, related_topics, created_by)
            VALUES
                ($1, $2, $3, $4)
            ''',
                                     enrollment_data.get('user_id'),
                                     enrollment_data.get('course_id'),
                                     enrollment_data.get('session_id'),
                                     enrollment_data.get('enrollment_id'))
            return res

    async def search(self, table, column, id):
        async with self.conn as conn:
            res = await conn.fetchrow(f'SELECT * FROM {table} where {column} = {id}')
            print(dict(res))
            return res
