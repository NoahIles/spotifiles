import os
from my_logger import initEvent_Logger
from playhouse.db_url import connect, parse
from playhouse.pool import PooledMySQLDatabase

mL = initEvent_Logger()

def connectPooledDB():
    url = os.environ.get('DATABASE_URL')
    db = None
    if url is None:
        mL.DEBUG("DATABASE_URL is not set")
    else:
        mL.info("DATABASE_URL is set")
        args = {'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True }
        db = connect(url, **args)
        mL.info("Database connection established")
    if db is None:
        mL.error("Database connection failed")
    return db

def initPooledDB():
    url = os.environ.get('DATABASE_URL')
    d = parse(url)
    d.update({'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True })
    db = PooledMySQLDatabase(d.pop('database'), **d)
    # db = connect(url, "mysql+pool")
    return db


if __name__ == '__main__':
    db = connectPooledDB()
    print(db)
    # print(db.is_closed())
    # db.open()
    with db.atomic():
        print(db.get_tables())