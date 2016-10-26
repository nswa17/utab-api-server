# -*- coding: utf-8 -*-
import os
import sys
from threading import Thread
import testtools as tt

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, path)
from app import *
import cherrypy
import json

STYLE_NAME = "NA"
STYLE = tt.styles[STYLE_NAME]
NUM_INSTITUTIONS = 4
NUM_TEAMS = 4
NUM_DEBATERS = STYLE["debater_num_per_team"] * NUM_TEAMS
NUM_ADJUDICATORS = NUM_TEAMS // STYLE["team_num"] + 4
NUM_VENUES = NUM_TEAMS // STYLE["team_num"]
NUM_OF_ROUNDS = 4
TOURNAMENT_NAME = "testtournament"
SEED = 100


if __name__ == '__main__':

	th = Thread(target=run, kwargs={"host":'localhost', "port":8080, "debug":True, "server":'cherrypy'})
	th.setDaemon(True)
	th.start()
	tt.set_seed(SEED)

	print(tt.create_tournament_exporter('tournaments', STYLE, TOURNAMENT_NAME, NUM_OF_ROUNDS, method='POST'))
	print(tt.save_backup_exporter('testtournament/backups', method='POST'))
	print(tt.simple_get_exporter('testtournament/backups', method='GET'))
	print(tt.add_institution_exporter(TOURNAMENT_NAME+'/institutions/', NUM_INSTITUTIONS, method='POST'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/institutions', method='GET'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/institutions/0', method='GET'))
	print(tt.add_debater_exporter(TOURNAMENT_NAME+'/speakers/', NUM_DEBATERS, method='POST'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/speakers', method='GET'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/speakers/0', method='GET'))
	print(tt.add_team_exporter(TOURNAMENT_NAME+'/teams/', NUM_TEAMS, NUM_INSTITUTIONS, STYLE, method='POST'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/teams/0', method='GET'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/teams', method='GET'))
	print(tt.add_adjudicator_exporter(TOURNAMENT_NAME+'/adjudicators/', NUM_ADJUDICATORS, NUM_TEAMS, NUM_INSTITUTIONS, method='POST'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/adjudicators', method='GET'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/adjudicators/0', method='GET'))
	print(tt.add_venue_exporter(TOURNAMENT_NAME+'/venues/', NUM_VENUES, method='POST'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/venues', method='GET'))
	print(tt.simple_get_exporter(TOURNAMENT_NAME+'/venues/0', method='GET'))
	print(tt.set_judge_criterion_exporter(TOURNAMENT_NAME, NUM_OF_ROUNDS, method='PUT'))

	for i in range(1, NUM_OF_ROUNDS+1):
		print(tt.send_round_config_exporter(TOURNAMENT_NAME+'/'+str(i), method='PUT'))
		stas = tt.get_suggested_team_allocations_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_team_allocations', method='POST')
		print(stas)
		print(tt.confirm_team_allocation_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_team_allocations/0', stas[0]['data'][0]['allocation'], method='POST'))

		stas2 = tt.simple_get_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_adjudicator_allocations', method='GET')
		print(stas2)
		print(tt.confirm_team_allocation_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_adjudicator_allocations/0', stas2[0]['data'][0]['allocation'], method='POST'))

		stas3 = tt.simple_get_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_venue_allocation', method='GET')
		final_allocation = stas3[0]['data']['allocation']
		print(stas3)
		print(tt.confirm_venue_allocation_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_venue_allocation', final_allocation, method='POST'))

		"""
		debater_result = tt.generate_random_speaker_result(final_allocation, STYLE, NUM_TEAMS)
		print(debater_result)
		team_result = tt.generate_team_result(final_allocation, STYLE, debater_result, NUM_TEAMS)
		print(team_result)
		adjudicator_result = tt.generate_adjudicator_result(final_allocation, STYLE)
		print(adjudicator_result)
		break
		"""

		stas4 = tt.send_speaker_result_exporter(TOURNAMENT_NAME+'/'+str(i)+'/results/speakers', final_allocation, STYLE, NUM_DEBATERS, NUM_TEAMS, method='PUT')
		print(stas4)
		stas5 = tt.send_adjudicator_result_exporter(TOURNAMENT_NAME+'/'+str(i)+'/results/adjudicators', final_allocation, STYLE, NUM_ADJUDICATORS, method='PUT')
		print(stas5)
		print(tt.finish_round_exporter(TOURNAMENT_NAME+'/'+str(i), i, method='POST'))

		print(tt.simple_get_exporter(TOURNAMENT_NAME+'/results/speakers', method='GET'))
		print(tt.simple_get_exporter(TOURNAMENT_NAME+'/results/teams', method='GET'))
		print(tt.simple_get_exporter(TOURNAMENT_NAME+'/results/adjudicators', method='GET'))

