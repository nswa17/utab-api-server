# -*- coding: utf-8 -*-
from bottle import get, post, request, response, route, run, abort
import cherrypy
import json
#jsonはここで処理, responseもここで作成

from lib.server.controller import *
import lib.server.src.stools as stools

API_VERSION = 'v1.0'

URL_styles = '/'+API_VERSION+'/styles'
URL_tournaments = '/'+API_VERSION+'/tournaments'
URL_tournament = '/'+API_VERSION+'/<tournament_name>'
URL_backups = '/'+API_VERSION+'/<tournament_name>/backups'
URL_verification = '/'+API_VERSION+'/<tournament_name>/verify'
URL_round = '/'+API_VERSION+'/<tournament_name>/<round_num:int>'
URL_team_allocations = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/suggested_team_allocations'
URL_team_allocation = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/suggested_team_allocations/<allocation_id:int>'
URL_adjudicator_allocations = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/suggested_adjudicator_allocations'
URL_adjudicator_allocation = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/suggested_adjudicator_allocations/<allocation_id:int>'
URL_venue_allocation = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/suggested_venue_allocation'
URL_adjudicators = '/'+API_VERSION+'/<tournament_name>/adjudicators'
URL_adjudicator = '/'+API_VERSION+'/<tournament_name>/adjudicators/<adjudicator_id:int>'
URL_speakers = '/'+API_VERSION+'/<tournament_name>/speakers'
URL_speaker = '/'+API_VERSION+'/<tournament_name>/speakers/<speaker_id:int>'
URL_teams = '/'+API_VERSION+'/<tournament_name>/teams'
URL_team = '/'+API_VERSION+'/<tournament_name>/teams/<team_id:int>'
URL_venues = '/'+API_VERSION+'/<tournament_name>/venues'
URL_venue = '/'+API_VERSION+'/<tournament_name>/venues/<venue_id:int>'
URL_institutions = '/'+API_VERSION+'/<tournament_name>/institutions'
URL_institution = '/'+API_VERSION+'/<tournament_name>/institutions/<institution_id:int>'
URL_team_results = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/results/teams'
URL_speaker_results = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/results/speakers'
URL_adjudicator_results = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/results/adjudicators'

URL_adjudicator_comments = '/'+API_VERSION+'/<tournament_name>/results/adjudicators/comments'
URL_total_team_results = '/'+API_VERSION+'/<tournament_name>/results/teams'
URL_total_adjudicator_results = '/'+API_VERSION+'/<tournament_name>/results/adjudicators'
URL_total_speaker_results = '/'+API_VERSION+'/<tournament_name>/results/speakers'

URL_check_allocation = '/'+API_VERSION+'/<tournament_name>/<round_num>/check'

@stools.route_json(URL_styles)
def list_styles_callback():
	return list_styles()

@stools.route_json(URL_styles, method='PUT')
def add_style_callback():
	req = request.json
	return add_style(req)

@stools.route_json(URL_tournaments)
def list_tournaments_callback():
	return list_tournaments()

@stools.route_json(URL_tournament, method='GET')
def fetch_tournament_callback(tournament_name):
	return fetch_tournament(tournament_name)

@stools.route_json(URL_tournament, method='POST')
def create_tournament_callback(tournament_name):
	req = request.json
	return create_tournament(req)

@stools.route_json(URL_tournament, method='DELETE')
def delete_tournament_callback():
	return ""

@stools.route_json(URL_tournament, method='PUT')
def set_judge_criterion_callback(tournament_name):
	req = request.json
	return set_judge_criterion(tournament_name, req)

@stools.route_json(URL_tournament, method='PATCH')#when available?
def modify_tournament_callback(tournament_name):
	return ""

@stools.route_json(URL_verification, method='PUT')
def verify_callback(tournament_name):
	return ""

@stools.route_json(URL_round)
def fetch_round_callback(tournament_name, round_num):
	return fetch_round(tournament_name, round_num)

@stools.route_json(URL_round, method='PUT')
def send_round_config_callback(tournament_name, round_num):
	req = request.json
	return send_round_config(tournament_name, round_num, req)

@stools.route_json(URL_round, method='POST')
def finish_round_callback(tournament_name, round_num):
	req = request.json
	return finish_round(tournament_name, round_num, req)

@stools.route_json(URL_team_allocations, method='POST')
def get_suggested_team_allocations_callback(tournament_name, round_num):
	req = request.json
	return get_suggested_team_allocations(tournament_name, round_num, req)

@stools.route_json(URL_team_allocations, method='PUT')
def check_team_allocation_callback(tournament_name, round_num):
	req = request.json
	return check_team_allocation(tournament_name, round_num, req)

@stools.route_json(URL_team_allocation)
def get_suggested_team_allocation_callback(tournament_name, round_num, allocation_id):
	return ""

@stools.route_json(URL_team_allocation, method='POST')
def confirm_team_allocation_callback(tournament_name, round_num, allocation_id):
	req = request.json
	return confirm_team_allocation(tournament_name, round_num, allocation_id, req)

@stools.route_json(URL_adjudicator_allocations, method='PUT')
def check_adjudicator_allocation_callback(tournament_name, round_num):
	req = request.json
	return check_adjudicator_allocation(tournament_name, round_num, req)

@stools.route_json(URL_adjudicator_allocations, method='POST')
def get_suggested_adjudicator_allocations_callback(tournament_name, round_num):
	return get_suggested_adjudicator_allocations(tournament_name, round_num)

@stools.route_json(URL_adjudicator_allocation, method='POST')
def confirm_adjudicator_allocation_callback(tournament_name, round_num, allocation_id):
	req = request.json
	return confirm_adjudicator_allocation(tournament_name, round_num, allocation_id, req)

@stools.route_json(URL_venue_allocation, method='POST')
def get_suggested_venue_allocation_callback(tournament_name, round_num):
	return get_suggested_venue_allocation(tournament_name, round_num)

@stools.route_json(URL_venue_allocation, method='PUT')
def check_venue_allocation_callback(tournament_name, round_num):
	return ""

@stools.route_json(URL_venue_allocation, method='POST')
def confirm_venue_allocation_callback(tournament_name, round_num):
	req = request.json
	return confirm_venue_allocation(tournament_name, round_num, req)

@stools.route_json(URL_check_allocation)
def check_allocation_callback(tournament_name):
	return ""

@stools.route_json(URL_adjudicators)
def list_adjudicators_callback(tournament_name):
	return list_adjudicators(tournament_name)

@stools.route_json(URL_adjudicator)
def fetch_adjudicator_callback(tournament_name, adjudicator_id):
	return fetch_adjudicator(tournament_name, adjudicator_id)

@stools.route_json(URL_adjudicator, method='POST')
def add_adjudicator_callback(tournament_name, adjudicator_id):
	req = request.json
	return add_adjudicator(tournament_name, req)

@stools.route_json(URL_adjudicator, method='DELETE')
def delete_adjudicator_callback(tournament_name, adjudicator_id):
	return ""

@stools.route_json(URL_adjudicator, method='PATCH')
def modify_adjudicator_callback(tournament_name, adjudicator_id):
	return ""

@stools.route_json(URL_speakers)
def list_speakers_callback(tournament_name):
	return list_speakers(tournament_name)

@stools.route_json(URL_speaker)
def fetch_speaker_callback(tournament_name, speaker_id):
	return fetch_speaker(tournament_name, speaker_id)

@stools.route_json(URL_speaker, method='POST')
def add_speaker_callback(tournament_name, speaker_id):
	req = request.json
	return add_speaker(tournament_name, req)

@stools.route_json(URL_speaker, method='DELETE')
def delete_speaker_callback(tournament_name, speaker_id):
	return ""

@stools.route_json(URL_speaker, method='PATCH')
def modify_speaker_callback(tournament_name, speaker_id):
	return ""

@stools.route_json(URL_teams)
def list_teams_callback(tournament_name):
	return list_teams(tournament_name)

@stools.route_json(URL_team)
def fetch_team_callback(tournament_name, team_id):
	return fetch_team(tournament_name, team_id)

@stools.route_json(URL_team, method='POST')
def add_team_callback(tournament_name, team_id):
	req = request.json
	return add_team(tournament_name, req)

@stools.route_json(URL_team, method='DELETE')
def delete_team_callback(tournament_name, team_id):
	return ""

@stools.route_json(URL_team, method='PATCH')
def modify_team_callback(tournament_name, team_id):
	return ""

@stools.route_json(URL_venues)
def list_venues_callback(tournament_name):
	return list_venues(tournament_name)

@stools.route_json(URL_venue)
def fetch_venue_callback(tournament_name, venue_id):
	return fetch_venue(tournament_name, venue_id)

@stools.route_json(URL_venue, method='POST')
def add_venue_callback(tournament_name, venue_id):
	req = request.json
	return add_venue(tournament_name, req)

@stools.route_json(URL_venue, method='DELETE')
def delete_venue_callback(tournament_name, venue_id):
	return ""

@stools.route_json(URL_venue, method='PATCH')
def modify_venue_callback(tournament_name, venue_id):
	return ""

@stools.route_json(URL_institutions)
def list_institutions_callback(tournament_name):
	return list_institutions(tournament_name)

@stools.route_json(URL_institution)
def fetch_institution_callback(tournament_name, institution_id):
	return fetch_institution(tournament_name, institution_id)

@stools.route_json(URL_institution, method='POST')
def add_institution_callback(tournament_name, institution_id):
	req = request.json
	return add_institution(tournament_name, req)

@stools.route_json(URL_institution, method='DELETE')
def delete_institution_callback(tournament_name, institution_id):
	return ""

@stools.route_json(URL_institution, method='PATCH')
def modify_institution_callback(tournament_name, institution_id):
	return ""

@stools.route_json(URL_team_results)
def get_team_results_callback(tournament_name, round_num):
	return ""

@stools.route_json(URL_speaker_results)
def get_speaker_results_callback(tournament_name, round_num):
	return ""

@stools.route_json(URL_speaker_results, method='PUT')
def send_speaker_result_callback(tournament_name, round_num):
	req = request.json
	return send_speaker_result(tournament_name, round_num, req)

@stools.route_json(URL_adjudicator_results)
def list_adjudicator_results_callback(tournament_name, round_num):
	return ""

@stools.route_json(URL_adjudicator_results, method='PUT')
def send_adjudicator_result_callback(tournament_name, round_num):
	req = request.json
	return send_adjudicator_result(tournament_name, round_num, req)

@stools.route_json(URL_backups)
def list_backups_callback(tournament_name):
	return list_backups(tournament_name)

@stools.route_json(URL_backups, method='PUT')
def import_backup_callback(tournament_name):
	req = request.json
	return import_backup(tournament_name, req)

@stools.route_json(URL_backups, method='POST')
def save_backup_callback(tournament_name):
	data = request.json
	return save_backup(tournament_name, data)

@stools.route_json(URL_adjudicator_comments)
def download_adjudicator_comments_callback(tournament_name):
	return ""

@stools.route_json(URL_total_team_results)
def download_total_team_results_callback(tournament_name):
	return download_total_team_results(tournament_name)

@stools.route_json(URL_total_speaker_results)
def download_total_speaker_results_callback(tournament_name):
	return download_total_speaker_results(tournament_name)

@stools.route_json(URL_total_adjudicator_results)
def download_total_adjudicator_results_callback(tournament_name):
	return download_total_adjudicator_results(tournament_name)

if __name__ == "__main__":

	initialize_backups()
	run(host='localhost', port=8080, debug=True, server='cherrypy')#must be False when publicated


