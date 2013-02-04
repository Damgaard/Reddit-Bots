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
# The number of id's we keep to make sure that a result haven't been processed
# before. One is insufficient as if becomes deleted/removed/placed in private
# subreddit, then we will message for every returned result.
IDS_KEPT = 3

def main():
    r = praw.Reddit('WordSubscriber by u/_Daimon_ ver 0.1.1. Source see '
                    'github.com/Damgaard/Reddit-Bots')
    r.login(USERNAME, PASSWORD)
    last_found_ids = load_last_found_ids()
    search_word = 'praw'
    bad_words = ['subreddit stats', 'electro', 'dubstep', 'house', 'music']
    newest_ids = get_newest_ids(r, search_word)
    for result in search_results(r, search_word, last_found_ids):
        if is_valid_result(result, bad_words):
            message_me(r, result, search_word)
    store_last_found_ids(newest_ids)

def load_last_found_ids():
    try:
        with open(DB_FILE, 'r') as db:
            last_ids = db.readlines()[:IDS_KEPT]
            last_ids = [id.strip() for id in last_ids if id.strip() != '']
            return last_ids + [None] * (IDS_KEPT - len(last_ids))
    except IOError:
        return [None] * IDS_KEPT

def store_last_found_ids(new_ids):
    with open(DB_FILE, 'w') as db:
        for id in new_ids:
            db.write("%s\n" % id)

def search_results(reddit_session, search_word, stop_ids):
    """
    Yield search results coming from the search_word.

    Stop when we hit stop_id

    """
    for result in reddit_session.search(search_word, sort='new', limit=None,
                                        place_holder=stop_ids[0]):
        if result.id in stop_ids:
            break
        yield result

def get_newest_ids(reddit_session, search_word):
    result_generator = reddit_session.search(search_word, sort='new',
                                             limit=IDS_KEPT)
    newest_ids = list(result.id for result in result_generator)
    return newest_ids + [None] * (IDS_KEPT - len(newest_ids))

def is_valid_result(result, bad_words):
    """Does the title or subreddit contain a bad word?"""
    good_title = all(word not in result.title.lower() for word in bad_words)
    good_subreddit = all(word not in result.subreddit.display_name.lower()
                                  for word in bad_words)
    return good_title and good_subreddit

def message_me(reddit_session, result, search_word):
    title = 'New post about %s' % search_word
    body =  '[%s](%s)' % (result.title, result.permalink)
    reddit_session.send_message('_Daimon_', title, body)

if __name__ == '__main__':
    main()
