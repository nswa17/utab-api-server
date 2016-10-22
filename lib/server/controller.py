# -*- coding: utf-8 -*-
from bottle import HTTPResponse
from threading import Lock

import sys
import os

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, path)

import utab.tournament as tn
import utab.src.tools as tools
import server.src.stools as stools

common_lock = Lock()

def list_all_styles():
	data = []
	errors = []
	for v in tn.styles.values():
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

	if req["style_name"] not in tn.styles:
		errors.append(stools.set_error(200, "style already exists", ""))
	else:
		tn.styles[req["style_name"]] = {
			"style_name": req["style_name"],
			"debater_num_per_team": req["debater_num_per_team"],
			"team_num": req["team_num"],
			"score_weights": req["score_weights"],
			"replies": req["replies"],
			"num_of_replies": req["num_of_replies_per_team"]
			}

	return data, errors

def list_all_tournaments():
	data = {}
	errors = []
	data["tournaments"] = []
	for tournament in tn.tournaments:
		data["tournaments"].append(
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
	data = {}
	if tournament_name not in tn.tournaments:
		errors.append(stools.set_error(500, "tournament not found"))
	else:
		data["tournament"] = {
			"url": tn.tournaments[data["tournament"]].url,
			"id": tn.tournaments[data["tournament"]].code,
			"name": tn.tournaments[data["tournament"]].name,
			"style": tn.tournaments[data["tournament"]].style,
			"host": tn.tournaments[data["tournament"]].host,
			"judge_criterion": tn.tournaments[data["tournament"]].judge_criterion
		}		

	return data, errors

@stools.lock_with(common_lock)
def create_tournament(req):######################
	errors = []
	data = {}

	if req["data"]["name"] in tn.tournaments.keys():
		errors.append(stools.set_error(0, "AlreadyExists", "The tournament name is already used."))#set_json_error_response(0, "AlreadyExists", "The tournament name is already used.") 
	else:
		name = req["data"]["name"]
		new_tournament = tn.Tournament(req["data"]["name"], len(tn.tournaments)+1, req["data"]["num_of_rounds"], req["data"]["style"])
		tn.tournaments[name] = new_tournament

		data["id"] = new_tournament.code
		data["name"] = new_tournament.name
		data["num_of_rounds"] = new_tournament.round_num
		data["style"] = new_tournament.style

	return data, errors

def fetch_round(tournament_name, round_num):
	data = {}
	errors = []
	if round_num not in range(1, len(tn.tournaments[tournament_name].round_num)+1):
		errors.append(stools.set_error(500, "round num not found", ""))########################
	else:
		_round = tn.tournaments[tournament_name].rounds[round_num-1]
		data["round_info"] = {
	        "num_of_rounds": tn.tournaments[tournament_name].round_num,
	        "status": _round.round_status,
	        "constants": _round.constants,
	        "constants_of_adj": _round.constants_of_adj
	    }

	return data, errors

@stools.lock_with(common_lock)
def create_style(req):
	data = req
	errors = []
	tn.styles[data["style_name"]] = {"style_name": data["style_name"], "style_name": data["debater_num_per_team"], "team_num": data["team_num"], "score_weights": data["score_weights"], "replies": data["replies"], "num_of_replies": data["num_of_replies_per_team"]}

	return data, errors

@stools.lock_with(common_lock)
def add_adjudicator(tournament_name, req):
	data = {}
	errors = []

	adj = tn.tournaments[tournament_name].add_adjudicator(name=req["name"], reputation=req["reputation"], judge_test=req["judge_test"], institution_codes=req["institutions"], conflict_team_codes=req["conflicts"], url=req["url"], available=req["available"])

	return data, errors

@stools.lock_with(common_lock)
def add_team(tournament_name, req):
	data = {}
	errors = []

	team = tn.tournaments[tournament_name].add_team(name=req["name"], institution_codes=req["institution_codes"], debater_codes=req["debater_codes"], url=req["url"], available=req["available"])
	data["a"] = ""#######################################################
	return data, errors

@stools.lock_with(common_lock)
def add_speaker(tournament_name, req):
	data = {}
	errors = []

	debater = tn.tournaments[tournament_name].add_debater(name=req["name"], url=req["url"])

	return data, errors

@stools.lock_with(common_lock)
def add_venue(tournament_name, req):
	data = {}
	errors = []

	venue = tn.tournaments[tournament_name].add_venue(name=req["name"], url=req["url"], available=req["available"], priority=req["priority"])

	return data, errors

@stools.lock_with(common_lock)
def add_institution(tournament_name, req):
	data = {}
	errors = []

	institution = tn.tournaments[tournament_name].add_institution(name=req["name"], url=req["url"], scale=req["scale"])

	return data, errors

@stools.lock_with(common_lock)
def set_judge_criterion(tournament_name, req):
	data = {}
	errors = []

	judge_criterion = tn.tournaments[tournament_name].add_judge_criterion(req["judge_criterion"])

	return data, errors
