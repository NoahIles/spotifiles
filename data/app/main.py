import os
from peewee import *
from fastapi import FastAPI
from playhouse.db_url import connect
from playhouse.dataset import DataSet
from pydantic import BaseModel

# Connection URL To MySQL Database
url = os.environ.get('DATABASE_URL')

app = FastAPI()
# mysql://user:passwd@ip:port/my_db
db = connect('{}'.format(url))

# $ Websites 
@app.get("/")
def read_root():
    return {"{}".format(url): "World"}

# Select top 10 rows of tweetData table
@app.get("/db/")
def read_db():
    cursor = db.execute_sql("select content, urll, likes, replies, retweets from tweetData order by likes desc limit 10")
    idk = cursor.fetchall()
    return {idk}

# Update specified tweet 'like' count by specified amount
@app.get("/update/{add_likes}/{tw_id}")
def read_item(add_likes: int, tw_id: str = "1118876219381026818"):
    bfore = db.execute_sql("select likes from tweetData where tweet_id = '{}'".format(tw_id))
    update_cursor = db.execute_sql("update tweetData set likes = likes + {} where tweet_id like {}".format(add_likes, tw_id))
    after = db.execute_sql("select likes from tweetData where tweet_id = '{}'".format(tw_id))
    after = after.fetchall()
    bfore = bfore.fetchall()
    return {"before Likes were": bfore, "after likes are": after}

