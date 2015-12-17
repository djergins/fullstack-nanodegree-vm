#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach
## Database connection


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    query = "select * from posts order by id desc"
    c.execute(query)
    results = c.fetchall()
    print(results)
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in results]
    # posts.sort(key=lambda row: row['time'], reverse=True)
    DB.close()
    return posts

    """Clean an HTML fragment and return it."""

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    query = "insert into posts (content) values (%s)"
    c.execute(query, (bleach.clean(content), ))
    DB.commit()
    DB.close()
    
