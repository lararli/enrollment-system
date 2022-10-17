import asyncio
from postgres.db import Connection, DB
from credentials import credentials
from datetime import datetime

connection = Connection(user=credentials.get('user'),
                        pwd=credentials.get('password'),
                        db=credentials.get('database'),
                        host=credentials.get('host'))

client = DB(connection)


async def main():
    results = await client.search(table='account', column='email', value='fulano@email.com')
    print(type(results[0].get('active')))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
