from .bit import *
from .internal import *
from .entity_classes import *
from .result import *

import time

class Tournament:
	def __init__(self, name, code, round_num, style=None, host = "", url = "", break_team_num = 0):
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
		#self.results = None
		self.analysis = None

	def round(self):
		return self.rounds[self.now_round-1]

	def set_judge_criterion(self, judge_criterion_dicts):
		self.judge_criterion = judge_criterion_dicts

	def add_team(self, code, name, debaters, institutions, url=""):
		team = Team(code, name, url, debaters,  institutions)
		add_element(self.team_list, team)

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

	def add_adjudicator(self, code, name, reputation, judge_test, institutions, conflict_teams, url=""):
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
		venue = Venue(code, name, url, available, priority)
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
		self.grid_list = Grid_list()
		self.lattice_list = None
		self.candidate_matchups = None
		self.candidate_allocations = None
		self.candidate_panel_allocation = None
		self.candidate_venue_allocation = None
		self.matchup = None
		self.allocation = None
		self.panel_allocation = None
		self.venue_allocation = None
		self.round_status = 0
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

	def set(self, force = False):
		if self.tournament.now_round != self.r:
			raise Exception("prior round is not finished")
			
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

	def compute_matchups(self):
		self.round_status = 1
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
		self.round_status = 2

	def set_matchup(self, matchup):
		self.matchup = matchup

	def compute_allocations(self):
		self.round_status = 3
		self.lattice_list = create_lattice_list(self.matchup, self.tournament.adjudicator_list)
		self.candidate_allocations = create_allocations(tournament=self.tournament, selected_grid_list=self.matchup, lattice_list=self.lattice_list, round_num=self.r, filter_list=self.filter_of_adj_list)
		self.round_status = 4

	def set_allocation(self, allocation):
		self.allocation = allocation

	def compute_venue_allocation(self):
		self.round_status = 7
		available_venue_list = [venue for venue in self.tournament.venue_list if venue.available]
		random.shuffle(available_venue_list)
		available_venue_list.sort(key=lambda venue:venue.priority)
		for lattice, venue in zip(self.allocation, available_venue_list):
			lattice.venue = venue
		#print(len(available_venue_list))
		#print(len(allocations))
		self.allocation.sort(key=lambda lattice: lattice.venue.name)
		self.round_status = 8

	def set_venue_allocation(self, venue_allocation):
		self.venue_allocation = venue_allocation

	def compute_panel_allocation(self):
		self.round_status = 5
		for lattice in self.allocation:
			for adjudicator in self.tournament.adjudicator_list:
				if adjudicator.name == lattice.chair.name:
					adjudicator.active = True
					break

		self.allocation.large_warnings = []

		inactive_adjudicator_list = [adjudicator for adjudicator in self.tournament.adjudicator_list if (not(adjudicator.active) and not(adjudicator.absent))]
		inactive_adjudicator_list.sort(key=lambda adjudicator:adjudicator.evaluation, reverse=True)

		if self.tournament.style["team_num"] == 2:
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

		self.round_status = 6

	def set_panel_allocation(self, panel_allocation):
		self.panel_allocation = panel_allocation

	def set_result(self, data, override = False):
		self.round_status = 9
		result = data["result"]
		debater_id = data["debater_id"]
		result_to_set = {
			"debater_id": debater_id,
			"team_id": result["team_id"],
			"scores": result["scores"],
			"win_point": result["win_point"],
			"opponent_ids": result["opponent_ids"],
			"position": result["position"]
		}

		check_result(self.tournament, result_to_set)

		if debater_id in self.raw_results:
			self.raw_results[debater_id].append(result_to_set)
		else:
			self.raw_results[debater_id] = [result_to_set]

	def set_result_of_adj(self, data, override = False):
		self.round_status = 9
		result = data["result"]
		adj_id = data["adj_id"]
		result_to_set = {
			"adj_id": adj_id,
			"from": result["from"],
			"from_id": result["from_id"],
			"from_name": result["from_name"],
			"chair": result["chair"],
			"point": result["point"],
			"team_ids": result["team_ids"],
			"comment": result["comment"],
		}

		check_result_of_adj(self.tournament, result_to_set)

		if adj_id in self.raw_results_of_adj:
			self.raw_results_of_adj[adj_id].append(result_to_set)
		else:
			self.raw_results_of_adj[adj_id] = [result_to_set]

	def end(self, force = False):
		if not force:
			check_team_list2(self.tournament.team_list, self.tournament.now_round, self.tournament.style["team_num"])

		self.tournament.now_round += 1
		self.round_status = 14

	def process_result(self, force=False):
		self.round_status = 10
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

		for k, v in self.raw_results.items():#all data of each debater
			team = find_element_by_id(self.tournament.team_list, v[0]["team_id"])
			debater = find_element_by_id(team.debaters, k)
			opponent_ids = v[0]["opponent_ids"]
			opponents = [get_name_from_id(self.tournament.team_list, opponent_id) for opponent_id in v[0]["opponent_ids"]]
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
		self.round_status = 11

	def process_result_of_adj(self, force=False):
		self.round_status = 12
		if not force:
			check_results_of_adj(self.tournament, self.raw_results)

		"""
		raw_results_of_adj = {adj_id:[
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

		for k, v in self.raw_results_of_adj.items():
			if len(v) == 0:
				score = 0
			else:
				score = sum([d["point"] for d in v])/len(v)

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
	
		self.round_status = 13
