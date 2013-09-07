"""
Undo Me

Deletes all your comments and submissions on Reddit.
"""

import praw

useragent = """Undo-me deletes all of a redditors comments & submissions.
               Created by u/_Daimon_. Source
               https://github.com/Damgaard/Reddit-Bots."""

r = praw.Reddit(useragent)
r.login()

for item in r.user.get_overview(limit=None):
    item.delete()
