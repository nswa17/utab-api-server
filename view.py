from bottle import get, post, request, response, route, run, abort
import sys
import urllib# for query parse
#引数気持ち悪い

from controller import *

API_VERSION = 'v0.1'

@route('/'+API_VERSION+'/styles')
def list_all_styles_callback():
	return list_all_styles()

@route('/'+API_VERSION+'/styles', method='PUT')
def create_style_callback(tournament_name):
	data = request.json
	return create_style(data)

@route('/'+API_VERSION+'/tournaments')
def list_all_tournaments_callback():
	return list_all_tournaments()

@route('/'+API_VERSION+'/tournaments', method='POST')
def create_tournament_callback():
	data = request.json
	return create_tournament(data)

@route('/'+API_VERSION+'/tournaments', method='DELETE')
def delete_tournament_callback():
	return ""

@route('/'+API_VERSION+'/<tournament_name>')
def fetch_tournament_data_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>', method='PATCH')
def revise_tournament_data_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/verify', method='PUT')
def verify_callback():
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>')
def fetch_round_data_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>', method='PUT')
def send_round_config_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>', method='POST')
def proceed_round_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/matchups')
def get_candidate_matchups_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/matchups/<matchup_id>')
def get_candidate_matchup_callback(tournament_name, round_num, matchup_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/matchups/<matchup_id>', method='PATCH')
def exchange_teams_callback(tournament_name, round_num, matchup_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/matchups/<matchup_id>', method='POST')
def confirm_candidate_matchup_callback(tournament_name, round_num, matchup_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/allocations')
def get_candidate_allocations_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/allocations/<allocation_id>')
def get_candidate_allocation_callback(tournament_name, round_num, allocation_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/matchups/<allocation_id>', method='PATCH')
def exchange_adjudicators_callback(tournament_name, round_num, allocation_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/matchups/<allocation_id>', method='POST')
def confirm_candidate_allocation_callback(tournament_name, round_num, allocation_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/panels')
def get_candidate_panel_allocation_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/panels', method='PATCH')
def exchange_panels_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/panels', method='POST')
def approve_candidate_panel_allocation_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/venues')
def get_candidate_venue_allocation_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/venues', method='PATCH')
def exchange_venues_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/control/venues', method='POST')
def approve_candidate_venue_allocation_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/adjudicators')
def list_all_adjudicators_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/adjudicators', method='POST')
def add_adjudicator_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/adjudicators', method='DELETE')
def delete_adjudicator_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/adjudicators/<adjudicator_id>')
def fetch_adjudicator_data_callback(tournament_name, adjudicator_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/adjudicators/<adjudicator_id>', method='PATCH')
def modify_adjudicator_callback(tournament_name, adjudicator_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/teams')
def list_all_teams_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/teams', method='POST')
def add_team_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/teams', method='DELETE')
def delete_team_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/teams/<team_id>')
def fetch_team_data_callback(tournament_name, team_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/teams/<team_id>', method='PATCH')
def modify_team_callback(tournament_name, team_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/venues')
def list_all_venues_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/venues', method='POST')
def add_venue_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/venues', method='DELETE')
def delete_venue_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/venues/<venue_id>')
def fetch_venue_data_callback(tournament_name, venue_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/venues/<venue_id>', method='PATCH')
def modify_venue_callback(tournament_name, venue_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/institutions')
def list_all_institutions_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/institutions', method='POST')
def add_institution_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/institutions', method='DELETE')
def delete_institution_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/institutions/<institution_id>')
def fetch_institution_data_callback(tournament_name, institution_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/institutions/<institution_id>', method='PATCH')
def modify_institution_callback(tournament_name, institution_id):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/results/teams')
def list_team_results_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/results/speakers')
def list_speaker_results_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/results/speakers', method='PUT')
def send_speaker_results_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/results/adjudicators')
def list_adjudicator_results_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/<round_num>/results/adjudicators', method='PUT')
def send_adjudicator_results_callback(tournament_name, round_num):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/backups')
def list_backups_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/backups', method='PUT')
def import_backup_callback(tournament_name):
	return ""

@route('/'+API_VERSION+'/<tournament_name>/backups', method='POST')
def save_backup_callback(tournament_name):
	return ""


if __name__ == "__main__":

	run(host='localhost', port=8080, debug=True)#must be False when publicated


