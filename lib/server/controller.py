# -*- coding: utf-8 -*-
from bottle import HTTPResponse
from threading import Lock
import json
import datetime
import pickle

import sys
import os

BACKUP_FOLDER = 'share'

with open(os.path.dirname(__file__)+'/dat/styles.json') as f:
	styles = json.load(f)

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, path)

import utab.tournament as tn
import utab.src.tools as tools
import server.src.stools as stools

tournaments = {
}


backups = {}

common_lock = Lock()

def list_styles():
	data = []
	errors = []
	for v in styles.values():
		data.append(
			{"style_name": v["style_name"],
			"debater_num_per_team": v["debater_num_per_team"],
			"team_num": v["team_num"],
			"score_weights": v["score_weights"],
			"replies": v["replies"],
			"num_of_replies": v["num_of_replies"]
			})

	return data, errors

@stools.lock_with(common_lock)
def add_style(req):
	data = {}
	errors = []

	if req["style_name"] not in styles:
		errors.append(stools.set_error(200, "style already exists", ""))
	else:
		styles[req["style_name"]] = {
			"style_name": req["style_name"],
			"debater_num_per_team": req["debater_num_per_team"],
			"team_num": req["team_num"],
			"score_weights": req["score_weights"],
			"replies": req["replies"],
			"num_of_replies": req["num_of_replies_per_team"]
			}

	return data, errors

def list_tournaments():
	data = []
	errors = []
	data["tournaments"] = []
	for tournament in tournaments:
		data.append(
		{
			"name": tournament.name,
			"code": tournament.code,
			"num_of_rounds": tournament.round_num,
			"style": tournament.style,
			"url": tournament.url,
			"judge_criterion": tournament.judge_criterion
		})

	return data, errors

def fetch_tournament(tournament_name):
	errors = []
	data = []
	if tournament_name not in tournaments:
		errors.append(stools.set_error(500, "tournament not found"))
	else:
		data = {
			"url": tournaments[data["tournament"]].url,
			"id": tournaments[data["tournament"]].code,
			"name": tournaments[data["tournament"]].name,
			"style": tournaments[data["tournament"]].style,
			"host": tournaments[data["tournament"]].host,
			"judge_criterion": tournaments[data["tournament"]].judge_criterion
		}		

	return data, errors

def create_backup_folder(path):
	os.makedirs(path)

def read_backup_dict(path):
	with open(path, 'r') as f:
		backup_dict = json.load(f)

	return backup_dict

@stools.lock_with(common_lock)
def initialize_backups():
	path = './'+BACKUP_FOLDER+'/backup_dict.json'
	return read_backup_dict(path)

def save_backup_dict(path, backup_dict):
	with open(path, 'w') as f:
		json.dump(backup_dict, f)

@stools.lock_with(common_lock)
def save_backup(tournament_name, req):
	errors = []
	t = tournaments[tournament_name]
	today =  datetime.datetime.today()
	nowtime = today.strftime("%Y%m%d%H%M%S")

	backup_dict_path = './'+BACKUP_FOLDER+'/backup_dict.json'
	folder_path = './'+BACKUP_FOLDER+'/'+t.name

	backup_dict = read_backup_dict(backup_dict_path)

	with open(folder_path+'/'+nowtime, 'wb') as f:
		pickle.dump(t, f)

	data = {
		"name": t.name,
		"date": nowtime,
		"comment": req["comment"],
		"current_round": t.now_round_num()
	}

	if t.name not in backups:
		backups[t.name] = [data]
	else:
		backups[t.name].append(data)
	if t.name not in backup_dict:
		backup_dict[t.name] = [data]
	else:
		backup_dict[t.name].append(data)

	save_backup_dict(backup_dict_path, backup_dict)

	return data, errors

def list_backups(tournament_name):
	errors = []
	t = tournaments[tournament_name]
	if t.name not in backups:
		data = []
	else:
		data = backups[t.name]

	return data, errors

@stools.lock_with(common_lock)
def import_backup(tournament_name, req):
	data = []
	errors = []
	t = tournaments[tournament_name]
	date = req['date']
	name = req['name']

	file_path = './'+BACKUP_FOLDER+'/'+name+'/'+date
	with open(file_path, 'rb') as f:
		loaded_tournament = pickle.load(f)

	tournaments[tournament_name] = loaded_tournament

	return data, errors

@stools.lock_with(common_lock)
def create_tournament(req):######################
	errors = []
	data = {}

	if req["name"] in tournaments.keys():
		errors.append(stools.set_error(0, "AlreadyExists", "The tournament name is already used."))#set_json_error_response(0, "AlreadyExists", "The tournament name is already used.") 
	else:
		name = req["name"]
		round_num = req["num_of_rounds"]
		style = styles[req["style"]]
		url = req["url"]
		host = req["host"]
		break_team_num = req["break_team_num"]
		new_tournament = tn.Tournament(name=name, code=len(tournaments), round_num=round_num, style=style, host=host, url=url, break_team_num=break_team_num)
		tournaments[name] = new_tournament

		data["id"] = new_tournament.code
		data["name"] = new_tournament.name
		data["num_of_rounds"] = new_tournament.round_num
		data["style"] = new_tournament.style
		data["host"] = new_tournament.host
		data["url"] = new_tournament.url
		data["judge_criterion"] = new_tournament.judge_criterion
		data["break_team_num"] = new_tournament.break_team_num

		folder_path = './'+BACKUP_FOLDER+'/'+str(new_tournament.name)
		if not os.path.isdir(folder_path):
			create_backup_folder(folder_path)

	return data, errors

def fetch_round(tournament_name, round_num):
	data = {}
	errors = []
	if round_num not in range(1, len(tournaments[tournament_name].round_num)+1):
		errors.append(stools.set_error(500, "round num not found", ""))########################
	else:
		_round = tournaments[tournament_name].now_round()
		data = {
	        "num_of_rounds": tournaments[tournament_name].round_num,
	        "status": _round.round_status,
	        "constants": _round.constants,
	        "constants_of_adj": _round.constants_of_adj
	    }

	return data, errors

@stools.lock_with(common_lock)
def send_round_config(tournament_name, round_num, req):
	data = {}
	errors = []
	r = tournaments[tournament_name].now_round()
	constants = req["constants"]
	constants_of_adj = req["constants_of_adj"]
	r.set_constants(constants["random_pairing"], constants["des_power_pairing"], constants["des_w_o_same_a_insti"], constants["des_w_o_same_b_insti"], constants["des_w_o_same_c_insti"], constants["des_w_o_same_opp"], constants["des_with_fair_sides"])
	r.set_constants_of_adj(constants_of_adj["random_allocation"], constants_of_adj["des_strong_strong"], constants_of_adj["des_with_fair_times"], constants_of_adj["des_avoiding_conflicts"], constants_of_adj["des_avoiding_past"], constants_of_adj["des_priori_bubble"], constants_of_adj["des_chair_rotation"])

	data["constants"] = r.constants
	data["constants_of_adj"] = r.constants_of_adj

	return data, errors

@stools.lock_with(common_lock)
def finish_round(tournament_name, round_num, req):
	errors = []
	data = {}
	r = tournaments[tournament_name].now_round()
	r.end(force=req["args"]["force"])

	return data, errors

@stools.lock_with(common_lock)
def create_style(req):
	data = {}
	errors = []
	styles[data["style_name"]] = {"style_name": data["style_name"], "style_name": data["debater_num_per_team"], "team_num": data["team_num"], "score_weights": data["score_weights"], "replies": data["replies"], "num_of_replies": data["num_of_replies_per_team"]}
	data["style_name"] = styles["style_name"]
	data["debater_num_per_team"] = styles["debater_num_per_team"]
	data["team_num"] = styles["team_num"]
	data["score_weights"] = styles["score_weights"]
	data["replies"] = styles["replies"]
	data["num_of_replies"] = styles["num_of_replies"]
	return data, errors

@stools.lock_with(common_lock)
def get_suggested_team_allocations(tournament_name, round_num, req):
	errors = []
	tournament = tournaments[tournament_name]
	r = tournament.start_round(force=req["args"]["force"])
	r.compute_matchups()
	data = r.respond_matchups()

	return data, errors

@stools.lock_with(common_lock)
def check_team_allocation(tournament_name, round_num, req):
	data = []
	errors = []
	r = tournaments[tournament_name].now_round()
	selected_grid_list, code = r.add_imported_matchup(req)
	data = r.respond_matchup(code)

	return data, errors

@stools.lock_with(common_lock)
def confirm_team_allocation(tournament_name, round_num, allocation_id, req):
	data = []
	errors = []
	r = tournaments[tournament_name].now_round()
	selected_grid_list, code = r.add_imported_matchup(req)

	r.set_matchup(selected_grid_list)
	data = r.respond_matchup()

	return data, errors

@stools.lock_with(common_lock)
def get_suggested_adjudicator_allocations(tournament_name, round_num):
	errors = []
	r = tournaments[tournament_name].now_round()
	r.compute_allocations()
	data = r.respond_allocations()

	return data, errors

@stools.lock_with(common_lock)
def check_adjudicator_allocation(tournament_name, round_num, req):
	data = []
	errors = []
	r = tournaments[tournament_name].now_round()
	selected_lattice_list, code = r.add_imported_allocation(req)
	data = r.respond_allocation(code)

	return data, errors

@stools.lock_with(common_lock)
def confirm_adjudicator_allocation(tournament_name, round_num, allocation_id, req):
	errors = []
	r = tournaments[tournament_name].now_round()
	selected_lattice_list, code = r.add_imported_allocation(req)
	r.set_allocation(selected_lattice_list)
	data = r.respond_allocation()

	return data, errors

@stools.lock_with(common_lock)
def get_suggested_venue_allocation(tournament_name, round_num):
	errors = []
	r = tournaments[tournament_name].now_round()
	r.compute_venue_allocation()
	data = r.respond_allocation()

	return data, errors

@stools.lock_with(common_lock)
def confirm_venue_allocation(tournament_name, round_num, req):
	errors = []
	r = tournaments[tournament_name].now_round()
	selected_lattice_list, code = r.add_imported_allocation(req)
	r.set_allocation(selected_lattice_list)
	data = r.respond_allocation()

	return data, errors

@stools.lock_with(common_lock)
def add_adjudicator(tournament_name, req):
	data = {}
	errors = []

	adj = tournaments[tournament_name].add_adjudicator(name=req["name"], reputation=req["reputation"], judge_test=req["judge_test"], institution_codes=req["institutions"], conflict_team_codes=req["conflicts"], url=req["url"], available=req["available"])
	data["name"] = adj.name
	data["id"] = adj.code
	data["reputation"] = adj.reputation
	data["judge_test"] = adj.judge_test
	data["institution_ids"] = [i.code for i in adj.institutions]
	data["conflict_team_ids"] = [t.code for t in adj.conflict_teams]
	data["url"] = adj.url
	data["available"] = not adj.absent
	return data, errors

def fetch_adjudicator(tournament_name, adjudicator_id):
	errors = []
	t = tournaments[tournament_name]
	data = t.fetch_adjudicator(adjudicator_id)
	data["id"] = data["code"]
	del data["code"]

	return data, errors

def list_adjudicators(tournament_name):
	errors = []
	t = tournaments[tournament_name]
	data = t.list_adjudicators()
	for ele in data:
		ele["id"] = ele["code"]
		del ele["code"]

	return data, errors

@stools.lock_with(common_lock)
def add_team(tournament_name, req):
	data = {}
	errors = []

	team = tournaments[tournament_name].add_team(name=req["name"], institution_codes=req["institution_codes"], debater_codes=req["debater_codes"], url=req["url"], available=req["available"])
	data["id"] = team.code
	data["name"] = team.name
	data["institution_ids"] = [i.code for i in team.institutions]
	data["debater_ids"] = [i.code for i in team.debaters]
	data["url"] = team.url
	data["available"] = team.available
	return data, errors

def fetch_team(tournament_name, team_id):
	errors = []
	t = tournaments[tournament_name]
	data = t.fetch_team(team_id)
	data["id"] = data["code"]
	del data["code"]

	return data, errors

def list_teams(tournament_name):
	errors = []
	t = tournaments[tournament_name]
	data = t.list_teams()
	for ele in data:
		ele["id"] = ele["code"]
		del ele["code"]

	return data, errors

@stools.lock_with(common_lock)
def add_speaker(tournament_name, req):
	data = {}
	errors = []

	debater = tournaments[tournament_name].add_debater(name=req["name"], url=req["url"])
	data["id"] = debater.code
	data["name"] = debater.name
	data["url"] = debater.url

	return data, errors

def fetch_speaker(tournament_name, speaker_id):
	errors = []
	t = tournaments[tournament_name]
	data = t.fetch_debater(speaker_id)
	data["id"] = data["code"]
	del data["code"]

	return data, errors

def list_speakers(tournament_name):
	errors = []
	t = tournaments[tournament_name]
	data = t.list_debaters()
	for ele in data:
		ele["id"] = ele["code"]
		del ele["code"]

	return data, errors

@stools.lock_with(common_lock)
def add_venue(tournament_name, req):
	data = {}
	errors = []

	venue = tournaments[tournament_name].add_venue(name=req["name"], url=req["url"], available=req["available"], priority=req["priority"])
	data["id"] = venue.code
	data["name"] = venue.name
	data["available"] = venue.available
	data["priority"] = venue.priority
	data["url"] = venue.url
	return data, errors

def fetch_venue(tournament_name, venue_id):
	errors = []
	t = tournaments[tournament_name]
	data = t.fetch_venue(venue_id)
	data["id"] = data["code"]
	del data["code"]

	return data, errors

def list_venues(tournament_name):
	errors = []
	t = tournaments[tournament_name]
	data = t.list_venues()
	for ele in data:
		ele["id"] = ele["code"]
		del ele["code"]

	return data, errors

@stools.lock_with(common_lock)
def add_institution(tournament_name, req):
	data = {}
	errors = []

	institution = tournaments[tournament_name].add_institution(name=req["name"], url=req["url"], scale=req["scale"])
	data["id"] = institution.code
	data["name"] = institution.name
	data["url"] = institution.url
	data["scale"] = institution.scale
	return data, errors

def fetch_institution(tournament_name, institution_id):
	errors = []
	t = tournaments[tournament_name]
	data = t.fetch_institution(institution_id)
	data["id"] = data["code"]
	del data["code"]

	return data, errors

def list_institutions(tournament_name):
	errors = []
	t = tournaments[tournament_name]
	data = t.list_institutions()
	for ele in data:
		ele["id"] = ele["code"]
		del ele["code"]

	return data, errors

@stools.lock_with(common_lock)
def set_judge_criterion(tournament_name, req):
	data = []
	errors = []

	judge_criterion = tournaments[tournament_name].add_judge_criterion(req["judge_criterion"])
	for criteria in judge_criterion:
		data.append(
		{
			"judge_test_percent":criteria["judge_test_percent"],
		    "judge_repu_percent":criteria["judge_repu_percent"],
		    "judge_perf_percent":criteria["judge_perf_percent"]
		})

	return data, errors

@stools.lock_with(common_lock)
def send_speaker_result(tournament_name, round_num, req):
	data = []
	errors = []
	r = tournaments[tournament_name].now_round()
	req["result"]["opponent_ids"] = req["result"]["opponents"]
	req["result"]["position"] = req["result"]["side"]
	uid = req["result"]["from_id"]
	data = r.set_result(req["result"], uid, override = req["override"])

	return data, errors

@stools.lock_with(common_lock)
def send_adjudicator_result(tournament_name, round_num, req):
	data = []
	errors = []
	r = tournaments[tournament_name].now_round()
	req["result"]["team_ids"] = req["result"]["teams"]

	uid = req["result"]["from_id"] if req["result"]["from"] == 'team' else -req["result"]["from_id"]
	data = r.set_result_of_adj(req["result"], uid, override = req["override"])

	return data, errors

def download_total_speaker_results(tournament_name):
	errors = []
	t = tournaments[tournament_name]
	data = t.total_debater_results()
	for d in data.values():
		d['id'] = d['code']
		del d['code']

	return data, errors

def download_total_team_results(tournament_name):
	errors = []
	t = tournaments[tournament_name]
	data = t.total_team_results()
	for d in data.values():
		d['id'] = d['code']
		del d['code']

	return data, errors

def download_total_adjudicator_results(tournament_name):
	errors = []
	t = tournaments[tournament_name]
	data = t.total_adjudicator_results()
	for d in data.values():
		d['id'] = d['code']
		del d['code']

	return data, errors

