Reddit Bots
===========

This repository contains some of my bots that uses the Python wrapper of the
Reddit API.

Created by

    *- Andreas Damgaard Pedersen*

Undo Me
-------

Deletes all the comments and submissions made by the logged-in user.

Karma Breakdown
---------------

This program allows us to get break down where a user got his karma. It is
similar to a `reddit gold <http://www.reddit.com/help/gold>`_ feature, except
we can get the karma breakdown for any user not just ourselves. It is less
precise than the official feature. Strictly speaking this is a program, not a
bot. It is included in this repo anyway as it serves as a nice introduction to
writing bots that uses the reddit api.

NOTE: This feature is now also available to non-gold user. Visit your userpage
and there will be a blue link on the top right half on the screen.

Nerd Baller
-----------

Creates an overview of post made by notables in the Starcraft 2 Scene.

Word Subscriber
---------------

Sends a user a message whenever a one of a series of words are used. Also
supports filtering out results from certain subreddits or with certain words
in their title. This is very useful if the words you search for are commonly
used in another context. For instance, I'm interested in knowing when the
`praw python module <https://github.com/praw-dev/praw>`_ is mentioned, but I
don't care about the artist `john praw <http://johnpraw.bandcamp.com/album/
john-praw>`_.
