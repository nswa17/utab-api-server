# -*- coding: utf-8 -*-
import os
import json
import random
import copy

from subprocess import check_output

#from unittest import TestCase
#from nose.tools import eq_, ok_

with open(os.path.dirname(__file__)+'/../lib/server/dat/styles.json') as f:
	styles = json.load(f)

API_VERSION = 'v1.0'
JSON_FOLDER = 'jsons'
TOURNAMENT_NAME = 'testtournament'

##TODOs

def set_seed(x):
	random.seed(x)

def export_json(json, fname):
	if fname is not None:
		with open(JSON_FOLDER+'/'+fname, 'w') as f:
			f.write(json)

def send_data(path, api_version=API_VERSION, address='localhost', port=8080, json_file_name=None, errors=None, method='GET'):
	url = address+':'+str(port)+'/'+api_version+'/'+path
	if json_file_name is None:
		output = check_output("http "+method+" "+url, shell=True)
	else:
		output = check_output("http "+method+" "+url+" < "+JSON_FOLDER+'/'+json_file_name, shell=True)
	try:
		ret_val = json.loads(output.decode('utf-8'))
		return ret_val
	except:
		return output.decode('utf-8')

def jsonize(func):
	def _(*args, **kwargs):
		return json.dumps(func(*args, **kwargs))

	return _

@jsonize
def create_tournament(style, tournament_name, num_of_rounds):
	d = {
	    "args":
	    {
	      "force": False
	    },
	    "data": 
	    {
	        "url": "",
	        "name": tournament_name,
	        "style": style["style_name"],
	        "host": "Great TD",
	        "num_of_rounds": num_of_rounds,
	        "break_team_num": 0
	    }
	}	
	return d

@jsonize
def add_institution(code):
	d = {
		"name": "Insti"+str(code),
		"url": "",
		"scale": random.choice(["a", "b", "c"])
	}

	return d

@jsonize
def add_debater(code):
	d = {
		"name": "Debater"+str(code),
		"url": ""
	}

	return d

@jsonize
def add_team(code, institution_codes, debater_codes):
	d = {
		"name": "Team"+str(code),
		"institution_codes": institution_codes,
		"debater_codes": debater_codes,
		"url": "",
		"available": True
	}

	return d

@jsonize
def add_adjudicator(code, reputation, judge_test, institution_codes, conflict_codes):
	d = {
		"name": "Adj"+str(code),
		"reputation": reputation,
		"judge_test": judge_test,
		"institutions": institution_codes,
		"conflicts": conflict_codes,
		"url": "",
		"available": True
	}

	return d

@jsonize
def add_venue(code, priority):
	d = {
		"name": str(code),
		"url": "",
		"available": True,
		"priority": priority
	}

	return d

@jsonize
def set_judge_criterion(num_of_rounds):
	d = {
		"judge_criterion":
		[
			{
				"judge_test_percent":100,
		        "judge_repu_percent":0,
		        "judge_perf_percent":0
			}
		]*num_of_rounds
	}

	return d

@jsonize
def confirm_team_allocation(d):

	return d

@jsonize
def get_suggested_team_allocations():
	d = {
	"args": {"force": False}
	}

	return d

@jsonize
def confirm_adjudicator_allocation(d):

	return d

@jsonize
def confirm_venue_allocation(d):

	return d

@jsonize
def send_round_config():
	d = {
		"constants":
		{
			"random_pairing": 5,
			"des_power_pairing": 1,
			"des_w_o_same_a_insti": 2,
			"des_w_o_same_b_insti": 0,
			"des_w_o_same_c_insti": 0,
			"des_w_o_same_opp": 3,
			"des_with_fair_sides": 4
		},
		"constants_of_adj":
		{
			"random_allocation": 4,
			"des_strong_strong": 2,
			"des_with_fair_times": 3,
			"des_avoiding_conflicts": 1,
			"des_avoiding_past": 0,
			"des_priori_bubble": 0,
			"des_chair_rotation": 0
		}
	}

	return d

def generate_team_result(d, style, debater_result, num_teams):
	if style["team_num"] == 4:
		sides = ["og", "oo", "cg", "co"]
	else:
		sides = ["gov", "opp"]

	team_result = {}

	for grid in d:
		sides_cp = copy.copy(sides)
		random.shuffle(sides_cp)
		for team_id, side in zip(grid["teams"], sides_cp):
			team_result[team_id] = {}
			same_team_debaters = [style["debater_num_per_team"]*team_id + j for j in range(style["debater_num_per_team"])]
			team_result[team_id]["sum"] = sum([sum(debater_result[code]) for code in same_team_debaters])
			team_result[team_id]["side"] = side

		for team_id in grid["teams"]:
			if style["team_num"] == 2:
				other_team_id = copy.copy(grid["teams"])
				other_team_id.remove(team_id)
				other_team_id = other_team_id[0]

				team_result[team_id]["margin"] = team_result[team_id]["sum"] - team_result[other_team_id]["sum"]
			else:
				team_result[team_id]["margin"] = 0

		teams = copy.copy(grid["teams"])
		teams.sort(key=lambda code: team_result[code]["sum"])
		for i,team_id in enumerate(teams):
			team_result[team_id]["win"] = i

	return team_result

def generate_random_speaker_result(d, style, num_teams):
	if style["team_num"] == 4:
		sides = ["og", "oo", "cg", "co"]
	else:
		sides = ["gov", "opp"]

	debater_result = {}
	for team_id in range(num_teams):
		same_team_debaters = [style["debater_num_per_team"]*team_id + j for j in range(style["debater_num_per_team"])]

		roles = list(range(style["debater_num_per_team"]))
		random.shuffle(roles)
		reply_indices = style["replies"]
		random.shuffle(reply_indices)
		chosen_reply_indices = reply_indices[:style["num_of_replies"]]

		total_rep = 0
		for debater, role in zip(same_team_debaters, roles):
			score_list = [0] * len(style["score_weights"])
			score_list[role] = random.randint(73, 77)* style["score_weights"][role]
			if role in chosen_reply_indices:
				score_list[style["debater_num_per_team"]+total_rep] = random.randint(73, 77) * style["score_weights"][style["debater_num_per_team"]+total_rep]
				total_rep += 1
			debater_result[debater] = score_list

	return debater_result

def generate_adjudicator_result(d, style):#DONT CONSIDER ROLLING
	adjudicator_result = {}
	adj_id = 0
	for grid in d:
		watched_teams = grid["teams"]
		chair_base_score = random.randint(3,8)
		chair_scores = [chair_base_score + random.randint(-2,+2) for i in range(style["team_num"]+len(grid["panels"]))]
		adjudicator_result[adj_id] = {"scores": chair_scores, "watched_teams": watched_teams}
		adj_id += 1
		for panel in grid["panels"]:
			panel_base_score = random.randint(3,8)
			panel_scores = [panel_base_score]
			adjudicator_result[adj_id] = {"scores": panel_scores, "watched_teams": watched_teams}
			adj_id += 1
			
	return  adjudicator_result

@jsonize
def send_speaker_result(d, speaker_id, style):

	d = {
		"override": False,
		"result":
		{   
		    "from_id": 2,
		    "debater_id": 0,
		    "current_round": 1,
		    "team_id": 0,
	        "scores": [78, 0, 39],
	        "win_point": 1,
	        "opponents": [1],
	        "side": "gov"
	    }
	}





def export_and_send(func):
	def _(*args, **kwargs):
		fnames = func(*args, **kwargs)
		ret_vals = []
		path = args[0]
		if "method" in kwargs:
			method = kwargs["method"]
		else:
			method = 'GET'

		for i, fname in enumerate(fnames):
			if fname == "":
				fname = None
			if path[-1] == '/': 
				ret_vals.append(send_data(path=path+str(i), json_file_name=fname, method=kwargs["method"]))
			else:
				ret_vals.append(send_data(path=path, json_file_name=fname, method=kwargs["method"]))

		return ret_vals

	return _

@export_and_send
def create_tournament_exporter(path, style, tournament_name, num_of_rounds, fname="create_tournament", method='POST'):
	fnames = []
	TOURNAMENT_NAME = tournament_name
	j = create_tournament(style, tournament_name, num_of_rounds)
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames

@export_and_send
def add_institution_exporter(path, num_institutions, fname="add_institution", method='POST'):
	fnames = []
	for i in range(num_institutions):
		j = add_institution(i)
		_fname = fname+str(i)+'.json'
		export_json(j, _fname)
		fnames.append(_fname)

	return fnames

@export_and_send
def add_debater_exporter(path, num_debaters, fname="add_debater", method='POST'):
	fnames = []
	for i in range(num_debaters):
		j = add_debater(i)
		_fname = fname+str(i)+'.json'
		export_json(j, _fname)
		fnames.append(_fname)

	return fnames

@export_and_send
def add_team_exporter(path, num_teams, num_institutions, style, fname="add_team", method='POST'):
	fnames = []
	for i in range(num_teams):
		institution_codes = [random.choice(range(num_institutions))]
		debater_codes = [style["debater_num_per_team"]*i + j for j in range(style["debater_num_per_team"])]
		j = add_team(i, institution_codes, debater_codes)
		_fname = fname+str(i)+'.json'
		export_json(j, _fname)
		fnames.append(_fname)

	return fnames

@export_and_send
def add_adjudicator_exporter(path, num_adjudicators, num_teams, num_institutions, fname="JSON_FOLDER+add_adjudicator", method='POST'):
	fnames = []
	for i in range(num_adjudicators):
		reputation = random.choice(range(1, 10))
		judge_test = random.choice(range(1, 10))
		institution_codes = [random.choice(range(num_institutions))]
		conflict_codes = [random.choice(range(num_teams))] if random.random() < 0.1 else []

		j = add_adjudicator(i, reputation, judge_test, institution_codes, conflict_codes)
		_fname = fname+str(i)+'.json'
		export_json(j, _fname)
		fnames.append(_fname)

	return fnames

@export_and_send
def add_venue_exporter(path, num_venues, fname="add_venue", method='POST'):
	fnames = []
	for i in range(num_venues):
		priority = random.choice([1, 2, 3])
		j = add_venue(i, priority)
		_fname = fname+str(i)+'.json'
		export_json(j, _fname)
		fnames.append(_fname)

	return fnames

@export_and_send
def set_judge_criterion_exporter(path, num_of_rounds, fname="set_judge_criterion", method='PUT'):
	fnames = []
	j = set_judge_criterion(num_of_rounds)
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames

@export_and_send
def send_round_config_exporter(path, fname="send_round_config", method='PUT'):
	fnames = []
	j = send_round_config()
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames

@export_and_send
def get_suggested_team_allocations_exporter(path, fname="get_suggested_team_allocations", method='POST'):
	fnames = []
	j = get_suggested_team_allocations()
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames

@export_and_send
def confirm_team_allocation_exporter(path, d, fname="confirm_team_allocation", method='POST'):
	fnames = []
	j = confirm_team_allocation(d)
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames

@export_and_send
def get_suggested_adjudicator_allocations_exporter(path, fname="", method='GET'):
	return [""]

@export_and_send
def confirm_adjudicator_allocation_exporter(path, d, fname="", method='POST'):
	fnames = []
	j = confirm_adjudicator_allocations(d)
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames

@export_and_send
def get_suggested_venue_allocation_exporter(path, fname="", method='GET'):
	return [""]

@export_and_send
def confirm_venue_allocation_exporter(path, d, fname="", method='POST'):
	fnames = []
	j = confirm_venue_allocation(d)
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames

"""
print(send_data(path='testtournament/'+str(round_num)+'/suggested_team_allocations', json_file_name='get_suggested_team_allocations.json', method='POST'))
print(send_data(path='testtournament/'+str(round_num)+'/suggested_team_allocations/0', json_file_name='confirm_team_allocation.json', method='POST'))
print(send_data(path='testtournament/'+str(round_num)+'/suggested_adjudicator_allocations'))
print(send_data(path='testtournament/'+str(round_num)+'/suggested_adjudicator_allocations/0', json_file_name='confirm_adjudicator_allocation.json', method='POST'))
print(send_data(path='testtournament/'+str(round_num)+'/suggested_venue_allocation'))
print(send_data(path='testtournament/'+str(round_num)+'/suggested_venue_allocation', json_file_name='confirm_venue_allocation.json', method='POST'))

print(send_data(path='testtournament/'+str(round_num)+'/results/speakers', json_file_name='send_speaker_result1.json', method='PUT'))
print(send_data(path='testtournament/'+str(round_num)+'/results/speakers', json_file_name='send_speaker_result2.json', method='PUT'))
print(send_data(path='testtournament/'+str(round_num)+'/results/speakers', json_file_name='send_speaker_result3.json', method='PUT'))
print(send_data(path='testtournament/'+str(round_num)+'/results/speakers', json_file_name='send_speaker_result4.json', method='PUT'))
print(send_data(path='testtournament/'+str(round_num)+'/results/adjudicators', json_file_name='send_adjudicator_result1.json', method='PUT'))
print(send_data(path='testtournament/'+str(round_num)+'/results/adjudicators', json_file_name='send_adjudicator_result2.json', method='PUT'))
print(send_data(path='testtournament/'+str(round_num)+'/results/adjudicators', json_file_name='send_adjudicator_result3.json', method='PUT'))
print(send_data(path='testtournament/'+str(round_num), json_file_name='finish_round.json', method='POST'))
print(send_data(path='testtournament/results/teams', json_file_name='finish_round.json'))
print(send_data(path='testtournament/results/speakers', json_file_name='finish_round.json'))
print(send_data(path='testtournament/results/adjudicators', json_file_name='finish_round.json'))
"""

