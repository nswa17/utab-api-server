# -*- coding: utf-8 -*-
import os
import sys
import random
import time
import itertools
import threading
import collections
import re
path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

import math
from error.error_classes import *
from .property import *
from .filter import *
from .select import *
from .grid_classes import *



def evaluate_adjudicator(adjudicator_list, judge_criterion):
	for adjudicator in adjudicator_list:
		adjudicator.evaluation = 0
		adjudicator.evaluation += adjudicator.reputation * judge_criterion[adjudicator.active_num]["judge_repu_percent"]/100.0
		adjudicator.evaluation += adjudicator.judge_test * judge_criterion[adjudicator.active_num]["judge_test_percent"]/100.0

		if adjudicator.active_num != 0:
			adjudicator.evaluation += sum(adjudicator.scores) / adjudicator.active_num * judge_criterion[adjudicator.active_num]["judge_perf_percent"]/100.0

def sort_adjudicator_list_by_score(adjudicator_list):
	adjudicator_list.sort(key=lambda adjudicator: adjudicator.evaluation, reverse=True)
	for rank, adjudicator in enumerate(adjudicator_list):
		adjudicator.ranking = rank+1

def sort_team_list_by_score(team_list):
	team_list.sort(key=lambda team: (sum(team.wins), sum(team.scores), (team.margin)), reverse=True)
	for j, team in enumerate(team_list):
		team.ranking = j + 1

def create_grid_list_by_thread(grid_list, team_list, team_num, flag):
	try:
		t = threading.Thread(target=cgl, args=(grid_list, team_list, team_num, flag))
		#t.setDaemon(True)#db
		t.start()
	except:
		interaction_modules.warn("couldn't start the sub thread")
		cgl(grid_list, team_list, team_num, flag)
	refresh_grids_for_adopt(grid_list)

def cgl(grid_list, team_list, team_num, flag):
	team_combinations_list = list(itertools.combinations(team_list, team_num))
	grid_list.extend(create_grids_by_combinations_list(team_combinations_list))
	try:
		flag.set()
	except:
		pass

def create_matchups(grid_list, round_num, tournament, filter_list, team_num):
	#interaction_modules.progress("[creating matchups for round "+str(round_num)+"]")
	#interaction_modules.progress("filtering grid list")
	filtration(grid_list, round_num, tournament, filter_list)
	#interaction_modules.progress("adding priority to grids")
	addpriority(grid_list)
	#show_adoptness1(grid_list, team_list)
	#print
	#show_adoptness2(grid_list, team_list)
	#interaction_modules.progress("selecting grids")
	selected_grid_lists = return_selected_grid_lists(grid_list, round_num, tournament)

	for k, selected_grid_list in enumerate(selected_grid_lists):
	#	export_matchups(selected_grid_list[0], str(k)+"team", round_num, workfolder_name)
		selected_grid_list.matchups_no = k+1

	return selected_grid_lists

def filtration(grid_list, round_num, tournament, filter_list):#max_filters = 20
	#for i in range(9):
	#	filter1(grid_list, i)
	#function_list = [power_pairing, prevent_same_institution_small, prevent_same_opponent, prevent_same_institution_middle, prevent_unfair_side, prevent_same_institution_large, random_pairing]
	all_len = len(grid_list)
	if all_len > 4:
		divided_grid_list_list = [grid_list[:int(all_len/4)], grid_list[int(all_len/4):int(all_len*2/4)], grid_list[int(all_len*2/4):int(all_len*3/4)], grid_list[int(all_len*3/4):]]
	else:
		divided_grid_list_list = [grid_list]
	es = [threading.Event() for i in range(len(divided_grid_list_list))]
	#random.shuffle(function_list)
	
	def func_wrapper(func):
		def func2(i, *args):
			func(*args)
			es[i].set()
		return func2

	for i, divided_grid_list in enumerate(divided_grid_list_list):
		for k, function in enumerate(filter_list):
			#interaction_modules.progress_bar2(k+1, len(function_list))
			function2 = func_wrapper(function)
			t = threading.Thread(target=function2, args=(i, divided_grid_list, round_num, tournament.team_list, k))
			t.setDaemon(True)
			t.start()
			#print str(function)#passpass
			#show_adoptbits(team_list, grid_list, k)
			#print
			#show_adoptbitslong(team_list, grid_list, k)
		#interaction_modules.progress("")

	while True:
		if False not in [e.isSet() for e in es]:
			break
		else:
			time.sleep(0.5)

def multi(selected_grid_list, selected_grid_lists2):
	for selected_grid_list2 in selected_grid_lists2:
		same = True
		for grid_pair in zip(selected_grid_list, selected_grid_list2):
			if grid_pair[0] != grid_pair[1]:
				same = False
				break
		if same: return True
	return False

def lattice_filtration(tournament, selected_grid_list, lattice_list, round_num, filter_list):#max_filters = 20
	#for i in range(9):
	#	filter1(grid_list, i)
	#function_list = [random_allocation, prevent_str_wek_round, prevent_unfair_adjudicators, prevent_conflicts, avoid_watched_teams, prioritize_bubble_round]
	
	for k, function in enumerate(filter_list):
		#interaction_modules.progress_bar2(k+1, len(function_list))
		function(round_num, tournament, selected_grid_list, lattice_list, k)
		#show_adoptbits_lattice(adjudicator_list, lattice_list, k)
		#print
		#show_adoptbitslong_lattice(adjudicator_list, lattice_list, k)
	#interaction_modules.progress("")

def create_allocations(tournament, selected_grid_list, lattice_list, round_num, filter_list):
	#interaction_modules.progress("[creating allocations for round "+str(round_num)+"]")
	#interaction_modules.progress("filtering lattice list")
	lattice_filtration(tournament, selected_grid_list, lattice_list, round_num, filter_list)
	#interaction_modules.progress("adding priority to grids")
	addpriority(lattice_list)
	#show_adoptness1(grid_list, team_list)
	#print
	#show_adoptness2(grid_list, team_list)
	#interaction_modules.progress("selecting lattices")
	selected_lattice_lists = return_selected_lattice_lists(lattice_list, round_num, tournament)
	for k, selected_lattice_list in enumerate(selected_lattice_lists):
		#export_allocations(selected_lattice_list_with_info[0], str(k)+"adj", round_num, workfolder_name)
		selected_lattice_list.allocation_no = k+1

	return selected_lattice_lists

def addpriority(grid_list):
	all_len = len(grid_list)
	for p, grid in enumerate(grid_list):
		grid.set_adoptness()
		#interaction_modules.progress_bar2(p+1, all_len)
	#interaction_modules.progress("")

def return_selected_lattice_lists(lattice_list, round_num, tournament):
	alg_list = [select_alg_adj2, select_alg_adj11, select_alg_adj13, select_alg_adj14]
	selected_lattice_lists = []

	cp1_small = lambda g: g.adoptness1
	cp2_small = lambda g: g.adoptness2
	cp1_strict = lambda g: g.adoptness_strict1
	cp2_strict = lambda g: g.adoptness_strict2
	cp1_long = lambda g: g.adoptness1long
	cp2_long = lambda g: g.adoptness2long
	cp1_weight = lambda g: g.adoptness_weight1
	cp2_weight = lambda g: g.adoptness_weight2

	cp_pair_list = [(cp1_small, cp2_small), (cp2_small, cp1_small), (cp1_long, cp2_long), (cp2_long, cp1_long), (cp1_strict, cp2_strict), (cp2_strict, cp1_strict), (cp1_weight, cp2_weight), (cp2_weight, cp1_weight)]


	entire_length = len(alg_list) * len(cp_pair_list)
	c = 1

	def wrap(alg):
		def new_alg(es, selected_lattice_lists, pid, *args):
			selected_lattice_lists[pid] = alg(pid, *args)
			if len(selected_lattice_lists[pid]) != 25:
				selected_lattice_lists[pid].internal_algorithm = "pid:"+str(pid)+", alg:"+str(alg.__name__)#db
				#interaction_modules.warn("pid:"+str(pid)+", alg:"+str(alg.__name__))#db
			es[pid].set()
		return new_alg

	#threads = []
	new_selected_lattice_lists = [Lattice_list() for i in range(len(alg_list)*len(cp_pair_list))]
	es = [threading.Event() for i in range(len(alg_list)*len(cp_pair_list))]
	for i, cp_pair in enumerate(cp_pair_list):
		for j, alg in enumerate(alg_list):
			alg_wrapped = wrap(alg)
			#interaction_modules.warn(str(i*len(alg_list)+j))
			t = threading.Thread(target=alg_wrapped, args=(es, new_selected_lattice_lists, i*len(alg_list)+j, lattice_list, round_num, tournament.adjudicator_list, cp_pair))
			t.setDaemon(True)
			t.start()
			#if i == 0 and j == 0: t.start()

	while True:
		if False not in [e.isSet() for e in es]:
			selected_lattice_lists.extend(new_selected_lattice_lists)
			break
		else:
			#interaction_modules.progress_bar2([e.isSet() for e in es].count(True), entire_length)
			time.sleep(0.5)

	"""
	#db
	for i, cp_pair in enumerate(cp_pair_list):
		for j, alg in enumerate(alg_list):
			interaction_modules.progress_bar2(c, entire_length)
			c+=1
			selected_lattice_lists.append(alg(i*len(alg_list)+j, lattice_list, round_num, tournament["adjudicator_list"], cp_pair))
	"""

	#interaction_modules.progress("")

	for selected_lattice_list in selected_lattice_lists:
		#if len(selected_lattice_list) == 19: interaction_modules.warn("warn")#db
		selected_lattice_list.sort(key=lambda lattice: lattice.__hash__())

	selected_lattice_lists2 = []
	for selected_lattice_list in selected_lattice_lists:
		if selected_lattice_list not in selected_lattice_lists2:
			selected_lattice_lists2.append(selected_lattice_list)

	for selected_lattice_list in selected_lattice_lists2:
		add_lattice_list_info(selected_lattice_list, tournament, round_num, "")

	selected_lattice_lists2.sort(key=lambda selected_lattice_list: selected_lattice_list.strong_strong_indicator, reverse=True)
			
	return selected_lattice_lists2

def add_lattice_list_info(selected_lattice_list, tournament, round_num, comment):
	lattice_list_checks(selected_lattice_list, tournament.rounds[round_num-1].constants_of_adj, round_num)
	errors = lattice_list_errors(selected_lattice_list, tournament, round_num)
	selected_lattice_list.large_warnings.extend(errors)
	for lattice in selected_lattice_list:
		for warn in lattice.warnings:
			selected_lattice_list.large_warnings.append(warn.longwarning())
	selected_lattice_list.large_warnings.sort()
	selected_lattice_list.large_warnings.sort()
	selected_lattice_list.strong_strong_indicator = calc_str_str_indicator(selected_lattice_list, tournament.style["team_num"])
	selected_lattice_list.num_of_warnings = calc_num_of_warnings(selected_lattice_list)
	selected_lattice_list.comment = comment

def lattice_list_errors(selected_lattice_list, tournament, round_num):
	large_warnings = []
	multi2 = {adjudicator.name:0 for adjudicator in tournament.adjudicator_list}

	for lattice in selected_lattice_list:
		multi2[lattice.chair.name] += 1
		if len(lattice.panel) == 2:
			multi2[lattice.panel[0].name] += 1
			multi2[lattice.panel[1].name] += 1
		elif len(lattice.panel) == 1:
			multi2[lattice.panel[0].name] += 1

	for k, v in list(multi2.items()):
		if v > 1:
			large_warnings.append("error : an adjudicator appears more than two times :"+str(k)+": "+str(v))
		elif v == 0:
			condemned_adjudicator = None
			for adjudicator in tournament.adjudicator_list:
				if adjudicator.name == k:
					condemned_adjudicator = adjudicator
					break
			if not condemned_adjudicator.absent:
				large_warnings.append("warning : an adjudicator does not exist in matchups :"+str(k))
			else:
				large_warnings.append("attention : an adjudicator is absent :"+str(k))

	multi3 = {grid:0 for grid in [lattice.grid for lattice in selected_lattice_list]}

	for lattice in selected_lattice_list:
		multi3[lattice.grid] += 1

	for k, v in list(multi3.items()):
		if v > 1:
			large_warnings.append("error : a grid appears more than two times :"+str(k)+": "+str(v))
			#large_warnings.append(str(sorted([adj.code for adj in tournament["adjudicator_list"]])))

	max_active_num = 0
	for adjudicator in tournament.adjudicator_list:
		if adjudicator.active_num > max_active_num:
			max_active_num = adjudicator.active_num
	next_active_adjudicators = []
	for lattice in selected_lattice_list:
		next_active_adjudicators.append(lattice.chair)
		next_active_adjudicators += lattice.panel

	for adjudicator in next_active_adjudicators:
		if adjudicator.active_num > max_active_num-1:
			max_active_num = adjudicator.active_num+1

	for adjudicator in tournament.adjudicator_list:
		if (adjudicator not in next_active_adjudicators) and ((max_active_num - adjudicator.active_num) > 0) and not(adjudicator.absent):
				large_warnings.append("warning : an adjudicator does nothing :{0:20s}, {1}".format(adjudicator.name, adjudicator.active_num))

	if round_num > 0:
		for adjudicator in tournament.adjudicator_list:
			if adjudicator.active_num_as_chair == 0:
				large_warnings.append("warning : a judge hasn't experienced a chair yet :"+str(adjudicator.name))
	return large_warnings

def lattice_list_checks(lattice_list, constants_of_adj, round_num):
	for lattice in lattice_list:
		lattice.warnings = []
		lattice.large_warnings = []
	lattice_check_conflict(lattice_list)
	lattice_check_bubble_round(lattice_list, constants_of_adj, round_num)
	lattice_check_same_round(lattice_list)

def lattice_check_conflict(lattice_list):
	if len(lattice_list[0].grid.teams) == 2:
		for i, lattice in enumerate(lattice_list):
			conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.chair.institutions)
			conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.chair.institutions)

			if list(conflicting_insti1 | conflicting_insti2):
				lattice.warnings.append(InstitutionConflict(lattice.chair, lattice.grid.teams))
			if lattice.grid.teams[0].name in lattice.chair.conflict_teams or lattice.grid.teams[1].name in lattice.chair.conflict_teams:
				lattice.warnings.append(PersonalConflict(lattice.chair, lattice.grid.teams))

			if len(lattice.panel) == 2:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.warnings.append(InstitutionConflict(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[0], lattice.grid.teams))
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[1].institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.warnings.append(InstitutionConflict(lattice.panel[1], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[1].conflict_teams or lattice.grid.teams[1].name in lattice.panel[1].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[1], lattice.grid.teams))
			elif len(lattice.panel) == 1:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.warnings.append(InstitutionConflict(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[0], lattice.grid.teams))
	else:
		for i, lattice in enumerate(lattice_list):
			conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.chair.institutions)
			conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.chair.institutions)
			conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.chair.institutions)
			conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.chair.institutions)

			if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
				lattice.warnings.append(InstitutionConflict(lattice.chair, lattice.grid.teams))
			if lattice.grid.teams[0].name in lattice.chair.conflict_teams or lattice.grid.teams[1].name in lattice.chair.conflict_teams or lattice.grid.teams[2].name in lattice.chair.conflict_teams or lattice.grid.teams[3].name in lattice.chair.conflict_teams:
				lattice.warnings.append(PersonalConflict(lattice.chair, lattice.grid.teams))

			if len(lattice.panel) == 2:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
					lattice.warnings.append(InstitutionConflict(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams or lattice.grid.teams[2].name in lattice.panel[0].conflict_teams or lattice.grid.teams[3].name in lattice.panel[0].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[0], lattice.grid.teams))
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.panel[1].institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
					lattice.warnings.append(InstitutionConflict(lattice.panel[1], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[1].conflict_teams or lattice.grid.teams[1].name in lattice.panel[1].conflict_teams or lattice.grid.teams[2].name in lattice.panel[1].conflict_teams or lattice.grid.teams[3].name in lattice.panel[1].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[1], lattice.grid.teams))
			elif len(lattice.panel) == 1:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
					lattice.warnings.append(InstitutionConflict(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams or lattice.grid.teams[2].name in lattice.panel[0].conflict_teams or lattice.grid.teams[3].name in lattice.panel[0].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[0], lattice.grid.teams))

def lattice_check_bubble_round(lattice_list, constants_of_adj, round_num):
	if len(lattice_list[0].grid.teams) == 2:
		for i, lattice in enumerate(lattice_list):
			if constants_of_adj["des_priori_bubble"] != 0:
				if lattice.grid.bubble < 5:
					lattice.warnings.append(BubbleRound(lattice.grid.teams))
		
	else:
		for i, lattice in enumerate(lattice_list):
			if constants_of_adj["des_priori_bubble"] != 0:
				if lattice.grid.bubble < 5:
					lattice.warnings.append(BubbleRound(lattice.grid.teams))
		
def lattice_check_same_round(lattice_list):
	if len(lattice_list[0].grid.teams) == 2:
		for i, lattice in enumerate(lattice_list):
			if lattice.grid.teams[0] in lattice.chair.watched_teams or lattice.grid.teams[1] in lattice.chair.watched_teams:
				lattice.warnings.append(WatchingAgain(lattice.chair, lattice.grid.teams))
			if len(lattice.panel) == 2:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0] in lattice.panel[1].watched_teams or lattice.grid.teams[1] in lattice.panel[1].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[1], lattice.grid.teams))
			elif len(lattice.panel) == 1:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[0], lattice.grid.teams))
	else:
		for i, lattice in enumerate(lattice_list):
			if lattice.grid.teams[0] in lattice.chair.watched_teams or lattice.grid.teams[1] in lattice.chair.watched_teams or lattice.grid.teams[2] in lattice.chair.watched_teams or lattice.grid.teams[3] in lattice.chair.watched_teams:
				lattice.warnings.append(WatchingAgain(lattice.chair, lattice.grid.teams))
			if len(lattice.panel) == 2:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams or lattice.grid.teams[2] in lattice.panel[0].watched_teams or lattice.grid.teams[3] in lattice.panel[0].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0] in lattice.panel[1].watched_teams or lattice.grid.teams[1] in lattice.panel[1].watched_teams or lattice.grid.teams[2] in lattice.panel[1].watched_teams or lattice.grid.teams[3] in lattice.panel[1].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[1], lattice.grid.teams))
			elif len(lattice.panel) == 1:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams or lattice.grid.teams[2] in lattice.panel[0].watched_teams or lattice.grid.teams[3] in lattice.panel[0].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[0], lattice.grid.teams))

def grid_list_checks(grid_list, tournament, round_num):
	for grid in grid_list:
		grid.warnings = []
		grid.large_warnings = []
	grid_check_one_sided(grid_list, tournament.team_list, round_num)
	grid_check_past_opponent(grid_list, tournament.team_list, round_num)
	grid_check_same_institution(grid_list, tournament.team_list, round_num)
	grid_check_power_pairing(grid_list, round_num)

def grid_check_power_pairing(grid_list, round_num):
	if len(grid_list[0].teams) == 2:
		if round_num > 1:
			for grid in grid_list:
				if abs(grid.teams[0].ranking - grid.teams[1].ranking) > int(0.3*2*len(grid_list)) or abs(sum(grid.teams[0].wins) - sum(grid.teams[1].wins)) > 1:
					difference = int(100*abs(grid.teams[0].ranking - grid.teams[1].ranking)/float(2*len(grid_list)))
					grid.warnings.append(PowerPairing(grid.teams[0], grid.teams[-1], difference))
	else:
		if round_num > 1:
			all_wins = [sum(team.wins) for grid in grid_list for team in grid.teams]
			for grid in grid_list:
				rankings = [team.ranking for team in grid.teams]
				wins = [sum(team.wins) for team in grid.teams]
				wins.sort()
				rankings.sort()
				wins_dict = {team: team.ranking for team in grid.teams}
				teams_sorted = sorted(list(wins_dict.items()), key=lambda x:x[1])
				len_teams = len(grid_list)*4
				if rankings[3]-rankings[0] > int(0.3*len_teams) or ret_wei(wins[3], all_wins, len(grid_list))-ret_wei(wins[0], all_wins, len(grid_list)) > 1:
					difference = int(100*abs(rankings[3]-rankings[0])/float(len_teams))
					grid.warnings.append(PowerPairing(teams_sorted[0][0], teams_sorted[3][0], difference))

def grid_check_one_sided(grid_list, tournament, round_num):
	if len(grid_list[0].teams) == 2:
		for i, grid in enumerate(grid_list):
			if is_one_sided(grid.teams[0], "gov", 2) != 0:
				grid.warnings.append(Sided(grid.teams[0], "gov", [grid.teams[0].past_sides.count("gov")+1, grid.teams[0].past_sides.count("opp")]))
			if is_one_sided(grid.teams[1], "opp", 2) != 0:
				grid.warnings.append(Sided(grid.teams[1], "opp", [grid.teams[0].past_sides.count("gov"), grid.teams[0].past_sides.count("opp")+1]))
			if grid.teams[0].past_sides.count("gov") == len(grid.teams[0].past_sides):# or grid.teams[0].past_sides.count(False) == len(grid.teams[0].past_sides):
				if round_num > 2:
					#interaction_modules.warn("ka;dslfjadsfdddddddddddd¥n¥n¥n¥n¥n¥n¥n¥n¥nn¥¥n¥n¥n¥n¥n")
					grid.warnings.append(AllSided(grid.teams[0], "gov", len(grid.teams[0].past_sides)+1))
			if grid.teams[1].past_sides.count("opp") == len(grid.teams[1].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[1], "opp", len(grid.teams[1].past_sides)+1))
	else:
		for i, grid in enumerate(grid_list):
			og_sided_value = is_one_halfed(grid.teams[0], "og")
			oo_sided_value = is_one_halfed(grid.teams[1], "oo")
			cg_sided_value = is_one_halfed(grid.teams[2], "cg")
			co_sided_value = is_one_halfed(grid.teams[3], "co")
			"""
			if og_sided_value != 0:
				grid.large_warnings.append("warning : a team's position unfair :"+str(grid.teams[0].name)+"("+str(grid.teams[0].past_sides.count("og")+1)+":"+str(grid.teams[0].past_sides.count("oo"))+":"+str(grid.teams[0].past_sides.count("cg"))+":"+str(grid.teams[0].past_sides.count("co"))+")")
				grid.warnings.append("wrn(unfair side)")
			if oo_sided_value != 0:
				grid.large_warnings.append("warning : a team's position unfair :"+str(grid.teams[1].name)+"("+str(grid.teams[1].past_sides.count("og"))+":"+str(grid.teams[1].past_sides.count("oo")+1)+":"+str(grid.teams[1].past_sides.count("cg"))+":"+str(grid.teams[1].past_sides.count("co"))+")")
				grid.warnings.append("wrn(unfair side)")
			if cg_sided_value != 0:
				grid.large_warnings.append("warning : a team's position unfair :"+str(grid.teams[2].name)+"("+str(grid.teams[2].past_sides.count("og"))+":"+str(grid.teams[2].past_sides.count("oo"))+":"+str(grid.teams[2].past_sides.count("cg")+1)+":"+str(grid.teams[2].past_sides.count("co"))+")")
				grid.warnings.append("wrn(unfair side)")
			if co_sided_value != 0:
				grid.large_warnings.append("warning : a team's position unfair :"+str(grid.teams[3].name)+"("+str(grid.teams[3].past_sides.count("og"))+":"+str(grid.teams[3].past_sides.count("oo"))+":"+str(grid.teams[3].past_sides.count("cg"))+":"+str(grid.teams[3].past_sides.count("co")+1)+")")
				grid.warnings.append("wrn(unfair side)")
			"""
			if grid.teams[0].past_sides.count("og") == len(grid.teams[0].past_sides):# or grid.teams[0].past_sides.count(False) == len(grid.teams[0].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[0], "og", len(grid.teams[0].past_sides)+1))
			if grid.teams[1].past_sides.count("oo") == len(grid.teams[1].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[1], "oo", len(grid.teams[1].past_sides)+1))
			if grid.teams[2].past_sides.count("cg") == len(grid.teams[2].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[2], "cg", len(grid.teams[2].past_sides)+1))
			if grid.teams[3].past_sides.count("co") == len(grid.teams[3].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[3], "co", len(grid.teams[3].past_sides)+1))
			if abs(og_sided_value) == 1:
				grid.warnings.append(Sided(grid.teams[0], "government/opposition", [grid.teams[0].past_sides.count("og")+1, grid.teams[0].past_sides.count("oo"), grid.teams[0].past_sides.count("cg"), grid.teams[0].past_sides.count("co")]))
			elif abs(og_sided_value) == 2:
				grid.warnings.append(Sided(grid.teams[0], "opening/closing", [grid.teams[0].past_sides.count("og")+1, grid.teams[0].past_sides.count("oo"), grid.teams[0].past_sides.count("cg"), grid.teams[0].past_sides.count("co")]))
			if abs(oo_sided_value) == 1:
				grid.warnings.append(Sided(grid.teams[1], "government/opposition", [grid.teams[1].past_sides.count("og"), grid.teams[1].past_sides.count("oo")+1, grid.teams[1].past_sides.count("cg"), grid.teams[1].past_sides.count("co")]))
			elif abs(oo_sided_value) == 2:
				grid.warnings.append(Sided(grid.teams[1], "opening/closing", [grid.teams[1].past_sides.count("og"), grid.teams[1].past_sides.count("oo")+1, grid.teams[1].past_sides.count("cg"), grid.teams[1].past_sides.count("co")]))
			if abs(cg_sided_value) == 1:
				grid.warnings.append(Sided(grid.teams[2], "government/opposition", [grid.teams[2].past_sides.count("og"), grid.teams[2].past_sides.count("oo"), grid.teams[2].past_sides.count("cg")+1, grid.teams[2].past_sides.count("co")]))
			elif abs(cg_sided_value) == 2:
				grid.warnings.append(Sided(grid.teams[2], "opening/closing", [grid.teams[2].past_sides.count("og"), grid.teams[2].past_sides.count("oo"), grid.teams[2].past_sides.count("cg")+1, grid.teams[2].past_sides.count("co")]))
			if abs(co_sided_value) == 1:
				grid.warnings.append(Sided(grid.teams[3], "government/opposition", [grid.teams[3].past_sides.count("og"), grid.teams[3].past_sides.count("oo"), grid.teams[3].past_sides.count("cg"), grid.teams[3].past_sides.count("co")+1]))
			elif abs(co_sided_value) == 2:
				grid.warnings.append(Sided(grid.teams[3], "opening/closing", [grid.teams[3].past_sides.count("og"), grid.teams[3].past_sides.count("oo"), grid.teams[3].past_sides.count("cg"), grid.teams[3].past_sides.count("co")+1]))

def grid_check_past_opponent(grid_list, tournament, round_num):
	for i, grid in enumerate(grid_list):
		pair_list = list(itertools.combinations(grid.teams, 2))
		#past_num = 0
		for pair in pair_list:
			if pair[0].past_opponents.count(pair[1].name) > 0:
				#grid.large_warnings.append("warning : a team matching again with past opponent :"+str(pair[0].name)+"-"+str(pair[1].name))
				#past_num += 1
				grid.warnings.append(PastOpponent(pair[0], pair[1]))

def grid_check_same_institution(grid_list, tournament, round_num):
	for i, grid in enumerate(grid_list):
		pair_list = list(itertools.combinations(grid.teams, 2))
		for pair in pair_list:
			conflicting_insti = list(set(pair[0].institutions) & set(pair[1].institutions))
			if conflicting_insti:
				for ci in conflicting_insti:
					grid.warnings.append(SameInstitution(conflicting_insti[0]))

def grid_list_errors(grid_list, tournament, round_num):
	large_warnings = []
	multi = {team.name:0 for team in tournament.team_list}

	for grid in grid_list:
		for team in grid.teams:
			multi[team.name] += 1

	for k, v in list(multi.items()):
		condemned_team = None
		for team in tournament.team_list:
			if team.name == k:
				condemned_team = team
				break
		if v > 1:
			large_warnings.append("error : a team appears more than two times :"+str(k)+": "+str(v))
		elif v == 0:
			if condemned_team.available:
				large_warnings.append("error : a team does not exist in matchups :"+str(k))
			else:
				large_warnings.append("warning : a team is absent :"+str(k))
	for i, grid in enumerate(grid_list):
		if len(list(set(grid.teams))) != len(grid.teams):
			large_warnings.append("error : a team matching with the same team :"+str([t.name for t in grid.teams]))
		for team in grid.teams:
			if not(team.available):
				large_warnings.append("error : an absent team appears :"+str(team.name))

	return large_warnings

def add_grid_list_info(selected_grid_list, tournament, round_num, comment):
	grid_list_checks(selected_grid_list, tournament, round_num)
	errors = grid_list_errors(selected_grid_list, tournament, round_num)
	selected_grid_list.large_warnings.extend(errors)
	for grid in selected_grid_list:
		for warn in grid.warnings:
			selected_grid_list.large_warnings.append(warn.longwarning())
	selected_grid_list.large_warnings.sort()
	selected_grid_list.power_pairing_indicator = calc_power_pairing_indicator(selected_grid_list, tournament.style["team_num"])
	selected_grid_list.same_institution_indicator = calc_same_institution_indicator(selected_grid_list)
	selected_grid_list.adopt_indicator, selected_grid_list.adopt_indicator_sd, selected_grid_list.adopt_indicator2 = calc_adopt_indicator(selected_grid_list)
	selected_grid_list.num_of_warnings = calc_num_of_warnings(selected_grid_list)
	selected_grid_list.scatter_indicator = calc_scatter_indicator(selected_grid_list)
	selected_grid_list.comment = comment

def return_selected_grid_lists(grid_list, round_num, tournament):
	if len(grid_list[0].teams) == 2:
		alg_list = [select_alg2, select_alg3, select_alg4, select_alg11, select_alg13, select_alg14]
	else:
		if len(grid_list) > 25**2:
			alg_list = []
		else:
			alg_list = [select_alg2, select_alg4, select_alg11, select_alg13, select_alg14]

	cp1_small = lambda g: g.adoptness1
	cp2_small = lambda g: g.adoptness2
	cp1_strict = lambda g: g.adoptness_strict1
	cp2_strict = lambda g: g.adoptness_strict2
	cp1_long = lambda g: g.adoptness1long
	cp2_long = lambda g: g.adoptness2long
	cp1_weight = lambda g: g.adoptness_weight1
	cp2_weight = lambda g: g.adoptness_weight2

	cp_pair_list = [(cp1_small, cp2_small), (cp2_small, cp1_small), (cp1_long, cp2_long), (cp2_long, cp1_long), (cp1_strict, cp2_strict), (cp2_strict, cp1_strict), (cp1_weight, cp2_weight), (cp2_weight, cp1_weight)]

	selected_grid_lists = []

	#interaction_modules.progress("creating special matchups")
	c = 1
	entire_length = 5
	if len(grid_list[0].teams) == 4:#add extra matchups
		def add_extra_matchups(pickup, divide_team_list_by_4, decide_position, comment, team_num):
			selected_grid_list_wudc = Grid_list()
			selected_grid_list_wudc2 = Grid_list()
			selected_grid_list_wudc = return_selected_grid_list_wudc(grid_list, tournament.team_list, pickup, divide_team_list_by_4, decide_position)
			selected_grid_list_info = add_grid_list_info(selected_grid_list_wudc, tournament.team_list, round_num, comment, tournament.style["team_num"])
			selected_grid_list_wudc2 = side_revision(grid_list, selected_grid_list_wudc)
			selected_grid_list_info2 = add_grid_list_info(selected_grid_list_wudc2, tournament.team_list, round_num, comment+" side-rev", tournament.style["team_num"])
			#selected_grid_list_wudc3 = side_revision(grid_list, selected_grid_list_wudc2)
			#selected_grid_list_info3 = return_grid_list_info(selected_grid_list_wudc3, team_list, round_num, comment+" side-rev2")

		add_extra_matchups(pickup_random, divide_team_list_by_4_random, decide_position_random, "WUDC RULE RANDOM", tournament.style["team_num"])
		#interaction_modules.progress_bar2(c, entire_length)
		c += 1
		add_extra_matchups(pickup_random, divide_team_list_by_4_score, decide_position_fair, "WUDC RULE CUSTOMIZED (For Atournament)", tournament.style["team_num"])
		#interaction_modules.progress_bar2(c, entire_length)
		c += 1
		add_extra_matchups(pickup_pull_up, divide_team_list_by_4_score, decide_position_fair, "WUDC RULE CUSTOMIZED pull up", tournament.style["team_num"])
		#interaction_modules.progress_bar2(c, entire_length)
		c += 1
		add_extra_matchups(pickup_pull_down, divide_team_list_by_4_score, decide_position_fair, "WUDC RULE CUSTOMIZED pull down", tournament.style["team_num"])
		#interaction_modules.progress_bar2(c, entire_length)
		c += 1
		add_extra_matchups(pickup_pull_up, divide_team_list_by_4_half, decide_position_fair, "WUDC RULE CUSTOMIZED position", tournament.style["team_num"])
		#interaction_modules.progress_bar2(c, entire_length)
		c += 1
	#interaction_modules.progress("")

	entire_length = len(alg_list) * len(cp_pair_list)
	c = 1

	def wrap(alg):
		def new_alg(es, selected_grid_lists, pid, *args):
			selected_grid_lists[pid] = alg(pid, *args)
			if len(selected_grid_lists[pid]) != 25:
				#interaction_modules.warn("pid:"+str(pid)+", alg:"+str(alg.__name__))#db
				selected_grid_lists[pid].internal_algorithm = "pid:"+str(pid)+", alg:"+str(alg.__name__)#db
			es[pid].set()
		return new_alg

	#threads = []
	new_selected_grid_lists = [Grid_list() for i in range(len(alg_list)*len(cp_pair_list))]
	es = [threading.Event() for i in range(len(alg_list)*len(cp_pair_list))]
	for i, cp_pair in enumerate(cp_pair_list):
		for j, alg in enumerate(alg_list):
			alg_wrapped = wrap(alg)
			t = threading.Thread(target=alg_wrapped, args=(es, new_selected_grid_lists, i*len(alg_list)+j, grid_list, round_num, tournament.team_list, cp_pair))
			t.setDaemon(True)
			t.start()
			#if i == 0 and j == 0: t.start()

	while True:
		if False not in [e.isSet() for e in es]:
			selected_grid_lists.extend(new_selected_grid_lists)
			break
		else:
			#interaction_modules.progress_bar2([e.isSet() for e in es].count(True), entire_length)
			time.sleep(0.5)

	"""			
	#db
	for i, cp_pair in enumerate(cp_pair_list):
		for j, alg in enumerate(alg_list):
			interaction_modules.progress_bar2(c, entire_length)
			c+=1
			selected_grid_lists.append(alg(i*len(alg_list)+j, grid_list, round_num, tournament["team_list"], cp_pair))
	"""
	
	#interaction_modules.progress("")
	#interaction_modules.progress("deleting same matchups")
	selected_grid_lists2 = Grid_list()
	for selected_grid_list in selected_grid_lists:
		if selected_grid_list != None:
			selected_grid_list.sort(key=lambda g: sum([t.code for t in g.teams]))
			if not multi(selected_grid_list, selected_grid_lists2):
				selected_grid_lists2.append(selected_grid_list)

	revised_selected_grid_lists2 = Grid_list()

	for selected_grid_list in selected_grid_lists2:
		revised_selected_grid_lists2.append(side_revision(grid_list, selected_grid_list))
	#revised2_selected_grid_lists2 = [side_revision2(grid_list, selected_grid_list) for selected_grid_list in revised_selected_grid_lists2]
	#selected_grid_lists3 = selected_grid_lists2+revised_selected_grid_lists2+revised2_selected_grid_lists2
	selected_grid_lists3 = revised_selected_grid_lists2

	for selected_grid_list3 in selected_grid_lists3:
		selected_grid_list3.sort(key=lambda grid: grid.__hash__())
	#interaction_modules.progress("creating more precise matchups")
	if len(grid_list[0].teams) == 2:#add more precise matchups
		selected_grid_lists4 = copy.copy(selected_grid_lists3)
		for selected_grid_list in selected_grid_lists3:
			revised_selected_grid_list = revise_selected_grid_list(selected_grid_list, grid_list)
			if not multi(revised_selected_grid_list, selected_grid_lists4):
				selected_grid_lists4.append(revised_selected_grid_list)
	else:
		selected_grid_lists4 = selected_grid_lists3
	#interaction_modules.progress("adding information to matchups")
	for k, selected_grid_list in enumerate(selected_grid_lists4):#add information
		add_grid_list_info(selected_grid_list, tournament, round_num, "")

	##################################################################################################

	selected_grid_lists4.sort(key=lambda selected_grid_list: (selected_grid_list.power_pairing_indicator, -selected_grid_list.adopt_indicator, selected_grid_list.same_institution_indicator), reverse=True)

	return selected_grid_lists4

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

def side_revision(grid_list, selected_grid_list):
	selected_grid_list2 = Grid_list()
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

def check_team_list(team_list):
	team_names = [team.name for team in team_list]
	for team_name in team_names:
		if team_names.count(team_name) > 1:
			raise Exception("error : Same team name appears : {}".format(team_name))

	for team in team_list:
		if not("c" in [insti.scale for insti in team.institutions] or "a" in [insti.scale for insti in team.institutions] or "b" in [insti.scale for insti in team.institutions]):
			raise Exception("error : Team scale broken : {}".format(team_name))

def check_adjudicator_list(adjudicator_list):
	adjudicators_names = [adjudicator.name for adjudicator in adjudicator_list]
	for adjudicator_name in adjudicators_names:
		if adjudicators_names.count(adjudicator_name) > 1:
			raise Exception("error : same adjudicator name appears : {}".format(adjudicator_name))

def check_team_list2(team_list, experienced_round_num, team_num):
	c = 0
	for team in team_list:
		if team.available:
			c+=1
	if (c % team_num) == 1:
		raise Exception("The number of teams is odd")
	for team in team_list:
		if len(team.past_opponents) != experienced_round_num*(team_num-1):
			if team.available:
				raise Exception("[warning]{0:15s} : uncertain data in past_opponents, round num != len(past_opponents)    {1}".format(team.name, team.past_opponents))
		if len(team.scores) != experienced_round_num:
			if team.available:
				raise Exception("[warning]{0:15s} : uncertain data in scores, round num != len(scores)    {1}".format(team.name, team.scores))
		if len(team.past_sides) != experienced_round_num:
			if team.available:
				raise Exception("[warning]{0:15s} : uncertain data in past_sides, round num != len(past_sides)    {1}".format(team.name, team.past_sides))
		if len(team.wins) != experienced_round_num:
			if team.available:
				raise Exception("[warning]{0:15s} : uncertain data in wins, round num != len(wins)    {1}".format(team.name, team.wins))

def create_lattice_list(matchups, adjudicator_list):
	lattice_list = Lattice_list()
	for grid in matchups:
		for chair in adjudicator_list:
			lattice_list.append(Lattice(grid, chair))

	for lattice in lattice_list:
		if (False in [t.available for t in lattice.grid.teams]) or lattice.chair.absent:
			lattice.set_not_available()
	#interaction_modules.warn(str(len(lattice_list)))#db
	return lattice_list


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
	selected_grid_list = Grid_list()
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
	selected_grid_list2 = Grid_list()
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
