#!/usr/bin/env python

"""
Breaks down a redditors karma by subreddit.

Usage: karma_breakdown redditor1 redditor2

The input should the names of redditors. It outputs 2 tables with karma 
breakdowns of comments and submissions by subreddit.

This program is part of the beginners tutorial on the python wrapper module
of Reddits API, which can be found here
https://github.com/praw-dev/praw/wiki/Getting-Started

Created by Andreas Damgaard Pedersen 22 April 2012
Reddit username: _Daimon_
"""

import argparse
import operator
import sys
import urllib2

import praw

def sort_and_cut(dic, limit):
    """Returns a sorted list containing the highest 'limit' elements"""
    return sorted(dic.iteritems(), key=operator.itemgetter(1), 
                  reverse=True)[:limit]

def term_print(karma_by_subreddit):
    """Print dict from main in nice readable format"""
    width = 25
    align = (">","<")
    titel = ("Subreddit", "Karma")
    print "{titel[0]:{align[0]}{width}} | {titel[1]:{align[1]}{width}}" \
        .format(titel = titel, align = align, width = width)
    print "{0:^{width}}".format("-"*width, width=width*2+1)
    for (subreddit, karma) in karma_by_subreddit:
        print "{subreddit:{align[0]}{width}} | {karma:{align[1]} {width}}" \
            .format(subreddit = subreddit, karma = karma, 
                   width = width, align = align)
    print

def main(user, thing_type="submissions"):
   """
   Create a dictionary with karma breakdown by subreddit.
      
   Takes a user and a thing_type (either 'submissions' or 'comments') 
   as input. Return a directory where the keys are display names of 
   subreddits, like proper or python, and the values are how much 
   karma the user has gained in that subreddit.
   """
   RETRIEVE_LIMIT = 100
   karma_by_subreddit = {}
   thing_limit = RETRIEVE_LIMIT
   user = r.get_redditor(user)
   gen = (user.get_comments(limit=thing_limit) if thing_type == "comments" else
          user.get_submitted(limit=thing_limit))
   for thing in gen:
       subreddit = thing.subreddit.display_name
       karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) 
                                        + thing.ups - thing.downs)
   return karma_by_subreddit

if __name__ == "__main__":
    CUT_LIMIT = 5
    DEFAULT_REDDITORS = ['_Daimon_']
    user_agent = "Karma breakdown 1.1 by /u/_Daimon_"
    r = praw.Reddit(user_agent=user_agent)
    parser = argparse.ArgumentParser(description=
            """Break down a users karma by subreddit""")
    parser.add_argument('redditors', metavar='N', type=str, nargs='*',
                default=DEFAULT_REDDITORS, help='Redditors to analyse')
    parser.add_argument('-c', '--comments', dest='show_comments', 
                action='store_false', help='Disable karma break for comments')
    parser.add_argument('-s', '--submissions', dest='show_submissions', 
                action='store_false', help='Disable karma break for submissions')
    args = parser.parse_args()
    break_by = ['comments', 'submissions']
    if not args.show_comments:
        break_by.remove('comments')
    if not args.show_submissions:
        break_by.remove('submissions')
    if not len(break_by):
        print >> sys.stderr, ("ERROR. Both comments and submission breaking " + 
                              "disabled!")
        sys.exit(-1)
    for user in args.redditors:
        try:
            for thing_type in break_by:
                karma = main(user, thing_type=thing_type)
                karma = sort_and_cut(karma, CUT_LIMIT)
                print "{0} karma for {1}".format(thing_type, user)
                term_print(karma)
        except urllib2.HTTPError:
            print "The user {0} does not exist!!".format(user)
