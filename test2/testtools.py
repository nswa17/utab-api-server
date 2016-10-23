# -*- coding: utf-8 -*-
import os
import json
import random

from subprocess import check_output

#from unittest import TestCase
#from nose.tools import eq_, ok_

with open(os.path.dirname(__file__)+'/../lib/server/dat/styles.json') as f:
	styles = json.load(f)

API_VERSION = 'v0.1'
JSON_FOLDER = 'jsons'
TOURNAMENT_NAME = 'testtournament'

##TODOs

def set_seed(x):
	random.seed(x)

def export_json(json, fname):
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

def export_and_send(path, method='GET'):
	def _export_and_send(func):
		def _(*args, **kwargs):
			fnames = func(*args, **kwargs)
			ret_vals = []
			for i, fname in enumerate(fnames):
				if fname[-1] == '/': 
					ret_vals.append(send_data(path=path+str(i), json_file_name=fname, method=method))
				else:
					ret_vals.append(send_data(path=path+str(i), json_file_name=fname, method=method))

			return ret_vals

		return _

	return _export_and_send

@export_and_send('tournaments', method='POST')
def create_tournament_exporter(style, tournament_name, num_of_rounds, fname="create_tournament"):
	fnames = []
	TOURNAMENT_NAME = tournament_name
	j = create_tournament(style, tournament_name, num_of_rounds)
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames

@export_and_send(TOURNAMENT_NAME+'/institutions/', method='POST')
def add_institution_exporter(num_institutions, fname="add_institution"):
	fnames = []
	for i in range(num_institutions):
		j = add_institution(i)
		_fname = fname+str(i)+'.json'
		export_json(j, _fname)
		fnames.append(_fname)

	return fnames

@export_and_send(TOURNAMENT_NAME+'/speakers/', method='POST')
def add_debater_exporter(num_debaters, fname="add_debater"):
	fnames = []
	for i in range(num_debaters):
		j = add_debater(i)
		_fname = fname+str(i)+'.json'
		export_json(j, _fname)
		fnames.append(_fname)

	return fnames

@export_and_send(TOURNAMENT_NAME+'/teams/', method='POST')
def add_team_exporter(num_teams, num_institutions, style, fname="add_team"):
	fnames = []
	for i in range(num_teams):
		institution_codes = [random.choice(range(num_institutions))]
		debater_codes = [style["debater_num_per_team"]*i + j for j in range(style["debater_num_per_team"])]
		j = add_team(i, institution_codes, debater_codes)
		_fname = fname+str(i)+'.json'
		export_json(j, _fname)
		fnames.append(_fname)

	return fnames

@export_and_send(TOURNAMENT_NAME+'/adjudicators/', method='POST')
def add_adjudicator_exporter(num_adjudicators, num_teams, num_institutions, fname="JSON_FOLDER+add_adjudicator"):
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

@export_and_send(TOURNAMENT_NAME+'/venues/', method='POST')
def add_venue_exporter(num_venues, fname="add_venue"):
	fnames = []
	for i in range(num_venues):
		priority = random.choice([1, 2, 3])
		j = add_venue(i, priority)
		_fname = fname+str(i)+'.json'
		export_json(j, _fname)
		fnames.append(_fname)

	return fnames

@export_and_send(TOURNAMENT_NAME, method='PUT')
def set_judge_criterion_exporter(num_of_rounds, fname="set_judge_criterion"):
	fnames = []
	j = set_judge_criterion(num_of_rounds)
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames
	
"""
@export_and_send(TOURNAMENT_NAME+, method='PUT')
def get_suggested_team_allocations_exporter(force=False, fname="get_suggested_team_allocations"):
	fnames = []
	j = get_suggested_team_allocations(force)
	_fname = fname+'.json'
	export_json(j, _fname)
	fnames.append(_fname)

	return fnames

"""
"""

print(send_data('tournaments', json_file_name='create_tournament.json', method='POST'))
print(send_data('testtournament/institutions/0', json_file_name='add_institution1.json', method='POST'))
print(send_data('testtournament/institutions/1', json_file_name='add_institution2.json', method='POST'))
print(send_data('testtournament/institutions/2', json_file_name='add_institution3.json', method='POST'))
"""
"""
t3 = Thread(target=send_data, kwargs={'path':'testtournament/speakers/1', 'json_file_name':'add_debater1.json', 'method':'POST'})
t4 = Thread(target=send_data, kwargs={'path':'testtournament/speakers/2', 'json_file_name':'add_debater2.json', 'method':'POST'})
t5 = Thread(target=send_data, kwargs={'path':'testtournament/speakers/3', 'json_file_name':'add_debater3.json', 'method':'POST'})
t6 = Thread(target=send_data, kwargs={'path':'testtournament/speakers/4', 'json_file_name':'add_debater4.json', 'method':'POST'})
t3.start()
t4.start()
t5.start()
t6.start()
"""
"""
print(send_data('testtournament/speakers/0', json_file_name='add_debater1.json', method='POST'))
print(send_data('testtournament/speakers/1', json_file_name='add_debater2.json', method='POST'))
print(send_data('testtournament/speakers/2', json_file_name='add_debater3.json', method='POST'))
print(send_data('testtournament/speakers/3', json_file_name='add_debater4.json', method='POST'))


print(send_data('testtournament/teams/0', json_file_name='add_team1.json', method='POST'))
print(send_data('testtournament/teams/1', json_file_name='add_team2.json', method='POST'))
print(send_data('testtournament/adjudicators/0', json_file_name='add_adjudicator1.json', method='POST'))
print(send_data('testtournament/adjudicators/1', json_file_name='add_adjudicator2.json', method='POST'))
print(send_data('testtournament/adjudicators/2', json_file_name='add_adjudicator3.json', method='POST'))
print(send_data('testtournament/venues/0', json_file_name='add_venue1.json', method='POST'))
print(send_data('testtournament', json_file_name='set_judge_criterion.json', method='PUT'))

for round_num in range(1, 3):
	print(send_data('testtournament/'+str(round_num), json_file_name='send_round_config.json', method='PUT'))
	
"""
"""
	t3 = Thread(target=send_data, kwargs={'path':'testtournament/0/suggested_team_allocations', 'json_file_name':'get_suggested_team_allocations.json', 'method':'POST'})
	t4 = Thread(target=send_data, kwargs={'path':'testtournament/0/suggested_team_allocations', 'json_file_name':'get_suggested_team_allocations.json', 'method':'POST'})
	t5 = Thread(target=send_data, kwargs={'path':'testtournament/0/suggested_team_allocations', 'json_file_name':'get_suggested_team_allocations.json', 'method':'POST'})
	t3.start()
	t4.start()
	t5.start()	
"""
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

