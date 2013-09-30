# -*- coding: utf-8 -*-

def ask_choice(possible_choices = None):
	"""
	Permits to get a choice between different choices as input
	"""

	choice = None
	ok = False

	while not ok:
		choice = raw_input("> ")

		if (possible_choices is None) or \
		   (choice.lower() in possible_choices):
			ok = True
		else:
			message = "Invalid choice, choose between "
			for c in possible_choices:
				message += c.upper() + " or "
			print message[:-4]

	return choice

def ask_number(bound_min = None, bound_max = None):
	"""
	Ask for a number between bound_min and bound_max
	"""

	choice = None
	ok = False

	while not ok:
		choice_tmp = raw_input("> ")

		try:
			choice = int(choice_tmp)

			if (bound_min is None or choice >= bound_min) and \
					(bound_max is None or choice <= bound_max):
				ok = True
		except ValueError:
			# choice was not a integer
			pass

		if not ok:
			message = "Invalid choice, choose a number"
			if bound_min is not None:
				message += " from %d" % bound_min
			if bound_max is not None:
				message += " to %d" % bound_max

			print message

	return choice

def show_menu():
	"""
	Print game menu
	"""

	print """
=	(P)lay
=	(L)evel easy | medium | hard
=	Local Search (T)ype SA | MC
=	(N)umber of loops
=	(S)ee configuration
=	(Q)uit
	"""

def ask_game():
	"""
	Ask for the game we want to play
	"""

	print """
(1) K-Queens
(2) Graph Coloring
(3) Third game (not yet chosen)
"""
	
	choice = ask_number(1, 3)
	if choice == 1:
		return "k-queens"
	elif choice == 2:
		return "graph-coloring"
	elif choice == 3:
		return "TODO"

	assert(0)

def ask_number_loops(_min, _max):
	"""
	Show a message to ask a number of loops between _min and _max
	"""

	print "Choose a number of loops between %d and %d" % (_min, _max)
	return ask_number(_min, _max)

def show_configuration(local_search_type, level, nb_loops):
	"""
	Print the current configuration
	"""

	if local_search_type == "mc":
		local_search_type = "Min Conflicts"
	elif local_search_type == "sa":
		local_search_type = "Simulated Annealing"
	else:
		assert(0)

	print """Local search type: %s
Level: %s
Number of loops: %d""" \
	% (local_search_type, level, nb_loops)

def show_non_perfect_game(nb_steps):
    print "Out of steps (%d)! We have only a non perfect result..." % nb_steps

def show_perfect_game(nb_steps):
	print "Game has been resolved in %d steps!" % nb_steps
