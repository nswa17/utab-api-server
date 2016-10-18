# -*- coding: utf-8 -*-
import random
import time
import itertools
import threading
import collections
#import inspect#db
from . import interaction_modules
import re
try:
	import readline
except:
	pass
import math
#from .bit_modules import *
from .commandline_modules import *
from .classes import *
from .property_modules import *
from .filter_modules import *
from .select_modules import *
from .io_modules import *

def merge_matchups_and_allocations(matchups, allocations, lattice_list, round_num, tournament, constants_of_adj, teamnum):
	new_allocations = [[], None]
	for grid, lattice in zip(matchups[0], allocations[0]):
		new_lattice = find_lattice_from_lattice_list(lattice_list, grid.teams, lattice.chair)
		new_lattice.panel = lattice.panel
		new_lattice.venue = lattice.venue
		new_allocations[0].append(new_lattice)

	selected_lattice_list_info = return_lattice_list_info(new_allocations[0], tournament, constants_of_adj, round_num, "", teamnum)
	selected_lattice_list_info.allocation_no = 1
	new_allocations[1] = selected_lattice_list_info

	return new_allocations

def import_matchup(filename_matchup, grid_list, tournament, teamnum):
	selected_lattice_list = []
	try:
		raw_data_rows = read_matchup(filename_matchup, teamnum)
	except:
		interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
		raise Exception("error: the matchups to import must be '"+filename_matchup+"'")

	for row in raw_data_rows:
		grid = None
		chair = None
		panels = []
		venue = None
		teams = []
		lattice = None
		for i in range(teamnum):
			for team in tournament["team_list"]:
				if team.name == row[i]:
					teams.append(team)
					break
		if len(teams) != teamnum:
			raise Exception("error: cannot read teams ["+str(row[:teamnum])+"] in matchup")

		for adjudicator in tournament["team_list"]:
			if row[teamnum] == adjudicator.name:
				chair = adjudicator
				break
		else:
			raise Exception("error: cannot read chair ["+row[teamnum]+"] in matchup")

		if row[1+teamnum]:
			for adjudicator in tournament["team_list"]:
				if row[1+teamnum] == adjudicator.name:
					panels.append(adjudicator)
					break
			else:
				raise Exception("error: cannot read panel ["+row[1+teamnum]+"] in matchup")
		if row[2+teamnum]:
			for adjudicator in tournament["team_list"]:
				if row[2+teamnum] == adjudicator.name:
					panels.append(adjudicator)
					break
			else:
				raise Exception("error: cannot read panel ["+row[2+teamnum]+"] in matchup")
		if row[3+teamnum]:
			for venue2 in tournament["venue_list"]:
				if venue2.name == row[3+teamnum]:
					venue = venue2
					break
			else:
				raise Exception("error: cannot read venue ["+row[3+teamnum]+"] in matchup")

		grid = find_grid_from_grid_list(grid_list, teams)
		if grid is None:
			raise Exception("error: failed to create lattice (maybe you have set as absent some team in "+str(teams))
			time.sleep(3)

		lattice = Lattice(grid, chair)
		lattice.panel = panels
		lattice.venue = venue

		selected_lattice_list.append(lattice)

	return selected_lattice_list

def addpriority(grid_list):
	all_len = len(grid_list)
	for p, grid in enumerate(grid_list):
		grid.set_adoptness()
		interaction_modules.progress_bar2(p+1, all_len)
	interaction_modules.progress("")




def add_grid_by_team(grid_list, team_list, team, teamnum):
	team_combinations_list = list(itertools.combinations(team_list, teamnum-1))
	team_combinations_list = map((lambda comb: comb+[team]), team_combinations_list)
	grid_list.extend(create_grids_by_combinations_list(team_combinations_list))

def delete_grid_by_team(grid_list, team):
	def related(grid, team):
		if team in grid.teams:
			return True
		else:
			return False
	#new_grid_list = 
	grid_list = [grid for grid in grid_list if not related(grid, team)]

def create_grids_by_combinations_list(team_combinations_list):
	grid_list = []
	for team_combinations in team_combinations_list:
		team_permutations_list = list(itertools.permutations(team_combinations))
		related_grids = [Grid(list(team_permutations)) for team_permutations in team_permutations_list]
		for grid in related_grids:
			grid.related_grids = related_grids
			if True in [not(team.available) for team in grid.teams]:
				grid.set_not_available()
		grid_list.extend(related_grids)
	return grid_list

def create_grid_list(team_list, teamnum):
	grid_list = []
	flag = False
	cgl(grid_list, team_list, teamnum, flag)
	return grid_list
	"""
	if teamnum == 2:
		grid_list = []
		pair_list = list(itertools.combinations(team_list, 2))
		for pair in pair_list:
			grid1 = Grid([pair[0], pair[1]])
			grid2 = Grid([pair[1], pair[0]])
			grid1.pair_grid = grid2
			grid2.pair_grid = grid1
			grid_list.extend([grid1, grid2])
		for team in team_list:
			grid1 = Grid([team, team])
			grid1.pair_grid = grid1
			grid_list.append(grid1)
		for grid in grid_list:
			if not(grid.teams[0].available) or not(grid.teams[1].available):
				grid.available = False

		return grid_list
	else:
		grid_list = []
		bundle_list = list(itertools.permutations(team_list, 4))
		#for team1 in team_list:
		#	for team2 in team_list:
		#		for team3 in team_list:
		#			for team4 in team_list:
		#				grid_list.append(Grid([team1, team2, team3, team4]))
		len_bundle = len(bundle_list)
		for j, bundle in enumerate(bundle_list):
			interaction_modules.progress_bar2(j+1, len_bundle)
			grid_list.append(Grid(list(bundle)))
		print

		for grid in grid_list:
			if not(grid.teams[0].available) or not(grid.teams[1].available) or not(grid.teams[2].available) or not(grid.teams[3].available):
				grid.available = False

		return grid_list
	"""
	"""
	grid_list = []
	bundle_list = list(itertools.combinations(team_list, teamnum))
	len_bundle = len(bundle_list)
	for j, bundle in enumerate(bundle_list):
		team_lists = list(itertools.permutations(bundle, teamnum))
		interaction_modules.progress_bar2(j+1, len_bundle)
		for team_list_for_grid in team_lists:
			grid_list.append(Grid(list(team_list_for_grid)))
	print

	for grid in grid_list:
		if not(grid.teams[0].available) or not(grid.teams[1].available) or not(grid.teams[2].available) or not(grid.teams[3].available):
			grid.available = False

	return grid_list
	"""



def find_grid_from_grid_list(grid_list, teams):
	for grid in grid_list:
		if grid.teams == teams:
			return grid
	return None


def find_lattice_from_lattice_list(lattice_list, teams, chair):
	for lattice in lattice_list:
		if lattice.grid.teams == teams and lattice.chair == chair:
			return lattice
	return None

def multi(selected_grid_list, selected_grid_lists2):
	for selected_grid_list2 in selected_grid_lists2:
		same = True
		for grid_pair in zip(selected_grid_list, selected_grid_list2):
			if grid_pair[0] != grid_pair[1]:
				same = False
				break
		if same: return True
	return False



def side_revision(grid_list, selected_grid_list):
	selected_grid_list2 = []
	#print [[[t.name for t in g.teams] for g in gl] for gl in selected_grid_lists2]
	if len(grid_list[0].teams) == 2:
		for grid in selected_grid_list:
			if ((grid.teams[0].past_sides.count("gov")-grid.teams[0].past_sides.count("opp")+1) > 0) and ((grid.teams[1].past_sides.count("gov")-grid.teams[1].past_sides.count("opp")-1) < 0):
				selected_grid_list2.extend(list(set(grid.related_grids)-set([grid])))
			else:
				selected_grid_list2.append(grid)

		return selected_grid_list2
	else:
		for grid in selected_grid_list:
			new_grid = grid

			selected_team_list_opening = [t for t in new_grid.teams if is_one_halfed(t, "cg") == -2 or is_one_halfed(t, "co") == -2]
			selected_team_list_closing = [t for t in new_grid.teams if is_one_halfed(t, "og") == 2 or is_one_halfed(t, "oo") == 2]
			selected_team_list_neutral = list(set(new_grid.teams)-set(selected_team_list_opening)-set(selected_team_list_closing))
			selected_team_list_neutral.sort(key=lambda team: sum(team.wins), reverse=True)
			selected_team_list = selected_team_list_opening+selected_team_list_neutral+selected_team_list_closing
			selected_team_list_opening2 = selected_team_list[0:2]
			selected_team_list_closing2 = selected_team_list[2:]
			selected_team_list_opening2.sort(key=lambda team: team.past_sides.count("og")+team.past_sides.count("cg"))
			selected_team_list_closing2.sort(key=lambda team: team.past_sides.count("og")+team.past_sides.count("cg"))
			selected_team_list2 = selected_team_list_opening2+selected_team_list_closing2
			new_grid = find_grid_from_grid_list(grid_list, selected_team_list2)
			#new_grid = better_grid(grid, grid_list)
			#if new_grid != grid: print new_grid, grid
			selected_grid_list2.append(new_grid)

		return selected_grid_list2

def side_revision2(grid_list, selected_grid_list):
	selected_grid_list2 = []
	#print [[[t.name for t in g.teams] for g in gl] for gl in selected_grid_lists2]
	if len(grid_list[0].teams) == 2:
		for grid in selected_grid_list:
			if ((grid.teams[0].past_sides.count("gov")-grid.teams[0].past_sides.count("opp")+1) > 0) and ((grid.teams[1].past_sides.count("gov")-grid.teams[1].past_sides.count("opp")-1) < 0):
				selected_grid_list2.append(list(set(grid.related_grids)-set([grid])))
			else:
				selected_grid_list2.append(grid)

		return selected_grid_list2
	else:
		for grid in selected_grid_list:
			new_grid = grid
			#print [t.name for t in grid.teams]
			#while changable:
			"""
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("og")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("oo")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("og")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
			if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("oo")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("oo")+1) > 0) and ((new_grid.teams[1].past_sides.count("og")-new_grid.teams[1].past_sides.count("oo")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			if ((new_grid.teams[2].past_sides.count("cg")-new_grid.teams[2].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("cg")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			"""
			"""#yaku tatazu
			if is_one_halfed(new_grid.teams[0], "og") == 1 and is_one_halfed(new_grid.teams[3], "co") == -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
			if is_one_halfed(new_grid.teams[2], "cg") == 1 and is_one_halfed(new_grid.teams[3], "co") == -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			if is_one_halfed(new_grid.teams[1], "oo") == 1 and is_one_halfed(new_grid.teams[2], "cg") == -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
			if is_one_halfed(new_grid.teams[0], "og") == 1 and is_one_halfed(new_grid.teams[1], "oo") == -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			if is_one_halfed(new_grid.teams[1], "oo") == 2 and is_one_halfed(new_grid.teams[2], "cg") == -2:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
			if is_one_halfed(new_grid.teams[0], "og") == 2 and is_one_halfed(new_grid.teams[3], "co") == -2:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
			if is_one_halfed(new_grid.teams[1], "oo") == 2 and is_one_halfed(new_grid.teams[3], "co") == -2:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[3], new_grid.teams[2], new_grid.teams[1]])
			if is_one_halfed(new_grid.teams[0], "og") == 2 and is_one_halfed(new_grid.teams[2], "cg") == -2:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[2], new_grid.teams[1], new_grid.teams[0], new_grid.teams[3]])
			"""
			"""
			#unnecessary revision
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("oo")+1) > 0) and ((new_grid.teams[1].past_sides.count("og")-new_grid.teams[1].past_sides.count("oo")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			if ((new_grid.teams[2].past_sides.count("cg")-new_grid.teams[2].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("cg")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("og")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
			if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("oo")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
			if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("oo")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("og")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			"""

			"""
			team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team1_og - team2_oo)*(team1_oo - team2_og) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team3_cg - team4_co)*(team3_co - team4_cg) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team1_og - team4_co)*(team1_co - team4_og) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team2_oo - team3_cg)*(team2_cg - team3_oo) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team1_og - team3_cg)*(team1_cg - team3_og) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[2], new_grid.teams[1], new_grid.teams[0], new_grid.teams[3]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team2_oo - team4_co)*(team2_co - team4_oo) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[3], new_grid.teams[2], new_grid.teams[1]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			"""

			new_grid = better_grid(grid, grid_list)
			#if new_grid != grid: print new_grid, grid
			selected_grid_list2.append(new_grid)

		return selected_grid_list2

def better_grid(grid, grid_list):
	candidate_grid_list = []
	teams = grid.teams
	candidate_team_lists = list(itertools.permutations(teams, 4))
	for candidate_team_list in candidate_team_lists:
		#print candidate_team_list
		candidate_grid_list.append(find_grid_from_grid_list(grid_list, list(candidate_team_list)))
	candidate_grid_list.sort(key=lambda grid: (sum_one_halfed(grid), var4_one_halfed(grid)))
	return candidate_grid_list[0]

def sum_one_halfed(grid):
	return abs(is_one_halfed(grid.teams[0], "og"))+abs(is_one_halfed(grid.teams[1], "oo"))+abs(is_one_halfed(grid.teams[2], "cg"))+abs(is_one_halfed(grid.teams[3], "co"))

def var4_one_halfed(grid):
	avr = (abs(is_one_halfed(grid.teams[0], "og"))+abs(is_one_halfed(grid.teams[1], "oo"))+abs(is_one_halfed(grid.teams[2], "cg"))+abs(is_one_halfed(grid.teams[3], "co")))/4.0
	return (abs(is_one_halfed(grid.teams[0], "og"))-avr)**2+(abs(is_one_halfed(grid.teams[1], "oo"))-avr)**2+(abs(is_one_halfed(grid.teams[2], "cg"))-avr)**2+(abs(is_one_halfed(grid.teams[3], "co"))-avr)**2

def pos(new_grid):
	team1_og = new_grid.teams[0].past_sides.count("og")+1
	team1_oo = new_grid.teams[0].past_sides.count("oo")
	team1_cg = new_grid.teams[0].past_sides.count("cg")
	team1_co = new_grid.teams[0].past_sides.count("co")
	team2_og = new_grid.teams[1].past_sides.count("og")
	team2_oo = new_grid.teams[1].past_sides.count("oo")+1
	team2_cg = new_grid.teams[1].past_sides.count("cg")
	team2_co = new_grid.teams[1].past_sides.count("co")
	team3_og = new_grid.teams[2].past_sides.count("og")
	team3_oo = new_grid.teams[2].past_sides.count("oo")
	team3_cg = new_grid.teams[2].past_sides.count("cg")+1
	team3_co = new_grid.teams[2].past_sides.count("co")
	team4_og = new_grid.teams[3].past_sides.count("og")
	team4_oo = new_grid.teams[3].past_sides.count("oo")
	team4_cg = new_grid.teams[3].past_sides.count("cg")
	team4_co = new_grid.teams[3].past_sides.count("co")+1

	return team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co

def pickup_random(team_buffer, team_list, num, grid_list):
	team_list_cp = list(copy.copy(team_list))
	random.shuffle(team_list_cp)
	return team_list_cp[0:num], team_list_cp[num:]

def pickup_pull_up(team_buffer, team_list, num, grid_list):
	team_list_cp = list(copy.copy(team_list))
	team_list_cp.sort(key=lambda team: sum(team.wins), reverse=True)
	return team_list_cp[0:num], team_list_cp[num:]

def pickup_pull_down(team_buffer, team_list, num, grid_list):
	team_list_cp = list(copy.copy(team_list))
	team_list_cp.sort(key=lambda team: sum(team.wins))
	return team_list_cp[0:num], team_list_cp[num:]

"""
def pickup_adopt(team_buffer, team_list, num, grid_list):
	team_list_cp = list(copy.copy(team_list))
	team_list_cp.sort(key=lambda team: sum(team.wins))
	other_team_lists = list(itertools.combinations(team_list, num))
	candidate_grid_list = []
	for other_team in other_team_lists:
		teams_for_grid_origin = team_buffer+list(other_team)
		teams_for_grid_list = list(itertools.permutations(teams_for_grid_origin, 4))
		for teams_for_grid in teams_for_grid_list:
			candidate_grid_list.append(find_grid_from_grid_list(grid_list, teams_for_grid))
	candidate_grid_list.sort(key=lambda grid: (grid.adoptness1long, grid.adoptness2long), reverse=True)

	return list(set(candidate_grid_list[0].teams)-set(team_buffer))
"""

def divide_team_list_by_4_random(selected_team_list, grid_list):
	selected_team_list_cp = list(copy.copy(selected_team_list))
	random.shuffle(selected_team_list_cp)
	selected_team_lists = list(zip(*[iter(selected_team_list_cp)]*4))
	return [list(ts) for ts in selected_team_lists]

"""
def divide_team_list_by_4_by_adopt(selected_team_list, grid_list):
	candidate_team_lists = list(itertools.permutations(selected_team_list, 4))
	def team_list_adoptness(team_list, grid_list):
		team_4_lists = list(itertools.permutations(selected_team_list, 4))
		adoptness = 0
		for team_4_list in team_4_lists:
			grid = find_grid_from_grid_list(grid_list, list(team_list))
			adoptness += grid.adoptness2long
		return adoptness
	candidate_team_lists.sort(key=lambda team_list: team_list_adoptness(team_list, grid_list))
	return [list(ts) for ts in selected_team_lists]
"""

def divide_team_list_by_4_score(selected_team_list, grid_list):
	selected_team_list_cp = list(copy.copy(selected_team_list))
	selected_team_list_cp.sort(key=lambda team: sum(team.wins), reverse=True)
	selected_team_lists = list(zip(*[iter(selected_team_list_cp)]*4))
	return [list(ts) for ts in selected_team_lists]

def divide_team_list_by_4_half(selected_team_list, grid_list):
	team_lists_by_4 = []
	selected_team_list_cp = list(copy.copy(selected_team_list))
	selected_team_list_opening = [t for t in selected_team_list_cp if is_one_halfed(t, "cg") == -2 or is_one_halfed(t, "co") == -2]
	selected_team_list_closing = [t for t in selected_team_list_cp if is_one_halfed(t, "og") == 2 or is_one_halfed(t, "oo") == 2]
	selected_team_list_opening.sort(key=lambda team: sum(team.wins), reverse=True)
	selected_team_list_closing.sort(key=lambda team: sum(team.wins), reverse=True)
	for i in range(min(int(len(selected_team_list_opening)/2), int(len(selected_team_list_closing)/2))):
		team_lists_by_4.append([selected_team_list_opening[2*i], selected_team_list_opening[2*i+1], selected_team_list_closing[2*i], selected_team_list_closing[2*i+1]])
	rest = list(set(selected_team_list)-set([inner for outer in team_lists_by_4 for inner in outer]))
	rest.sort(key=lambda team: sum(team.wins), reverse=True)
	team_lists_by_4.extend(list(zip(*[iter(selected_team_list_cp)]*4)))
	return [list(ts) for ts in team_lists_by_4]

def decide_position_random(selected_team_list):
	selected_team_list_cp = list(copy.copy(selected_team_list))
	random.shuffle(selected_team_list_cp)
	return selected_team_list_cp

def decide_position_fair(selected_team_list):
	selected_team_lists = list(itertools.permutations(selected_team_list, 4))
	selected_team_lists.sort(key=lambda selected_team_list: abs(is_one_halfed(selected_team_list[0], "og"))+abs(is_one_halfed(selected_team_list[1], "oo"))+abs(is_one_halfed(selected_team_list[2], "cg"))+abs(is_one_halfed(selected_team_list[3], "co")))
	return list(selected_team_lists[0])

def return_selected_grid_list_wudc(grid_list, team_list, pickup, divide_team_list_by_4, decide_position):
	selected_grid_list = []
	team_list_available = [team for team in team_list if team.available]

	random.shuffle(team_list_available)
	team_list_available.sort(key=lambda team: sum(team.wins), reverse=True)

	team_lists_by_same_wins = []
	highest_wins = sum(team_list_available[0].wins)
	team_list_by_same_wins = []
	for team in team_list_available:
		if sum(team.wins) == highest_wins:
			team_list_by_same_wins.append(team)
		else:
			team_lists_by_same_wins.append(list(copy.copy(team_list_by_same_wins)))
			highest_wins = sum(team.wins)
			team_list_by_same_wins = [team]
	team_lists_by_same_wins.append(team_list_by_same_wins)

	selected_team_lists = []
	nowcount = 0
	team_num_for_4division = 0
	teams_buffer = []

	#print [sum(team.wins) for team in team_list_available]

	while nowcount < len(team_lists_by_same_wins):
		#print [t.name for ts in selected_team_lists for t in ts]
		#print [sum(t.wins) for ts in selected_team_lists for t in ts]
		if teams_buffer == []:
			if len(team_lists_by_same_wins[nowcount]) % 4 == 0:
				teams_buffer = team_lists_by_same_wins[nowcount]
				nowcount += 1
				selected_team_lists.append(list(copy.copy(teams_buffer)))
				teams_buffer = []
				team_num_for_4division = 0
				#print "called4"
			else:
				team_num_for_4division = 4 - len(team_lists_by_same_wins[nowcount]) % 4
				teams_buffer = team_lists_by_same_wins[nowcount]
				nowcount += 1
				#print [t.name for t in teams_buffer]
				#print team_num_for_4division
				#print "called3"
		else:
			if len(team_lists_by_same_wins[nowcount]) == team_num_for_4division:
				"""
				picked_up_teams, rest = pickup(team_lists_by_same_wins[nowcount], team_num_for_4division)
				
				
				teams_buffer.extend(picked_up_teams)
				"""
				#print [t.name for t in picked_up_teams]
				#print [t.name for t in rest]
				teams_buffer.extend(team_lists_by_same_wins[nowcount])
				nowcount += 1
				selected_team_lists.append(list(copy.copy(teams_buffer)))
				teams_buffer = []
				#print "called"
				team_num_for_4division = 0
			elif len(team_lists_by_same_wins[nowcount]) > team_num_for_4division:
				#print "called1"
				picked_up_teams, rest = pickup(teams_buffer, team_lists_by_same_wins[nowcount], team_num_for_4division, grid_list)
				teams_buffer.extend(picked_up_teams)
				team_lists_by_same_wins[nowcount] = rest
				selected_team_lists.append(list(copy.copy(teams_buffer)))
				teams_buffer = []
				team_num_for_4division = 0
			else:
				#print "called2"
				#print team_num_for_4division
				team_num_for_4division -= len(team_lists_by_same_wins[nowcount])
				#print team_num_for_4division
				teams_buffer.extend(team_lists_by_same_wins[nowcount])
				nowcount += 1
				#print team_num_for_4division
				#print [t.name for t in teams_buffer]
		#print [t.name for t in teams_buffer]
		#print [[t.name for t in ts] for ts in team_lists_by_same_wins]
		#print [[t.name for t in ts] for ts in selected_team_lists]

	selected_team_lists = [list(selected_team_list) for selected_team_list in selected_team_lists]

	selected_team_lists2 = []
	for selected_team_list in selected_team_lists:
		if len(selected_team_list) / 4 != 1:
			team_lists = divide_team_list_by_4(selected_team_list, grid_list)
			selected_team_lists2.extend(team_lists)
		else:
			selected_team_lists2.append(selected_team_list)

	selected_team_lists3 = []
	for selected_team_list in selected_team_lists2:
		selected_team_lists3.append(decide_position(selected_team_list))

	if len(selected_team_lists3[-1]) != 4:
		selected_team_lists3.pop()

	for selected_team_list in selected_team_lists3:
		#print selected_team_list
		selected_grid_list.append(find_grid_from_grid_list(grid_list, selected_team_list))

	return selected_grid_list

def revise_selected_grid_list(selected_grid_list, grid_list):
	selected_grid_list2 = []
	many_gov_teams = []
	many_opp_teams = []
	for grid in selected_grid_list:
		if is_one_sided(grid.teams[0], "gov", 2) > 0: many_gov_teams.append(grid.teams[0])
		if is_one_sided(grid.teams[1], "opp", 2) < 0: many_opp_teams.append(grid.teams[1])

	for i in range(len(selected_grid_list)):
		grid = selected_grid_list[i]
		team_0_i = selected_grid_list[i].teams[0]
		team_1_i = selected_grid_list[i].teams[1]
		if i == len(selected_grid_list)-1:
			selected_grid_list2.append(grid)
			break
		team_0_in = selected_grid_list[i+1].teams[0]
		team_1_in = selected_grid_list[i+1].teams[1]
		if team_0_i in many_gov_teams and team_1_i in many_opp_teams:
			selected_grid_list2.append(find_grid_from_grid_list(grid_list, [team_1_i, team_0_i]))
		elif team_0_i in many_gov_teams and team_1_in in many_opp_teams:
			selected_grid_list2.extend([find_grid_from_grid_list(grid_list, [team_1_in, team_0_i]), find_grid_from_grid_list(grid_list, [team_0_in, team_1_i])])
		elif team_0_in in many_gov_teams and team_1_i in many_opp_teams:
			selected_grid_list2.extend([find_grid_from_grid_list(grid_list, [team_1_i, team_0_in]), find_grid_from_grid_list(grid_list, [team_0_i, team_1_in])])
		else:
			selected_grid_list2.append(grid)
	return selected_grid_list2
	"""
	for grid in selected_grid_list_cp:
		if is_one_sided(grid.teams[0], True) > 0:
			if is_one_sided(selected_grid_list[selected_grid_list.index(grid)].teams[1], False) < 0:
				new_grid = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1]])
				selected_grid_list.insert()
				selected_grid_list.remove(grid)
			elif is_one_sided(selected_grid_list[selected_grid_list.index(grid)+1].teams[1], False) < 0:
				new_grid = find_grid_from_grid_list(grid_list, [grid.teams[0], selected_grid_list[selected_grid_list.index(grid)+1].teams[1]])
	"""

def refresh_grids(grid_list):
	for grid in grid_list:
		grid.initialize()

def exchange_teams(grid_list, matchups, team_a, team_b):
	if len(matchups[0].teams) == 2:
		for i, grid in enumerate(matchups):
			if grid.teams[0] == team_a and grid.teams[1] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_b, team_a])
				#grid.teams[0], grid.teams[1] = 
				break
			elif grid.teams[1] == team_a and grid.teams[0] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_a, team_b])
				break
			else:
				if grid.teams[0] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [team_b, grid.teams[1]])
				elif grid.teams[1] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_a])
				elif grid.teams[1] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_b])
				elif grid.teams[0] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [team_a, grid.teams[1]])
	else:
		for i, grid in enumerate(matchups):
			if grid.teams[0] == team_a and grid.teams[1] == team_b:
				#grid.teams[0], grid.teams[1] = team_b, team_a
				matchups[i] = find_grid_from_grid_list(grid_list, [team_b, team_a, grid.teams[2], grid.teams[3]])
				break
			elif grid.teams[0] == team_a and grid.teams[2] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_b, grid.teams[1], team_a, grid.teams[3]])
				break
			elif grid.teams[0] == team_a and grid.teams[3] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_b, grid.teams[1], grid.teams[2], team_a])
				break
			elif grid.teams[1] == team_a and grid.teams[0] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_a, team_b, grid.teams[2], grid.teams[3]])
				break
			elif grid.teams[1] == team_a and grid.teams[2] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_b, team_a, grid.teams[3]])
				break
			elif grid.teams[1] == team_a and grid.teams[3] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_b, grid.teams[2], team_a])
				break
			elif grid.teams[2] == team_a and grid.teams[0] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_a, grid.teams[1], team_b, grid.teams[3]])
				break
			elif grid.teams[2] == team_a and grid.teams[1] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_a, team_b, grid.teams[3]])
				break
			elif grid.teams[2] == team_a and grid.teams[3] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], team_b, team_a])
				break
			elif grid.teams[3] == team_a and grid.teams[0] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_a, grid.teams[1], grid.teams[2], team_b])
				break
			elif grid.teams[3] == team_a and grid.teams[1] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_a, grid.teams[2], team_b])
				break
			elif grid.teams[3] == team_a and grid.teams[2] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], team_a, team_b])
				break
			else:
				if grid.teams[0] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [team_b, grid.teams[1], grid.teams[2], grid.teams[3]])
				elif grid.teams[1] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_b, grid.teams[2], grid.teams[3]])
				elif grid.teams[2] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], team_b, grid.teams[3]])
				elif grid.teams[3] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], grid.teams[2], team_b])
				elif grid.teams[0] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [team_a, grid.teams[1], grid.teams[2], grid.teams[3]])
				elif grid.teams[1] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_a, grid.teams[2], grid.teams[3]])
				elif grid.teams[2] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], team_a, grid.teams[3]])
				elif grid.teams[3] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], grid.teams[2], team_a])

def exchange_adj(allocations, adjudicator1, adjudicator2):
	for lattice in allocations[0]:
		if len(lattice.panel) == 2:
			if lattice.panel[0] == adjudicator1:
				lattice.panel[0] = adjudicator2
			elif lattice.panel[0] == adjudicator2:
				lattice.panel[0] = adjudicator1
			if lattice.panel[1] == adjudicator2:
				lattice.panel[1] = adjudicator1
			elif lattice.panel[1] == adjudicator1:
				lattice.panel[1] = adjudicator2
		elif len(lattice.panel) == 1:
			if lattice.panel[0] == adjudicator1:
				lattice.panel[0] = adjudicator2
			elif lattice.panel[0] == adjudicator2:
				lattice.panel[0] = adjudicator1

	for lattice in allocations[0]:
		if lattice.chair == adjudicator1:
			lattice.chair = adjudicator2
		elif lattice.chair == adjudicator2:
			lattice.chair = adjudicator1

def delete_adj(allocations, panel):
	for lattice in allocations[0]:
		if len(lattice.panel) == 2:
			if lattice.panel[0] == panel:
				lattice.panel.pop(0)
			elif lattice.panel[1] == panel:
				lattice.panel.pop(1)
		elif len(lattice.panel) == 1:
			if lattice.panel[0] == panel:
				lattice.panel.pop(0)

def add_adj(allocations, chair, panel):
	for lattice in allocations[0]:
		if len(lattice.panel) < 2 and lattice.chair.name == chair:
			lattice.panel.append(panel)
			break
	else:
		interaction_modules.warn("please write a valid chair name")


def cmp_allocations(allocations1, allocations2):
	for lattice1 in allocations1:
		for lattice2 in allocations2:
			if lattice1.teams == lattice2.teams:
				if lattice1.chair != lattice2.chair:
					return False
				else:
					break
		else:
			return False
	return True




pass