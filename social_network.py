# Name: Yu-Shou(Joshua) Chen
# CSE 160
# Homework 5

import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

###
#  Problem 1a
###

practice_graph = nx.Graph()

practice_graph.add_edge("A", "B")
practice_graph.add_edge("A", "C")
practice_graph.add_edge("B", "C")
practice_graph.add_edge("D", "B")
practice_graph.add_edge("F", "D")
practice_graph.add_edge("E", "D")
practice_graph.add_edge("C", "D")
practice_graph.add_edge("C", "F")


def draw_practice_graph(graph):
    """Draw practice_graph to the screen.
    """
    nx.draw_networkx(graph)
    plt.show()


# Comment out this line after you have visually verified your practice graph.
# Otherwise, the picture will pop up every time that you run your program.
# draw_practice_graph(practice_graph)


###
#  Problem 1b
###

rj = nx.Graph()
rj.add_edge("Nurse", "Juliet")
rj.add_edge("Tybalt", "Juliet")
rj.add_edge("Capulet", "Juliet")
rj.add_edge("Friar Laurence", "Juliet")
rj.add_edge("Romeo", "Juliet")
rj.add_edge("Tybalt", "Capulet")
rj.add_edge("Friar Laurence", "Romeo")
rj.add_edge("Romeo", "Benvolio")
rj.add_edge("Romeo", "Montague")
rj.add_edge("Romeo", "Mercutio")
rj.add_edge("Benvolio", "Montague")
rj.add_edge("Capulet", "Escalus")
rj.add_edge("Capulet", "Paris")
rj.add_edge("Montague", "Escalus")
rj.add_edge("Escalus", "Paris")
rj.add_edge("Escalus", "Mercutio")
rj.add_edge("Mercutio", "Paris")


def draw_rj(graph):
    """Draw the rj graph to the screen and to a file.
    """
    nx.draw_networkx(graph)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()


# Comment out this line after you have visually verified your rj graph and
# created your PDF file.
# Otherwise, the picture will pop up every time that you run your program.
# draw_rj(rj)


###
#  Problem 2
###

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    # This function has already been implemented for you.
    # You do not need to add any more code to this (short!) function.
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Find and return the friends of friends of the given user.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a set containing the names of all of the friends of
    friends of the user. The set should not contain the user itself
    or their immediate friends.
    """
    broad_set = set()
    for friend in friends(graph, user):
        broad_set = broad_set | set(graph.neighbors(friend))
    without_friend_set = broad_set - set(graph.neighbors(user))
    fd_of_fd_set = without_friend_set - set([user])
    return fd_of_fd_set


def common_friends(graph, user1, user2):
    """Finds and returns the set of friends that user1 and user2 have in common.

    Arguments:
        graph:  the graph object that contains the users
        user1: a string representing one user
        user2: a string representing another user

    Returns: a set containing the friends user1 and user2 have in common
    """
    return set(friends(graph, user1)) & set(friends(graph, user2))


def number_of_common_friends_map(graph, user):
    """Returns a map (a dictionary), mapping a person to the number of friends
    that person has in common with the given user. The map keys are the
    people who have at least one friend in common with the given user,
    and are neither the given user nor one of the given user's friends.
    Example: a graph called my_graph and user "X"
    Here is what is relevant about my_graph:
        - "X" and "Y" have two friends in common
        - "X" and "Z" have one friend in common
        - "X" and "W" have one friend in common
        - "X" and "V" have no friends in common
        - "X" is friends with "W" (but not with "Y" or "Z")
    Here is what should be returned:
      number_of_common_friends_map(my_graph, "X")  =>   { 'Y':2, 'Z':1 }

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a dictionary mapping each person to the number of (non-zero)
    friends they have in common with the user
    """
    cmn_fd_map = {}
    for fd_of_fd in friends_of_friends(graph, user):
        count = len(common_friends(graph, fd_of_fd, user))
        cmn_fd_map[fd_of_fd] = count
    return cmn_fd_map


def number_map_to_sorted_list(map_with_number_vals):
    """Given a dictionary, return a list of the keys in the dictionary.
    The keys are sorted by the number value they map to, from greatest
    number down to smallest number.
    When two keys map to the same number value, the keys are sorted by their
    natural sort order for whatever type the key is, from least to greatest.

    Arguments:
        map_with_number_vals: a dictionary whose values are numbers

    Returns: a list of keys, sorted by the values in map_with_number_vals
    """
    key_lst = []
    sorted_byname = sorted(map_with_number_vals.items())
    sorted_lst = sorted(sorted_byname, key=itemgetter(1), reverse=True)
    for item in sorted_lst:
        key_lst.append(itemgetter(0)(item))
    return key_lst


def recommend_by_number_of_common_friends(graph, user):
    """
    Returns a list of friend recommendations for the user, sorted
    by number of friends in common.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: A list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the number of common friends (people
    with the most common friends are listed first).  In the
    case of a tie in number of common friends, the names/IDs are
    sorted by their natural sort order, from least to greatest.
    """

    return number_map_to_sorted_list(number_of_common_friends_map(graph, user))


###
#  Problem 3
###

def influence_map(graph, user):
    """Returns a map (a dictionary) mapping from each person to their
    influence score, with respect to the given user. The map only
    contains people who have at least one friend in common with the given
    user and are neither the user nor one of the users's friends.
    See the assignment writeup for the definition of influence scores.
    """
    influence_mp = {}
    for fd_of_fd in friends_of_friends(graph, user):
        point_sum = 0
        for cmn_fd in common_friends(graph, fd_of_fd, user):
            influence_point = 1 / len(list(graph.neighbors(cmn_fd)))
            point_sum += influence_point
        influence_mp[fd_of_fd] = point_sum
    return influence_mp


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the influence score (people
    with the biggest influence score are listed first).  In the
    case of a tie in influence score, the names/IDs are sorted
    by their natural sort order, from least to greatest.
    """
    return number_map_to_sorted_list(influence_map(graph, user))


###
#  Problem 4
###

print("Problem 4:")
print()
unchanged_lst = []
changed_lst = []
for name in rj:
    if recommend_by_number_of_common_friends(rj, name) == \
            recommend_by_influence(rj, name):
        unchanged_lst.append(name)
    else:
        changed_lst.append(name)
print("Unchanged Recommendations:", sorted(unchanged_lst))
print("Changed Recommendations:", sorted(changed_lst))


###
#  Problem 5
###

facebook = nx.Graph()
myfile = open("facebook-links.txt", "r")
for identity in myfile:
    id_list = identity.split()
    facebook.add_edge(int(id_list[0]), int(id_list[1]))
myfile.close()


# assert len(facebook.nodes()) == 63731
# assert len(facebook.edges()) == 817090

###
#  Problem 6
###
print()
print("Problem 6:")
print()


def sorted_list(graph):
    userid_list = []
    for user in graph:
        userid_list.append(user)
    sorted_user_list = sorted(userid_list)
    return sorted_user_list


for userid in sorted_list(facebook):
    if userid >= 1000 and userid % 1000 == 0:
        recommend = recommend_by_number_of_common_friends(facebook, userid)
        if len(recommend) > 10:
            print(userid, "(by number_of_common_friends):",
                  recommend[0:10])
        else:
            print(userid, "(by number_of_common_friends):", recommend)


###
#  Problem 7
###
print()
print("Problem 7:")
print()

for userid in sorted_list(facebook):
    if userid >= 1000 and userid % 1000 == 0:
        recommend = recommend_by_influence(facebook, userid)
        if len(recommend) > 10:
            print(userid, "(by influence):", recommend[0:10])
        else:
            print(userid, "(by influence):", recommend)


###
#  Problem 8
###
print()
print("Problem 8:")
print()

sum_of_unchanged = 0
sum_of_changed = 0
for userid in sorted_list(facebook):
    if userid >= 1000 and userid % 1000 == 0:
        recommend_cmn_friend = recommend_by_number_of_common_friends(facebook,
                                                                     userid)
        recommend_influence = recommend_by_influence(facebook, userid)
        if recommend_cmn_friend == recommend_influence:
            sum_of_unchanged += 1
        else:
            sum_of_changed += 1

print("Same:", sum_of_unchanged)
print("Different:", sum_of_changed)

###
#  Collaboration
###

# No one help me.
