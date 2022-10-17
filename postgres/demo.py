import asyncio
from postgres.db import Connection, DB
from credentials import credentials
from datetime import datetime

connection = Connection(user=credentials.get('user'),
                        pwd=credentials.get('password'),
                        db=credentials.get('database'),
                        host=credentials.get('host'))

client = DB(connection)

d = {
    'name': 'Git Crash Course',
    'course_id': 2,
    'workload': 2.0,
    'created_by': ['Fulano', 'Beltrano'],
    'created_date': datetime.strptime('2017-08-09 12:12:12', '%Y-%m-%d %H:%M:%S'),
    'related_topics': ['Python', 'Programming', 'Technology', 'Algorithms']
}


s = {
    'start_date': datetime.strptime('2017-08-09 12:12:12', '%Y-%m-%d %H:%M:%S'),
    'end_date': datetime.strptime('2017-08-09 12:45:12', '%Y-%m-%d %H:%M:%S'),
    'account_id': 1
}


e = {
    'account_id': 1,
    'course_id': 2,
    'session_id': 1,
    'enrollment_date': datetime.strptime('2017-08-09 12:45:12', '%Y-%m-%d %H:%M:%S')
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.search(table='course', column='active', value=True))
    loop.close()
