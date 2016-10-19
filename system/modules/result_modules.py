import shutil
import csv
import sys
import os
import copy
import itertools
import re
from .tools import *

def check_result(tournament, result):
	### check whether the debater id belongs to the team id in dictionary
	team = find_element_by_id(tournament.team_list, result["team_id"])

	if not team.is_belonging(result["debater_id"]):
		raise Exception("debater_id {} 's team doesn't have team_id {}".format(result["debater_id"], result["team_id"]))
	### check if the score is not all zero

def check_results(tournament, raw_results):########
	regexp = re.compile(r'^[0-9A-Za-z. ¥-]+$')

	results_lists = []

	positions = len(tournament.style["score_weights"])
	team_num = tournament.style["team_num"]
	debater_num_per_team = tournament.style["debater_num_per_team"]

	team_codes_posted = []
	for v in raw_results.values():
		for d in v:
			team_codes_posted.append(d["team_id"])

	for team in tournament.team_list:
		if team.code not in team_codes_posted and team.available:
			raise Exception("result of team {} is not sent".format(team.name))

	debater_codes_posted = [k for k in raw_results.keys()]

	for debater in tournament.debater_list:
		if debater.code not in debater_codes_posted and debater.team.available:
			raise Exception("result of debater {} is not sent".format(debater.name))

	"""
	raw_results['32'::debater_id] = [{
			"team_id": '3',
			"scores": [0, 0, 10],
			"win_point": 1,
			"opponent_ids": 33,
			"position": 'gov'
			}]
	"""

	### check same team has same wins/sides
	### us for the opponent is the oppnent for them
	### collected all results?

def get_weighted_score(score_list, score_weights):
	score = 0
	sum_weight = 0
	for sc, weight in zip(score_list, score_weights):
		if sc != 0:
			score += sc
			sum_weight += weight

	score = 0 if sum_weight == 0 else score / sum_weight
	return score

def get_score_list_averaged(result_dicts):
	score_list = []#array for scores [8(pm), 0(mg), 4(gr)]
	num_sources = len(result_dicts)
	for result_dict in result_dicts:
		if score_list == []:
			score_list = result_dict["scores"]
		else:
			score_list = [score_list[i] + result_dict["scores"][i] for i in range(len(result_dict["scores"]))]

	return [score/num_sources for score in score_list]

def check_result_of_adj(tournament, result):
	if result["from"] == 'chair' or result["from"] == 'panel':
		from_adj = find_element_by_id(tournament.adjudicator_list, result["from_id"])
		if result["from_name"] != from_adj.name:
			raise Exception("sender's id and name doesn't match")

def check_results_of_adj(tournament, raw_results):
	pass


