# -*- coding: utf-8 -*-
import time
import os
import json

from src.bit import *
from src.internal import *
from src.entity_classes import *
from src.result import *
from src.db import *
import src.tools as tools

with open(os.path.dirname(__file__)+'/dat/styles.json') as f:
	styles = json.load(f)

tournaments = {
			  }

class Tournament:
	def __init__(self, name, code, round_num, style, host, url, break_team_num = 0):
		self.name = name
		self.code = code
		self.round_num = round_num
		self.style = style
		self.host = host
		self.url = url
		self.team_list = []
		self.adjudicator_list = []
		self.debater_list = []
		self.venue_list = []
		self.institution_list = []
		self.rounds = [Round(i+1, self) for i in range(round_num)]
		self.judge_criterion = None
		self.break_team_num = break_team_num
		self.now_round = 1
		self.finished = False
		self.analysis = None

	def start_round(self, force=False):
		self.rounds[self.now_round-1].set(force=force)
		return self.rounds[self.now_round-1]

	def add_judge_criterion(self, judge_criterion_dicts):
		self.judge_criterion = judge_criterion_dicts
		return self.judge_criterion

	def add_team(self, name, debater_codes, institution_codes, url, available, code=None):
		institutions = tools.find_elements_by_ids(self.institution_list, institution_codes)
		debaters = tools.find_elements_by_ids(self.debater_list, debater_codes)
		if code is None:
			team = Team(tools.generate_code(self.team_list), name, url, debaters, institutions, available)
		else:
			team = Team(code, name, url, debaters, institutions, available)
		add_element(self.team_list, team)

		return team

	def modify_team(self, code, name=None, url=None, debaters=None, institutions=None):
		team = find_element_by_id(self.team_list, code)[0]
		if name is not None:
			team.name = name
		if debaters is not None:
			team.debaters = debaters
		if institutions is not None:
			team.institutions = institutions
		if url is not None:
			team.url = url

	def delete_team(self, team_or_code):
		delete_element(self.team_list, team_or_code)

	def add_adjudicator(self, name, reputation, judge_test, institution_codes, conflict_team_codes, url, available, code=None):
		institutions = tools.find_elements_by_ids(self.institution_list, institution_codes)
		conflict_teams = tools.find_elements_by_ids(self.team_list, conflict_team_codes)
		if code is None:
			adj = Adjudicator(tools.generate_code(self.adjudicator_list), name, url, reputation, judge_test, institutions, conflict_teams, available)
		else:
			adj = Adjudicator(code, name, url, reputation, judge_test, institutions, conflict_teams, available)
		add_element(self.adjudicator_list, adj)

		return adj

	def delete_adjudicator(self, adj_or_code):
		delete_element(self.adjudicator_list, adj_or_code)

	def add_debater(self, name, url, code=None):
		if code is None:
			debater = Debater(tools.generate_code(self.debater_list), name, url)
		else:
			debater = Debater(code, name, url)
		add_element(self.debater_list, debater)

		return debater

	def delete_debater(self, debater_or_code):
		delete_element(self.debater_list, debater_or_code)

	def add_venue(self, name, url, available, priority, code=None):
		if code is None:
			venue = Venue(tools.generate_code(self.venue_list), name, url, available, priority)
		else:
			venue = Venue(code, name, url, available, priority)

		add_element(self.venue_list, venue)
		return venue

	def delete_venue(self, venue_or_code):
		delete_element(self.venue_list, venue_or_code)

	def modify_venue_status(self):
		pass

	def add_institution(self, name, url, scale, code=None):
		if code is None:
			institution = Institution(tools.generate_code(self.institution_list), name, url, scale)
		else:
			institution = Institution(code, name, url, scale)
		add_element(self.institution_list, institution)

		return institution

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
		self.grid_list = Grid_list()
		self.lattice_list = None
		self.candidate_matchups = None
		self.candidate_allocations = None
		self.candidate_panel_allocation = None
		self.candidate_venue_allocation = None
		self.matchup = None
		self.allocation = None
		self.__round_status = 0
		"""
		0: before starting round(adding adjudicators, etc...)
		1: computing matchups
		2: finished computing matchups
		3: computing allocations
		4: finished computing matchups
		5: computing panel allocation
		6: finished computing panel allocation
		7: computing venue allocation
		8: finished computing venue allocation
		9: collecting results
		10: team results processing
		11: team results processed
		12: adj results processing
		13: adj results processed
		14: results processed, prepared to proceed to next round
		"""
		self.normal = True # False if an error occur
		self.constants = {}
		self.constants_of_adj = {}
		self.filter_list = []
		self.filter_of_adj_list = []
		self.raw_results = {}
		self.raw_results_of_adj = {}

	def this_round(func):
		def _(*args, **kwargs):
			self = args[0]
			if self.r == self.tournament.now_round:
				ret_val = func(*args, **kwargs)
				return ret_val
			else:
				raise Exception('requested round is not available now')
		return _

	@this_round
	def set_constants(self, v_random_pairing = 4, des_power_pairing = 1, des_w_o_same_a_insti = 2, des_w_o_same_b_insti = 0, des_w_o_same_c_insti = 0, des_w_o_same_opp = 5, des_with_fair_sides = 3):
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

	@this_round
	def set_constants_of_adj(self, v_random_allocation = 4, des_strong_strong = 2, des_with_fair_times = 3, des_avoiding_conflicts = 1, des_avoiding_past = 0, des_priori_bubble = 0, des_chair_rotation = 0):
		self.constants_of_adj["random_allocation"] = v_random_allocation
		self.constants_of_adj["des_strong_strong"] = des_strong_strong
		self.constants_of_adj["des_with_fair_times"] = des_with_fair_times
		self.constants_of_adj["des_avoiding_conflicts"] = des_avoiding_conflicts
		self.constants_of_adj["des_avoiding_past"] = des_avoiding_past
		self.constants_of_adj["des_priori_bubble"] = des_priori_bubble
		self.constants_of_adj["des_chair_rotation"] = des_chair_rotation
		functions = [random_allocation, prevent_str_wek_round, prevent_unfair_adjudicators, prevent_conflicts, avoid_watched_teams, prioritize_bubble_round, rotation_allocation]

		order = [v_random_allocation, des_strong_strong, des_with_fair_times, des_avoiding_conflicts, des_avoiding_past, des_priori_bubble, des_chair_rotation]
		for i in range(len(functions)):
			if i+1 in order:
				self.filter_of_adj_list.append(functions[order.index(i+1)])

	@this_round
	def set(self, force = False):
		if self.tournament.now_round != self.r:
			raise Exception("prior round is not finished")
		if self.tournament.judge_criterion is None:
			raise Exception('judge criterion is not set')
		if self.r == 1:
			if len(self.tournament.judge_criterion) < self.tournament.round_num:
				raise Exception('need to set judge criterion!')
			if self.tournament.style is None:
				raise Exception('need to set up style')

		adj_available_num = len([adj for adj in self.tournament.adjudicator_list if not adj.absent])
		venue_available_num = len([venue for venue in self.tournament.venue_list if venue.available])
		team_available_num = len([team for team in self.tournament.team_list if team.available])

		if adj_available_num < team_available_num/self.tournament.style["team_num"]:
			raise Exception("More adjudicators needed")
		if venue_available_num < team_available_num/self.tournament.style["team_num"]:
			raise Exception("More venues needed")
		if team_available_num % self.tournament.style["team_num"] != 0 and not force:
			raise Exception("{} teams cannot take part in the next round. {} more teams needed".format(team_available_num % self.tournament.style["team_num"], self.tournament.style["team_num"] - (team_available_num % self.tournament.style["team_num"])))

		if self.constants == {}:
			raise Exception("constants in round {} is not set".format(self.r))
		if self.constants_of_adj == {}:
			raise Exception("constants of adj in round {} is not set".format(self.r))

		if not force:
			check_team_list(self.tournament.team_list)
			check_adjudicator_list(self.tournament.adjudicator_list)

	@this_round
	def get_round_status(self):
		return self.__round_status

	@this_round
	def compute_matchups(self):
		self.__round_status = 1
		grid_flag = threading.Event()

		create_grid_list_by_thread(self.grid_list, self.tournament.team_list, self.tournament.style["team_num"], grid_flag)

		evaluate_adjudicator(self.tournament.adjudicator_list, self.tournament.judge_criterion)
		sort_adjudicator_list_by_score(self.tournament.adjudicator_list)
		sort_team_list_by_score(self.tournament.team_list)

		while True:
			if grid_flag.isSet():
				break
			else:
				time.sleep(0.5)
		self.candidate_matchups = create_matchups(grid_list=self.grid_list, round_num=self.r, tournament=self.tournament, filter_list=self.filter_list, team_num=self.tournament.style["team_num"])
		self.__round_status = 2

	@this_round
	def set_matchup(self, matchup):
		self.matchup = matchup

	@this_round
	def add_imported_matchup(self, matchup_dict):
		code = tools.generate_code(self.candidate_matchups)
		new_matchup = get_imported_matchup(matchup_dict, self.grid_list, self.tournament, self.r, code)
		self.candidate_matchups.append(new_matchup)

		return new_matchup, code

	@this_round
	def add_imported_allocation(self, allocation_dict):
		code = tools.generate_code(self.candidate_allocations)
		new_allocation = get_imported_allocation(allocation_dict, self.lattice_list, self.tournament, self.r, code)
		self.candidate_allocations.append(new_allocation)

		return new_allocation, code

	@this_round
	def respond_matchup(self, code=None):
		if code is not None:
			matchup = find_element_by_id(self.candidate_matchups, code)
		else:
			matchup = self.matchup
		matchup_dict = {}
		matchup_dict["algorithm"] = matchup.internal_algorithm
		matchup_dict["indices"] = {
		    "power_pairing_indicator": matchup.power_pairing_indicator,
		    "adopt_indicator": matchup.adopt_indicator,
		    "adopt_indicator2": matchup.adopt_indicator2,
		    "adopt_indicator_sd": matchup.adopt_indicator_sd,
		    "gini_index": matchup.gini_index,
		    "scatter_indicator": matchup.scatter_indicator
		}
		matchup_dict["large_warings"] = matchup.large_warnings
		matchup_conv = []
		for grid in matchup:
			matchup_conv.append({
				"team_ids": tools.get_ids(grid.teams),
				"warnings": [w.status for w in grid.warnings]
			})
		matchup_dict["allocation"] = matchup_conv

		matchup_dict["code"] = matchup.code
		return matchup_dict

	@this_round
	def respond_matchups(self):
		codes = [m.code for m in self.candidate_matchups]
		return [self.respond_matchup(code) for code in codes]

	@this_round
	def respond_allocation(self, code=None):
		if code is not None:
			allocation = find_element_by_id(self.candidate_allocations, code)
		else:
			allocation = self.allocation
		allocation_dict = {}
		allocation_dict["algorithm"] = allocation.internal_algorithm
		allocation_dict["indices"] = {
		    "strong_strong_indicator": allocation.strong_strong_indicator
		}
		allocation_dict["large_warings"] = allocation.large_warnings
		allocation_conv = []
		for lattice in allocation:
			allocation_conv.append(
				{
					"teams": tools.get_ids(lattice.grid.teams),
					"warnings": [w.status for w in lattice.warnings],#############################################################
					"chairs": [lattice.chair.code],##############fix in next version
					"venue": lattice.venue.code if lattice.venue is not None else None,
					"panels": tools.get_ids(lattice.panels)
				})
		allocation_dict["allocation"] = allocation_conv

		allocation_dict["code"] = allocation.code
		return allocation_dict

	@this_round
	def respond_allocations(self):
		codes = [m.code for m in self.candidate_allocations]
		return [self.respond_allocation(code) for code in codes]

	@this_round
	def compute_allocations(self):
		if self.matchup is None:
			raise Exception('you must compute team allocation first')
		self.__round_status = 3
		self.lattice_list = create_lattice_list(self.matchup, self.tournament.adjudicator_list)
		self.candidate_allocations = create_allocations(tournament=self.tournament, selected_grid_list=self.matchup, lattice_list=self.lattice_list, round_num=self.r, filter_list=self.filter_of_adj_list)
		self.__round_status = 5
		for allocation in self.candidate_allocations:
			set_panel_allocation(allocation, self.tournament)

	@this_round
	def set_allocation(self, allocation):
		self.allocation = allocation

	@this_round
	def compute_venue_allocation(self):
		self.__round_status = 7
		available_venue_list = [venue for venue in self.tournament.venue_list if venue.available]
		random.shuffle(available_venue_list)
		available_venue_list.sort(key=lambda venue:venue.priority)
		for lattice, venue in zip(self.allocation, available_venue_list):
			lattice.venue = venue
		#print(len(available_venue_list))
		#print(len(allocations))
		self.allocation.sort(key=lambda lattice: lattice.venue.name)
		self.__round_status = 8

	@this_round
	def set_result(self, data, meta, override = False):
		self.__round_status = 9
		debater_id = data["debater_id"]
		result_to_set = {
			"debater_id": data["debater_id"],
			"team_id": data["team_id"],
			"scores": data["scores"],
			"win_point": data["win_point"],
			"opponent_ids": data["opponent_ids"],
			"position": data["position"]
		}

		uid = meta["from_id"]

		#check_result(self.tournament, meta)####################################

		if debater_id in self.raw_results:
			if override:
				self.raw_results[debater_id][uid] = result_to_set
			else:
				if self.raw_results[debater_id][uid]:
					raise Exception('already sent')
				else:
					self.raw_results[debater_id][uid] = result_to_set

		else:
			self.raw_results[debater_id] = {uid: result_to_set}

		return result_to_set

	@this_round
	def set_result_of_adj(self, data, meta, override = False):
		self.__round_status = 9
		adj_id = data["adjudicator_id"]
		result_to_set = {
			"adjudicator_id": data["adjudicator_id"],
			"chair": data["chair"],
			"score": data["score"],
			"teams": data["teams"],
			"comment": data["comment"]
		}

		uid = meta["from_id"] if meta["from"] == 'team' else -meta["from_id"]

		#check_result_of_adj(self.tournament, meta)####################################

		if adj_id in self.raw_results_of_adj:
			if override:
				self.raw_results_of_adj[adj_id][uid] = result_to_set
			else:
				if self.raw_results_of_adj[adj_id][uid]:
					raise Exception('already sent')
				else:
					self.raw_results_of_adj[adj_id][uid] = result_to_set

		else:
			self.raw_results_of_adj[adj_id] = {uid: result_to_set}

		return result_to_set

	@this_round
	def end(self, force = False):
		if not force:
			check_team_list2(self.tournament.team_list, self.tournament.now_round, self.tournament.style["team_num"])

		self.tournament.now_round += 1
		self.__round_status = 14

	@this_round
	def process_result(self, force=False):
		self.__round_status = 10
		team_num = self.tournament.style["team_num"]

		if not force:
			check_results(self.tournament, self.raw_results)
		
		team_list_temp = []
		debater_list_temp = []

		debater_num_per_team = self.tournament.style["debater_num_per_team"]
		positions = len(self.tournament.style["score_weights"])
		score_weights = self.tournament.style["score_weights"]
		team_num = self.tournament.style["team_num"]

		"""
		raw_results['32'::debater_id] = [
			23: # uid of sender
			{
				"team_id": '3',
				"scores": [0, 0, 10],	#differ by each source
				"win_point": 1,
				"opponent_ids": 33,
				"position": 'gov'
			}
		]
		"""

		results_by_teams = {}

		for k, d in self.raw_results.items():#all data of each debater
			v = d.values()
			team = find_element_by_id(self.tournament.team_list, v[0]["team_id"])
			debater = find_element_by_id(team.debaters, k)
			opponent_ids = v[0]["opponent_ids"]
			opponents = tools.find_elements_by_ids(self.team_list, v[0]["opponent_ids"])
			win_point = v[0]["win_point"]
			position = v[0]["position"]
			score_list = get_score_list_averaged(v)
			score = get_weighted_score(score_list, score_weights)

			debater.finishing_process(score_list, score)

			if team in results_by_teams:
				results_by_teams[team]["score_lists"].append(score_list)
			else:
				results_by_teams[team] = {
					"opponent_ids": opponent_ids,
					"score_lists": [score_list],
					"position": position,
					"win_point": win_point
				}

		for k, v in results_by_teams.items():# calculate team score
			v["team_score"] = sum([sum(score_list) for score_list in v["score_lists"]])

		for k, v in results_by_teams.items():#calculate margin
			if team_num == 2:
				v["margin"] = 0
			else:
				opponent_score = results_by_teams[find_element_by_id(self.tournament.team_list, v["opponent_ids"][0])]["team_score"]
				v["margin"] = v["team_score"] - opponent_score

		for team, v in results_by_teams.items():
			team.finishing_process(opponents=opponents, score=v["team_score"], position=v["position"], win_point=v["win_point"], margin=v["margin"])

		rest_debater_list = [d for d in self.tournament.debater_list if d.code not in self.raw_results.keys()]
		for debater in rest_debater_list:
			debater.score_lists_sub.append(['n/a']*positions)
			debater.scores_sub.append('n/a')
			debater.rankings_sub.append('n/a')

		rest_team_list = [t for t in self.tournament.team_list if t not in results_by_teams.keys()]
		for team in rest_team_list:
			team.dummy_finishing_process()
			for debater in team.debaters:
				debater.dummy_finishing_process(style_cfg)
		self.__round_status = 11

	@this_round
	def process_result_of_adj(self, force=False):
		self.__round_status = 12
		if not force:
			check_results_of_adj(self.tournament, self.raw_results)

		"""
		raw_results_of_adj = {adj_id:[
			-24: #uid of result sender
			{
				"adj_id": data["adj_id"],
				"from": result["from"],	#differ in each result
				"from_id": result["from_id"],	#differ in each result
				"from_name": result["from_name"],	#differ in each result
				"chair": true if chair
				"point": result["point"],	#differ in each result
				"team_ids": result["team_ids"],
				"comment": result["comment"], #differ in each result
			}
		]}
		"""
		adjudicator_temp = []

		for k, d in self.raw_results_of_adj.items():
			v = d.values()
			if len(v) == 0:
				score = 0
			else:
				score = sum([d["score"] for d in v])/len(v)

			comments = [{"comment": d["comment"], "from": d["from"], "from_id": d["from_id"], "from_name": d["from_name"]} for d in v]
			adjudicator = find_element_by_id(self.tournament.adjudicator_list, k)
			adjudicator_temp.append(adjudicator)
			teams = [find_element_by_id(self.tournament.team_list, team_id) for team_id in v[0]["team_ids"]]
			chair = v[0]["chair"] 
			watched_debate_score = [t.score for t in teams]

			adjudicator.finishing_process(score=score, teams=teams, watched_debate_score=watched_debate_score, chair=chair, comments=comments)

		adjudicator_temp.sort(key=lambda adjudicator: adjudicator.watched_debate_score, reverse=True)

		for k, adjudicator in enumerate(adjudicator_temp):
			adjudicator.watched_debate_ranks.append(k+1)
			adjudicator.watched_debate_ranks_sub.append(k+1)

		rest_adjudicator_list = [adjudicator for adjudicator in self.tournament.adjudicator_list if adjudicator not in adjudicator_temp]

		for adj in rest_adjudicator_list:
			adj.watched_debate_ranks_sub.append('n/a')

		for adjudicator in rest_adjudicator_list:
			adjudicator.dummy_finishing_process(self.tournament.style["team_num"])
	
		self.__round_status = 13
