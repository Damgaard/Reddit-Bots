"""
A small scripts I wrote to notify me when new stuff about a subject is posted.

It's meant to be a tool for me. I work on a 64 Windows machine with python 2.7.
It may or may not work on other systems.

Use cronjobs / task manager to keep the program running.

TODO: Make callable with commandline arguments to improve versatility.
"""

import os

import praw

from authentication import USERNAME, PASSWORD

HERE = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(HERE, 'SubscriberDB.txt')

def load_last_found_id():
    try:
        with open(DB_FILE, 'r') as db:
            return db.read().strip()
    except IOError:
        return None

def store_last_found_id(new_id):
    with open(DB_FILE, 'w') as db:
        db.write(new_id)

def search_results(search_word, stop_id):
    """
    Yield search results coming from the search_word.

    Stop when we hit stop_id

    """
    for result in r.search(search_word, sort='new', limit=None,
                           place_holder=stop_id):
        yield result

def get_newest_id(search_word):
    return search_results(search_word, None).next().id

def is_valid_result(result, bad_words):
    """Does the title or subreddit contain a bad word?"""
    good_title = all(word not in result.title.lower() for word in bad_words)
    good_subreddit = all(word not in result.subreddit.display_name.lower()
                                  for word in bad_words)
    return good_title and good_subreddit

def message_me(result, search_word):
    title = 'New post about %s' % search_word
    body =  '[%s](%s)' % (result.title, result.url)
    r.send_message('_Daimon_', title, body)

r = praw.Reddit('WordSubscriber by u/_Daimon_ ver 0.1.1. Source see '
                'github.com/Damgaard/Reddit-Bots')
r.login(USERNAME, PASSWORD)
last_found_id = load_last_found_id()
search_word = 'praw'
bad_words = ['subreddit stats', 'electro', 'dubstep', 'house', 'music']
newest_id = get_newest_id(search_word)
for result in search_results(search_word, last_found_id):
    if is_valid_result(result, bad_words):
        message_me(result, search_word)
store_last_found_id(newest_id)
