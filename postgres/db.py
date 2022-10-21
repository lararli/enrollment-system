from contextlib import AsyncExitStack
import asyncpg
from datetime import datetime


class Connection:
    """
    Context manager to manage the connection with a postgres database.
    """

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
    """
    Configure and manage the session for a postgres DB with dependency injection.
    """

    def __init__(self, conn: Connection = None):
        self.conn = conn

    async def add_user(self, account_data: dict) -> None:
        """
        Insert a new user into the account table given a dictionary with the user information.
        Args:
            account_data: dictionary that contains user information to insert in the database.

        Returns: None

        """
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

    async def deactivate_user(self, user_id: int) -> None:
        """
        Set the "active" column in the account table as false to indicates the user are deactivated.
        Args:
            user_id: id of the user to update the information.

        Returns: None

        """
        async with self.conn as conn:
            await conn.execute('''
            UPDATE account
                SET active = False
                WHERE account_id = $1
            ''',
                               user_id)

    async def add_course(self, course_data: dict) -> None:
        """
        Insert a new course into the course table given a dictionary with the course information.
        Args:
            course_data: dictionary that contains course information to insert into the user database.

        Returns: None

        """
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

    async def deactivate_course(self, course_id: int) -> None:
        """
        Set the "active" column in the account table as false to indicates the user are deactivated.
        Args:
            course_id: id of the user to update the information.

        Returns: None

        """
        async with self.conn as conn:
            await conn.execute('''
            UPDATE course
                SET active = false
                WHERE course_id = $1
            ''',
                               course_id)

    async def enroll_user(self, account_id: int, course_id: int) -> None:
        """
        Add a new enrollment in the enrollment table given a account_id and a course_id
        Args:
            account_id: id of the user
            course_id: if of the course

        Returns:

        """
        async with self.conn as conn:
            await conn.execute('''
            INSERT INTO 
                enrollment(account_id, course_id)
            VALUES
                ($1, $2)
            ''',
                               account_id,
                               course_id)

    async def search(self, table: str, column: str, value: str):
        """
        Search a register or a list of register given a table, column and a value to filter this column.
        Args:
            table: name of the table
            column: column you want to filter
            value: value you want to filter

        Returns:

        """
        async with self.conn as conn:
            res = await conn.fetch(f"SELECT * FROM {table} where {column} = '{value}'")

            if res:
                data = [dict(result) for result in res]
                if table == 'account':
                    # it returns just one user
                    return data[0]
                # return a list of dictionaries with all registers.
                return data
            return None

    async def delete_enrollment(self, value: str):
        async with self.conn as conn:
            await conn.execute('''
                        DELETE FROM enrollment
                        WHERE account_id = $1
                        ''',
                               value)

    async def delete_user(self, value: str):
        async with self.conn as conn:
            await conn.execute('''
                        DELETE FROM account
                        WHERE account_id = $1
                        ''',
                               value)

