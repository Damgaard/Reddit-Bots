#!/usr/bin/env python

'''
Create overview of submissions made by SC2 Notables

Author: Andreas Damgaard Pedersen
Date: 8 May 2012
'''

import re
import time

import reddit

# Reddits taken from http://www.reddit.com/r/starcraft/comments/rs2t1/more_related_reddits/
# And added starcraft + iama
SC_REDDITS = ('starcraft', 'iama', 'AlmostRelevant', 'broodwar',
              'BuildingEsports', 'Destiny', 'HuskyStarcraft',
              'KarmaStarcraft', 'sc2mods', 'starcat', 'starcraft2',
              'starcraftvods', 'thegdstudio', 'trueStarcraft')


# Definition and list here
# http://www.reddit.com/r/starcraft/comments/p8rca/guide_to_account_approval_on_rstarcraft/
class Baller:
    """A baller is someone who has the inside scoop of Starcraft.
       Professional Gamers, Casters or Industry insiders."""
    def __init__(self, (redditor_link, desc, roles)):
        self.redditor = redditor_link.split('/')[-1]
        self.redditor_link = redditor_link
        self.roles = roles.replace(" ", "").split(",")
        has_link = re.search("\[(?P<desc>.*?)\]\((?P<link>.*?)\)", desc)
        if has_link:
            self.desc = ("<a href='" + has_link.group('link') +
                         "' target=_blank>" + has_link.group('desc') + "</a>")
        else:
            self.desc = desc


def get_ballers(ids):
    """Build a list of ballers by going through the approved users pages"""
    text = "\n".join(r.get_submission(submission_id=d).selftext for d in ids)
    everybody = re.findall("\[.*?\]\((?P<user_link>.*?)\)\|" +
                           "(?P<desc>.*?)\|(?P<roles>.*?)(?=\n|\Z)", text)
    print "Total ballers = %d" % len(everybody)
    return (Baller(person) for person in everybody)


def build_subs(ballers):
    """Return a list of pairings (baller, sub) with the information about
       the baller that made the submission"""
    result = []
    baller_num = 0
    for baller in ballers:
        print "Currently looking at baller %d" % baller_num
        baller_num += 1
        redditor = r.get_redditor(baller.redditor)
        for sub in redditor.get_submitted(limit=None):
            if (sub.subreddit.display_name in SC_REDDITS):
                result.append((baller, sub))
    return result


def split_by_role(paired):
    """Add the (baller, sub) pairings to a dictionary with keys of roles
       based on the ballers role"""
    roles = {"PG": [], "II": [], "CC": [], "all_by_karma": paired,
                       "all_by_name": paired, 'all_by_date': paired}
    for baller, submission in paired:
        for role in roles:
            if role in baller.roles:
                roles[role].append((baller, submission))
    return roles


def sort_pairings_in_roles(roles):
    """Sort the (baller, submission) pairings in the roles"""
    roles['PG'] = sorted(roles['PG'], key=lambda (b, s): s.score, reverse=True)
    roles['II'] = sorted(roles['II'], key=lambda (b, s): s.score, reverse=True)
    roles['CC'] = sorted(roles['CC'], key=lambda (b, s): s.score, reverse=True)
    roles['all_by_karma'] = sorted(roles['all_by_karma'],
                                   key=lambda (b, s): s.score, reverse=True)
    roles['all_by_name'] = sorted(roles['all_by_name'],
                                  key=lambda (b, s): (b.redditor, -s.score))
    roles['all_by_date'] = sorted(roles['all_by_karma'],
                                  key=lambda (b, s): s.created, reverse=True)
    return roles


def build_html(sorted_roles):
    header = """<html><head><title>All Starcraft 2 Baller post in /r/starcraft</title>
    <script language="javascript">
function toggle(showHideDiv) {
    var ele = document.getElementById(showHideDiv);
    if(ele.style.display == "block") {
            ele.style.display = "none";
    }
    else {
        ele.style.display = "block";
    }
}
</script><body><center>"""
    footer = '</center></body></html>'
    body = ""
    readable_name = {'PG': 'Professional Gamers', 'II': 'Industry Insiders',
                     'CC': 'Casters and Commentators',
                     'all_by_karma': 'everybody sorted by karma',
                     'all_by_name': 'everybody sorted alphabetically',
                     'all_by_date': 'everybody sorted by date'}
    roles_correctly_sorted = ['all_by_karma', 'all_by_name',
                              'all_by_date', 'PG', 'CC', 'II']
    for role in roles_correctly_sorted:
        body += """<div id="headerDiv">Click here to ==>
         <a href="javascript:toggle('con_{0}');" >
         Show/Hide</a> table of {1}
    </div>
    <div style="clear:both;"></div>
    <div id="contentDiv">
        <div id="con_{0}" style="display: {2};">
        <table width=90%% border=1px>
        <tr><td><strong>Reddit name</strong></td><td><strong>Submission</strong></td>
        <td><strong>Karma</strong></td><td><strong>mm-dd-year</strong></td>
        <td><strong>Behind the name</strong></td></tr>
        """.format(role, readable_name[role],
                   "block" if role == 'all_by_karma' else "none")
        for (baller, submission) in sorted_roles[role]:
            body += """<tr><td><a href='{0.redditor_link}' target=_blank>
                    {0.redditor}</a></td><td><a href='{1}'
                    target=_blank>{2}</a>
                    </td><td>{4}</td><td>{3}</td>
                    <td>{0.desc}</td></tr>
                    """.format(baller,
                               submission.permalink.encode('ascii', 'ignore'),
                               submission.title.encode('ascii', 'ignore'),
                               time.strftime("%d-%m-%Y",
                                             time.gmtime(submission.created)),
                               submission.score)
        body += """
         </table>
         </div>
    </div><br /><br />"""
    return header + body + footer


def main():
    APPROVED_USERS_PAGES = ('p9mkj', 'p9mqn', 'qpyfl', 'sshyn')
    ballers = get_ballers(APPROVED_USERS_PAGES)
    paired = build_subs(ballers)
    splitted = split_by_role(paired)
    sorted_roles = sort_pairings_in_roles(splitted)
    output = build_html(sorted_roles)
    with open('created_baller.html', 'w') as out:
        out.write(output)


if __name__ == '__main__':
    r = reddit.Reddit(user_agent="""Starcraft 2 Baller Overview creator by
                                 '/u/_Daimon_""")
    main()
