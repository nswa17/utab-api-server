#controllers
from bottle import HTTPResponse

import json
from model import *

def list_all_teams(team_list):
	all_teams = {}
	for team in team_list:
		all_teams[team.name] = {"id":team.code, "name":team_name, "url":team.url}

	return set_json_response(all_teams)

def set_json_response(data={}, status=200, errors=None):
	data_rev = {"errors":errors, "data":data}
	body = json.dumps(data_rev)
	r = HTTPResponse(status = status, body = body)
	r.set_header('Content-Type', 'application/json')
	return r

def list_all_tournaments():
	return set_json_response(data=list(tournaments.keys()))

def set_json_error_response(status_code, status_text, message):
	error = {}
	error["statusCode"] = status_code
	error["statusText"] = status_text
	error["message"] = message
	return set_json_response(errors=error)

def create_tournament(data):
	try:
		tournament_name = data["tournament_name"]
		style = data["style"]
		round_num = data["round_num"]
	except KeyError:
		return set_json_error_response(0, "KeyError", "Data sent has no key named tournament_name/style/round_num.")

	if data["tournament_name"] in tournaments.keys():
		return set_json_error_response(0, "AlreadyExists", "The tournament name is already used.")

	tournaments[tournament_name] = Tournament(tournament_name, len(tournaments)+1, round_num, style)

	return set_json_response(data={
			"id": tournaments[tournament_name].code,
			"name": tournament_name,
			"num_of_rounds": round_num,
			"style": style
			}
		)

def list_all_tournaments():
	data = {}
	data["tournament_num"] = len(tournaments)
	data["tournaments"] = [{"name": t.name, "num_of_rounds": t.round_num, "style": t.style["style_name"]} for t in tournaments.values()]

	return set_json_response(data=data)

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
	styles[data["style_name"]] = {"style_name": data["style_name"], "style_name" = data["debater_num_per_team"], "team_num":data["team_num"], "score_weights":data["score_weights"], "replies":data["replies"], "num_of_replies":data["num_of_replies"]}

	pass
