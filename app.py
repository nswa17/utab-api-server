# -*- coding: utf-8 -*-
from bottle import get, post, request, response, route, run, abort
import cherrypy
import json
#jsonはここで処理, responseもここで作成

from lib.server.controller import *
import lib.server.src.stools as stools

API_VERSION = 'v0.1'

URL_styles = '/'+API_VERSION+'/styles'
URL_tournaments = '/'+API_VERSION+'/tournaments'
URL_tournament = '/'+API_VERSION+'/<tournament_name>'
URL_backups = '/'+API_VERSION+'/<tournament_name>/backups'
URL_verification = '/'+API_VERSION+'/<tournament_name>/verify'
URL_round = '/'+API_VERSION+'/<tournament_name>/<round_num:int>'
URL_team_allocations = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/suggested_team_allocations'
URL_team_allocation = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/team_allocation'
URL_adjudicator_allocations = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/suggested_adjudicator_allocations'
URL_adjudicator_allocation = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/adjudicator_allocation'
URL_venue_allocation = '/'+API_VERSION+'/<tournament_name>/<round_num:int>/venue_allocation'
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

URL_check_allocation = '/'+API_VERSION+'/<tournament_name>/check'

@route(URL_styles)
@stools.make_json(URL_styles)
def list_all_styles_callback():
	return list_all_styles()

@route(URL_styles, method='PUT')
@stools.make_json(URL_styles)
def add_style_callback(tournament_name):
	req = request.json
	return add_style(req)

@route(URL_tournaments)
@stools.make_json(URL_tournaments)
def list_all_tournaments_callback():
	return list_all_tournaments()

@route(URL_tournament)#when available?
@stools.make_json(URL_tournament)
def fetch_tournament_callback(tournament_name):
	return fetch_tournament(tournament_name)

@route(URL_tournament, method='POST')
@stools.make_json(URL_tournament)
def create_tournament_callback(tournament_name):
	req = request.json
	return create_tournament(req)

@route(URL_tournament, method='DELETE')
@stools.make_json(URL_tournament)
def delete_tournament_callback():
	return ""

@route(URL_tournament, method='PUT')
@stools.make_json(URL_tournament)
def set_judge_criterion_callback(tournament_name):
	req = request.json
	return set_judge_criterion(tournament_name, req)

@route(URL_tournament, method='PATCH')#when available?
@stools.make_json(URL_tournament)
def modify_tournament_callback(tournament_name):
	return ""

@route(URL_verification, method='PUT')
@stools.make_json(URL_tournament)
def verify_callback(tournament_name):
	return ""

@route(URL_round)
@stools.make_json(URL_round)
def fetch_round_callback(tournament_name, round_num):
	return fetch_round(tournament_name, round_num)

@route(URL_round, method='PUT')
@stools.make_json(URL_round)
def send_round_config_callback(tournament_name, round_num):
	return ""

@route(URL_round, method='POST')
@stools.make_json(URL_round)
def proceed_round_callback(tournament_name, round_num):
	return ""

@route(URL_team_allocations)
@stools.make_json(URL_team_allocations)
def get_suggested_team_allocations_callback(tournament_name, round_num):
	return ""

@route(URL_team_allocation)
@stools.make_json(URL_team_allocation)
def get_suggested_team_allocation_callback(tournament_name, round_num, matchup_id):
	return ""

@route(URL_team_allocation, method='PATCH')
@stools.make_json(URL_team_allocation)
def modify_suggested_team_allocation_callback(tournament_name, round_num, matchup_id):
	return ""

@route(URL_team_allocation, method='POST')
@stools.make_json(URL_team_allocation)
def confirm_team_allocation_callback(tournament_name, round_num, matchup_id):
	return ""

@route(URL_adjudicator_allocations)
@stools.make_json(URL_adjudicator_allocations)
def get_suggested_adjudicator_allocations_callback(tournament_name, round_num):
	return ""

@route(URL_adjudicator_allocation, method='PATCH')
@stools.make_json(URL_adjudicator_allocation)
def modify_suggested_adjudicator_allocation_callback(tournament_name, round_num):
	return ""

@route(URL_adjudicator_allocation, method='POST')
@stools.make_json(URL_adjudicator_allocation)
def confirm_adjudicator_allocation_callback(tournament_name, round_num):
	return ""

@route(URL_venue_allocation)
@stools.make_json(URL_venue_allocation)
def get_suggested_venue_allocation_callback(tournament_name, round_num):
	return ""

@route(URL_venue_allocation, method='PATCH')
@stools.make_json(URL_venue_allocation)
def moodify_venue_allocation_callback(tournament_name, round_num):
	return ""

@route(URL_venue_allocation, method='POST')
@stools.make_json(URL_venue_allocation)
def confirm_venue_allocation_callback(tournament_name, round_num):
	return ""

@route(URL_check_allocation)
@stools.make_json(URL_check_allocation)
def check_allocation_callback(tournament_name):
	return ""

@route(URL_adjudicators)
@stools.make_json(URL_adjudicators)
def list_all_adjudicators_callback(tournament_name):
	return ""

@route(URL_adjudicator)
@stools.make_json(URL_adjudicator)
def fetch_adjudicator_callback(tournament_name, adjudicator_id):
	return ""

@route(URL_adjudicator, method='POST')
@stools.make_json(URL_adjudicator)
def add_adjudicator_callback(tournament_name, adjudicator_id):
	req = request.json
	return add_adjudicator(tournament_name, req)

@route(URL_adjudicator, method='DELETE')
@stools.make_json(URL_adjudicator)
def delete_adjudicator_callback(tournament_name, adjudicator_id):
	return ""

@route(URL_adjudicator, method='PATCH')
@stools.make_json(URL_adjudicator)
def modify_adjudicator_callback(tournament_name, adjudicator_id):
	return ""


@route(URL_speakers)
@stools.make_json(URL_speakers)
def list_all_speakers_callback(tournament_name):
	return ""

@route(URL_speaker)
@stools.make_json(URL_speaker)
def fetch_speaker_callback(tournament_name, speaker_id):
	return ""

@route(URL_speaker, method='POST')
@stools.make_json(URL_speaker)
def add_speaker_callback(tournament_name, speaker_id):
	req = request.json
	return add_speaker(tournament_name, req)

@route(URL_speaker, method='DELETE')
@stools.make_json(URL_speaker)
def delete_speaker_callback(tournament_name, speaker_id):
	return ""

@route(URL_speaker, method='PATCH')
@stools.make_json(URL_speaker)
def modify_speaker_callback(tournament_name, speaker_id):
	return ""

@route(URL_teams)
@stools.make_json(URL_teams)
def list_all_teams_callback(tournament_name):
	return ""

@route(URL_team)
@stools.make_json(URL_team)
def fetch_team_callback(tournament_name, team_id):
	return ""

@route(URL_team, method='POST')
@stools.make_json(URL_team)
def add_team_callback(tournament_name, team_id):
	req = request.json
	return add_team(tournament_name, req)

@route(URL_team, method='DELETE')
@stools.make_json(URL_team)
def delete_team_callback(tournament_name, team_id):
	return ""

@route(URL_team, method='PATCH')
@stools.make_json(URL_team)
def modify_team_callback(tournament_name, team_id):
	return ""

@route(URL_venues)
@stools.make_json(URL_venues)
def list_all_venues_callback(tournament_name):
	return ""

@route(URL_venue)
@stools.make_json(URL_venue)
def fetch_venue_callback(tournament_name, venue_id):
	return ""

@route(URL_venue, method='POST')
@stools.make_json(URL_venues)
def add_venue_callback(tournament_name, venue_id):
	req = request.json
	return add_venue(tournament_name, req)

@route(URL_venue, method='DELETE')
@stools.make_json(URL_venues)
def delete_venue_callback(tournament_name, venue_id):
	return ""

@route(URL_venue, method='PATCH')
@stools.make_json(URL_venue)
def modify_venue_callback(tournament_name, venue_id):
	return ""

@route(URL_institutions)
@stools.make_json(URL_institutions)
def list_all_institutions_callback(tournament_name):
	return ""

@route(URL_institution)
@stools.make_json(URL_institution)
def fetch_institution_callback(tournament_name, institution_id):
	return ""

@route(URL_institution, method='POST')
@stools.make_json(URL_institution)
def add_institution_callback(tournament_name, institution_id):
	req = request.json
	return add_institution(tournament_name, req)

@route(URL_institution, method='DELETE')
@stools.make_json(URL_institution)
def delete_institution_callback(tournament_name, institution_id):
	return ""

@route(URL_institution, method='PATCH')
@stools.make_json(URL_institution)
def modify_institution_callback(tournament_name, institution_id):
	return ""

@route(URL_team_results)
@stools.make_json(URL_team_results)
def get_team_results_callback(tournament_name, round_num):
	return ""

@route(URL_speaker_results)
@stools.make_json(URL_speaker_results)
def get_speaker_results_callback(tournament_name, round_num):
	return ""

@route(URL_speaker_results, method='PUT')
@stools.make_json(URL_speaker_results)
def send_speaker_results_callback(tournament_name, round_num):
	return ""

@route(URL_adjudicator_results)
@stools.make_json(URL_adjudicator_results)
def list_adjudicator_results_callback(tournament_name, round_num):
	return ""

@route(URL_adjudicator_results, method='PUT')
@stools.make_json(URL_adjudicator_results)
def send_adjudicator_results_callback(tournament_name, round_num):
	return ""

@route(URL_backups)
@stools.make_json(URL_backups)
def list_backups_callback(tournament_name):
	return ""

@route(URL_backups, method='PUT')
@stools.make_json(URL_backups)
def import_backup_callback(tournament_name):
	return ""

@route(URL_backups, method='POST')
@stools.make_json(URL_backups)
def save_backup_callback(tournament_name):
	return ""

@route(URL_adjudicator_comments)
@stools.make_json(URL_adjudicator_comments)
def download_adjudicator_comments_callback(tournament_name):
	return ""

@route(URL_total_team_results)
@stools.make_json(URL_total_team_results)
def download_total_team_results_callback(tournament_name):
	return ""

@route(URL_total_speaker_results)
@stools.make_json(URL_total_speaker_results)
def download_total_speaker_results_callback(tournament_name):
	return ""

@route(URL_total_adjudicator_results)
@stools.make_json(URL_total_adjudicator_results)
def download_total_adjudicator_results_callback(tournament_name):
	return ""

if __name__ == "__main__":

	run(host='localhost', port=8080, debug=True, server='cherrypy')#must be False when publicated


