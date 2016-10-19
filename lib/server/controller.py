# -*- coding: utf-8 -*-
from bottle import HTTPResponse

import sys
import os

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, path)

import utab.tournament

def list_all_teams(team_list):
	errors = []
	data = {}
	for team in team_list:
		data[team.name] = {"id":team.code, "name":team_name, "url":team.url}
	return data, errors

def list_all_tournaments():
	data = {}
	errors = []
	return data, errors

"""
def set_json_error_response(status_code, status_text, message):
	return set_json_response(errors=set_error(status_code, status_text, message))
"""

def set_error(status_code, status_text, message):
	error = {}
	error["statusCode"] = status_code
	error["statusText"] = status_text
	error["message"] = message

	return error

def create_tournament(req):
	errors = []
	data = {}

	try:
		name = req["name"]
		style = req["style"]
		round_num = req["round_num"]
	except KeyError:
		errors.append(set_error(0, "KeyError", "Data sent has no key named name/style/round_num."))#set_json_error_response(0, "KeyError", "Data sent has no key named name/style/round_num.")
		return data, errors
	if req["name"] in tournaments.keys():
		errors.append(set_error(0, "AlreadyExists", "The tournament name is already used."))#set_json_error_response(0, "AlreadyExists", "The tournament name is already used.") 
		return data, errors

	tournaments[name] = Tournament(name, len(tournaments)+1, round_num, style)

	data["id"] = tournaments[name].code
	data["name"] = name
	data["num_of_rounds"] = round_num
	data["style"] = style
	return data, errors

def list_all_tournaments():
	data = {}
	errors = []
	data["tournament_num"] = len(tournaments)
	data["tournaments"] = [{"name": t.name, "num_of_rounds": t.round_num, "style": t.style["style_name"]} for t in tournaments.values()]

	return data, errors

def list_all_styles():
	data = []
	for v in styles.values():
		data.append(
			{"style_name": v["style_name"],
			"debater_num_per_team": v["debater_num_per_team"],
			"team_num": v["team_num"],
			"score_weights": v["score_weights"],
			"replies": v["replies"],
			"num_of_replies": v["num_of_replies"]
			})

	return set_json_response(data=data)

def create_style(data):
	styles[data["style_name"]] = {"style_name": data["style_name"], "style_name": data["debater_num_per_team"], "team_num": data["team_num"], "score_weights": data["score_weights"], "replies": data["replies"], "num_of_replies": data["num_of_replies"]}

	pass
