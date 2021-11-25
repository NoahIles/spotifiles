import os
from my_logger import initEvent_Logger
from playhouse.db_url import connect

mL = initEvent_Logger()

def connectDB():
    url = os.environ.get('DATABASE_URL')
    db = None
    if url is None:
        mL.DEBUG("DATABASE_URL is not set")
    else:
        mL.info("DATABASE_URL is set")
        args = {'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True}
        db = connect(url,**args)
        mL.info("Database connection established")
    if db is None:
        mL.error("Database connection failed")
    return db

if __name__ == '__main__':
    try:
        connectDB()
        print("Successfully connected to database")
    except Exception as e:
        mL.error("Database connection failed")
        print(e)