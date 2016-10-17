from .bit_modules import *
from .internal_modules import *
from .io_modules import *
from .entity_classes import *

import time
#import re
#import copy
#import sys
#from datetime import datetime
#import os.path
#import math
#import shutil

def add_element(target_list, element):
	if element not in target_list:
		target_list.append(element)
	else:
		raise Exception("id {} already exists".format(element.code))

def delete_element(target_list, element_or_code):
	if type(element_or_code) == int:
		element = filter(lambda x: x.code == element_or_code)[0]
	else:
		element = element_or_code

	try:
		target_list.remove(element)
	except:
		raise Exception("id {} does not exist".format(element.code))

def find_element_by_code(target_list, code):
	elements = filter(lambda x: x.code == code, target_list)
	if len(elements) == 0:
		raise Exception("Entity id {} does not exist")
	return elements[0]

def check_name_and_code(target_list, code, name):
	element = find_element_by_code(target_list, code)
	if element.name != name:
		raise Exception("Entity id {} has name {}, not {}".format(code, element.name, name))

class Tournament:
	def __init__(self, tournament_code, tournament_name, round_num, style, host = "", url = "", break_team_num = 0):
		self.name = tournament_name
		self.tournament_code = tournament_code
		self.round_num = round_num
		self.style = style
		self.host = host
		self.url = url
		self.team_list = Team_list
		self.adjudicator_list = []
		self.debater_list = []
		self.venue_list = []
		self.institution_list = []
		self.rounds = [Round(i+1, self) for i in range(round_num)]
		self.filter_lists = []#
		self.constants = []#
		self.break_team_num = break_team_num
		self.now_round = 1
		self.finished = False
		self.results = None
		self.analysis = None

	def add_team(self, code, name, url="", debaters, institutions):
		team = Team(code, name, debaters, institutions)
		add_element(self.team_list, team)

	def modify_team(self, code, name=None, url=None, debaters=None, institutions=None):
		if code in [t.code for t in self.team_list]:
			team = filter(lambda x: x.code == code)[0]
			if name is not None:
				team.name = name
			if debaters is not None:
				team.debaters = debaters
			if institutions is not None:
				team.institutions = institutions
			if url is not None:
				team.url = url
		else:
			raise Exception("team code {} does not exist".format(code))

	def delete_team(self, team_or_code):
		delete_element(self.team_list, team_or_code)

	def add_adjudicator(self, code, name, url="", reputation, judge_test, institutions, conflict_teams):
		adj = Adjudicator(code, name, url, reputation, judge_test, institutions, conflict_teams)
		add_element(self.adjudicator_list, adj)

	def delete_adjudicator(self, adj_or_code):
		delete_element(self.adjudicator_list, adj_or_code)

	def add_debater(self, code, name, url=""):
		debater = Debater(code, name, url)
		add_element(self.debater_list, debater)

	def delete_debater(self, debater_or_code):
		delete_element(self.debater_list, debater_or_code)

	def add_venue(self, code, name, url="", available = True, priority = 1):
		venue = Venue(code, name)
		add_element(self.venue_list, venue)

	def delete_venue(self, venue_or_code):
		delete_element(self.venue_list, venue_or_code)

	def modify_venue_status(self):
		pass

	def add_institution(self, code, name, url="", scale="a"):
		institution = Institution(code, name, url, scale)
		add_element(self.institution_list, institution)

	def delete_institution(self, institution_or_code):
		delete_element(self.institution_list, institution_or_code)

	def list_adjudicators(self):
		pass

	def list_teams(self):
		pass

	def list_venues(self):
		pass

	def list_speakers(self):
		pass

	def list_institutions(self):
		pass

	def end(self):
		#issue results
		pass

class Round:
	def __init__(self, r, tournament):
		self.r = r    #	round No. ex) Round 1 => 1
		self.tournament = tournament
		self.prepared = False    #	True if round preparation has finished
		self.grid_list = []
		self.lattice_list = None
		self.candidate_matchups = None
		self.candidate_allocations = None
		self.candidate_panel_allocation = None
		self.candidate_venue_allocation = None
		self.matchup = None
		self.allocation = None
		self.panel_allocation = None
		self.venue_allocation = None
		self.matchups_processed = False
		self.allocations_processed = False
		self.panel_allocation_processed = False
		self.venue_allocation_processed = False
		self.finished = False
		self.constants = {}
		self.constants_of_adj = {}
		self.filter_list = []
		self.filter_of_adj_list = []

	def set_constants(self, v_random_pairing = 4, des_power_pairing = 1, des_w_o_same_a_insti = 2, des_w_o_same_b_insti = 0, des_w_o_same_c_insti = 0, des_with_fair_sides = 3):
		self.constants["random_pairing"] = v_random_pairing
		self.constants["des_power_pairing"] = des_power_pairing
		self.constants["des_w_o_same_a_insti"] = des_w_o_same_a_insti
		self.constants["des_w_o_same_b_insti"] = des_w_o_same_b_insti
		self.constants["des_w_o_same_c_insti"] = des_w_o_same_c_insti
		self.constants["des_w_o_same_opp"] = des_w_o_same_opp
		self.constants["des_with_fair_sides"] = des_with_fair_sides
		functions = [random_pairing, power_pairing, prevent_same_institution_a, prevent_same_institution_b, prevent_same_institution_c, prevent_same_opponent, prevent_unfair_side]

		order = [v_random_pairing, des_power_pairing, des_w_o_same_a_insti, des_w_o_same_b_insti, des_w_o_same_c_insti, des_with_fair_sides]
		for i in range(len(functions)):
			if i+1 in order:
				self.filter_list.append(functions[order.index(i+1)])

	def set_constants_of_adj(self, v_random_allocation = 4, des_strong_strong = 2, des_with_fair_sides = 3, des_avoiding_conflicts = 1, des_avoiding_past = 0, des_priori_bubble = 0, des_chair_rotation = 0, judge_test = 0, judge_repu_percent = 0, judge_perf_percent = 0):
		self.constants_of_adj["random_allocation"] = v_random_allocation
		self.constants_of_adj["des_strong_strong"] = des_strong_strong
		self.constants_of_adj["des_with_fair_times"] = des_with_fair_times
		self.constants_of_adj["des_avoiding_conflicts"] = des_avoiding_conflicts
		self.constants_of_adj["des_avoiding_past"] = des_avoiding_past
		self.constants_of_adj["des_priori_bubble"] = des_priori_bubble
		self.constants_of_adj["des_chair_rotation"] = des_chair_rotation
		self.constants_of_adj["judge_test_percent"] = judge_test_percent
		self.constants_of_adj["judge_repu_percent"] = judge_repu_percent
		self.constants_of_adj["judge_perf_percent"] = judge_perf_percent
		functions = [random_allocation, prevent_str_wek_round, prevent_unfair_adjudicators, prevent_conflicts, avoid_watched_teams, prioritize_bubble_round, rotation_allocation]

		order = [v_random_allocation, des_strong_strong, des_with_fair_sides, des_avoiding_conflicts, des_avoiding_past, des_priori_bubble, des_chair_rotation, judge_test, judge_repu_percent, judge_perf_percent]
		for i in range(len(functions)):
			if i+1 in order:
				self.filter_of_adj_list.append(functions[order.index(i+1)])

	def set(self, force = False):
		adj_available_num = len([adj for adj in self.tournament.adjudicator_list if not adj.absent])
		venue_available_num = len([venue for venue in tournament.venue_list if venue.available])
		team_available_num = len([team for team in tournament.team_list if team.available])
		#interaction_modules.progress("Available Adjudicators: {0:d}, Available Venues: {1:d}, Available Teams: {2:d}".format(adj_available_num, venue_available_num, team_available_num))

		if adj_available_num < team_available_num/self.tournament.style["team_num"]:
			raise Exception("More adjudicators needed")
		if venue_available_num < team_available_num/self.tournament.style["team_num"]:
			raise Exception("More venues needed")
		if team_available_num % self.tournament.style["team_num"] != 0 and not force:
			raise Exception("{} teams cannot take part in the next round. {} more teams needed".format(team_available_num % self.tournament.style["team_num"], self.tournament.style["team_num"] - (team_available_num % self.tournament.style["team_num"])))

		if not force:
			check_team_list(self.tournament.team_list)
			check_adjudicator_list(self.tournament.adjudicator_list)

	def compute_matchups(self):
		grid_flag = threading.Event()
		create_grid_list_by_thread(self.grid_list, self.tournament.team_list, self.tournament.style["team_num"], grid_flag)
		evaluate_adjudicator(self.tournament.adjudicator_list, self.constants_of_adj)
		sort_adjudicator_list_by_score(self.tournament.adjudicator_list)
		sort_team_list_by_score(self.tournament.team_list)
		while True:
			if grid_flag.isSet():
				break
			else:
				time.sleep(0.5)

		self.matchups = create_matchups(grid_list=self.grid_list, round_num=self.r, tournament=self.tournament, filter_list=filter_list, team_num=self.tournament.style["team_num"], workfolder_name=fnames["workfolder"])
		self.matchups_processed = True

	def set_matchup(self, matchup):
		self.matchup = matchup

	def compute_allocations(self):
		lattice_list = create_lattice_list(matchups[0], tournament["adjudicator_list"])
		self.allocations = create_allocations(tournament=self.tournament, selected_grid_list=self.matchup, lattice_list=lattice_list, round_num=self.r, filter_list=self.filter_of_adj_list, constants_of_adj=self.constants_of_adj, workfolder_name=fnames["workfolder"])
		self.allocations_processed = True

	def set_allocation(self, allocation):
		self.allocation = allocation

	def compute_venue_allocation(self):
		available_venue_list = [venue for venue in self.tournament.venue_list if venue.available]
		random.shuffle(available_venue_list)
		available_venue_list.sort(key=lambda venue:venue.priority)
		for lattice, venue in zip(self.allocation, available_venue_list):
			lattice.venue = venue
		#print(len(available_venue_list))
		#print(len(allocations))
		self.allocation.sort(key=lambda lattice: lattice.venue.name)
		self.venue_allocation_processed = True

	def set_venue_allocation(self, venue_allocation):
		self.venue_allocation = venue_allocation

	def compute_panel_allocation(self):
		for lattice in self.allocation:
			for adjudicator in self.tournament.adjudicator_list:
				if adjudicator.name == lattice.chair.name:
					adjudicator.active = True
					break

		allocation.large_warnings = []

		inactive_adjudicator_list = [adjudicator for adjudicator in self.tournament.adjudicator_list if (not(adjudicator.active) and not(adjudicator.absent))]
		inactive_adjudicator_list.sort(key=lambda adjudicator:adjudicator.evaluation, reverse=True)

		if len(self.tournament.style["team_num"]) == 2:
			for lattice in self.allocation:
				may_be_panels = []
				for panel in inactive_adjudicator_list:
					conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(panel.institutions)
					conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(panel.institutions)
					if list(conflicting_insti1 | conflicting_insti2) or panel.active:
						continue
					else:
						may_be_panels.append(panel)
					if len(may_be_panels) == 2:
						break
				if len(may_be_panels) < 2:
					continue
				else:
					lattice.panel = may_be_panels
					lattice.panel[0].active = True
					lattice.panel[1].active = True
		else:
			for lattice in self.allocation:
				may_be_panels = []
				for panel in inactive_adjudicator_list:
					conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(panel.institutions)
					conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(panel.institutions)
					conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(panel.institutions)
					conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(panel.institutions)
					if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4) or panel.active:
						continue
					else:
						may_be_panels.append(panel)
					if len(may_be_panels) == 2:
						break
				if len(may_be_panels) < 2:
					continue
				else:
					lattice.panel = may_be_panels
					lattice.panel[0].active = True
					lattice.panel[1].active = True

		self.panel_allocation_processed = True

	def set_panel_allocation(self, panel_allocation):
		self.panel_allocation = panel_allocation

	def set_result(self, result, override = False):


		#	{
		#		debater単位
		#	}
		#
		#
		#
		#
		#
		#
		#

        position_num = len(self.tournament.style["score_weights"])
        team_num = self.tournament.style["team_num"]
        debater_num_per_team = self.tournament.style["debater_num_per_team"]
        score_weights = self.tournament.style["score_weights"]

		if len(result["points"]) != position_num:
			raise Exception("Length of points is incorrect")
		if result["points"].count(0) == 0:
			raise Exception("Debater id {} has fields with all 0".format(result["id"]))######### When in typical style?
		elif result["points"].count(0) == positions:
			raise Exception("points of Debater id {} has all fields non zero".format(result["id"]))

		"""	

        "team_id": team_id,
        "id": ,
        "points": ::[Float], /* 0 if he/she has no role */
        "win": ::Bool /* True if win else False */,
        "opponent_team_id": opponent_team_name,
        "side": ::String /* in BP, "og", "oo", "cg", "co". in 2side game, "gov", "opp"

        for i in range(int(len(results_list)/debater_num_per_team)):#results=>[team name, name, R[i] 1st, R[i] 2nd, R[i] rep, win?lose?, opponent name, gov?opp?]
				for team in tournament["team_list"]:
					if team.name == results_list[debater_num_per_team*i][0]:
						member_names = [results_list[debater_num_per_team*i+j][1] for j in range(debater_num_per_team)]
						member_score_lists = [results_list[debater_num_per_team*i+j][2:2+positions] for j in range(debater_num_per_team)]
						side = results_list[debater_num_per_team*i][2+positions+team_num]
						win = results_list[debater_num_per_team*i][2+positions]
						for debater in team.debaters:
							for member_name, member_score_list in zip(member_names, member_score_lists):
								if debater.name == member_name:
									score = 0
									sum_weight = 0
									for sc, weight in zip(member_score_list, score_weight):
										score += sc
										sum_weight += weight
									if sum_weight == 0:
										interaction_modules.warn("error: Results file(Results"+str(round_num)+".csv) broken")
									else:
										score = score/float(sum_weight)
										debater.finishing_process(member_score_list, score)
										debater_list_temp.append(debater)
										break
							else:
								interaction_modules.warn("error: Results file(Results"+str(round_num)+".csv) broken")
	
						if team_num == 4:
							margin = 0
						else:
							opp_team_score = 0
							for results in results_list:
								if results[0] == results_list[debater_num_per_team*i][3+positions]:
									opp_team_score += sum(results[2:2+positions])
							margin = sum([sum(member_score_list) for member_score_list in member_score_lists])-opp_team_score
						team.finishing_process(opponent=[results_list[debater_num_per_team*i][3+positions+j] for j in range(team_num-1)], score=sum([sum(member_score_list) for member_score_list in member_score_lists]), side=side, win=win, margin=margin)
						team_list_temp.append(team)
	
			all_debater_list = [d for t in tournament["team_list"] for d in t.debaters]
			ranking = 1
			for debater in all_debater_list:
				debater.rankings.append(ranking)
				debater.rankings_sub.append(ranking)
				ranking += 1
			rest_debater_list = [d for d in all_debater_list if d not in debater_list_temp]
			for debater in rest_debater_list:
				debater.score_lists_sub.append(['n/a']*positions)
				debater.scores_sub.append('n/a')
				debater.rankings_sub.append('n/a')
	
			for team in tournament["team_list"]:
				if team.name not in [results[0] for results in results_list]:
					if team.available:
						interaction_modules.warn("team: {0:15s} not in results: {1}".format(team.name, filename_results))
	
			for team in tournament["team_list"]:
				for debater in team.debaters:
					if debater.name not in [results[1] for results in results_list]:
						if team.available:
							interaction_modules.warn("debater: {0:15s} not in results: {1}".format(debater.name, filename_results))
	
			rest_team_list = [t for t in tournament["team_list"] if t not in team_list_temp]
			for team in rest_team_list:
				team.dummy_finishing_process()
				for debater in team.debaters:
					debater.dummy_finishing_process(style_cfg)
			"""

	def end(self, force = False):
		if not force:
			check_team_list2(self.tournament.team_list, self.tournament.now_round, self.tournament.style["team_num"])

		self.tournament.now_round += 1
