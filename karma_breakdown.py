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
    align = (">", "<")
    titel = ("Subreddit", "Karma")
    print "{titel[0]:{align[0]}{width}} | {titel[1]:{align[1]}{width}}" \
        .format(titel=titel, align=align, width=width)
    print "{0:^{width}}".format("-" * width, width=width * 2 + 1)
    for subreddit, karma in karma_by_subreddit:
        print "{subreddit:{align[0]}{width}} | {karma:{align[1]} {width}}" \
            .format(subreddit=subreddit, karma=karma, width=width, align=align)
    print


def main(user, limit, thing_type="submissions"):
    """
    Create a dictionary with karma breakdown by subreddit.

    Takes a user and a thing_type (either 'submissions' or 'comments')
    as input. Return a directory where the keys are display names of
    subreddits, like proper or python, and the values are how much
    karma the user has gained in that subreddit.
    """
    karma_by_subreddit = {}
    user = r.get_redditor(user)
    gen = (user.get_comments(limit=limit) if thing_type == "comments" else
           user.get_submitted(limit=limit))
    for thing in gen:
        subreddit = thing.subreddit.display_name
        karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0)
                                         + thing.ups - thing.downs)
    return karma_by_subreddit


if __name__ == "__main__":
    user_agent = "Karma breakdown 1.1 by /u/_Daimon_"
    r = praw.Reddit(user_agent=user_agent)
    parser = argparse.ArgumentParser(
        description="Break down a users karma by subreddit")
    parser.add_argument('redditors', metavar='N', type=str, nargs='*',
                        default=['_Daimon_'], help='Redditors to analyse')
    parser.add_argument('-c', '--comments', dest='show_comments',
                        action='store_false',
                        help="Don't breakdown comments karma")
    parser.add_argument('-s', '--submissions', dest='show_submissions',
                        action='store_false',
                        help="Don't breakdown submissions karma")
    parser.add_argument('--limit', dest='limit', type=int, default=100,
                        help='How many entries are examined')
    parser.add_argument('--highest', dest='highest', type=int, default=5,
                        help='This number of subreddits with highest karma'
                             'gained are shown')
    args = parser.parse_args()
    break_by = ['comments'] if args.show_comments else []
    break_by += ['submissions'] if args.show_submissions else []
    if not break_by:
        print "ERROR. Both comments and submission breaking disabled!"
        sys.exit(-1)
    for user in args.redditors:
        try:
            for thing_type in break_by:
                karma = main(user, args.limit, thing_type=thing_type)
                karma = sort_and_cut(karma, args.highest)
                print "{0} karma for {1}".format(thing_type, user)
                term_print(karma)
        except urllib2.HTTPError:
            print "The user {0} does not exist!!".format(user)
