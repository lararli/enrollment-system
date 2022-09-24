import asyncio
from db import Connection, Client
from datetime import datetime
from credentials import credentials

connection = Connection(user=credentials.get('user'),
                        pwd=credentials.get('password'),
                        db=credentials.get('database'),
                        host=credentials.get('host'))

c = Client(connection)

d = {'course_id': 1,
     'course_name': 'Python for Beginners',
     'active': True,
     'created_date': datetime.now(),
     'workload': 2.5,
     'related_topics': ['Python', 'Programming', 'Technology'],
     'created_by': ['Lara']}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(c.search(table='courses', column='course_id', id=1))
    loop.close()
