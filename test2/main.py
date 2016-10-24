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

tt.set_seed(100)


if __name__ == '__main__':
	th = Thread(target=run, kwargs={"host":'localhost', "port":8080, "debug":True, "server":'cherrypy'})
	th.setDaemon(True)
	th.start()

	print(tt.create_tournament_exporter('tournaments', STYLE, TOURNAMENT_NAME, NUM_OF_ROUNDS, method='POST'))
	print(tt.add_institution_exporter(TOURNAMENT_NAME+'/institutions/', NUM_INSTITUTIONS, method='POST'))
	print(tt.add_debater_exporter(TOURNAMENT_NAME+'/speakers/', NUM_DEBATERS, method='POST'))
	print(tt.add_team_exporter(TOURNAMENT_NAME+'/teams/', NUM_TEAMS, NUM_INSTITUTIONS, STYLE, method='POST'))
	print(tt.add_adjudicator_exporter(TOURNAMENT_NAME+'/adjudicators/', NUM_ADJUDICATORS, NUM_TEAMS, NUM_INSTITUTIONS, method='POST'))
	print(tt.add_venue_exporter(TOURNAMENT_NAME+'/venues/', NUM_VENUES, method='POST'))
	print(tt.set_judge_criterion_exporter(TOURNAMENT_NAME, NUM_OF_ROUNDS, method='PUT'))

	for i in range(1, NUM_OF_ROUNDS+1):
		print(tt.send_round_config_exporter(TOURNAMENT_NAME+'/'+str(i), method='PUT'))
		stas = tt.get_suggested_team_allocations_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_team_allocations', method='POST')
		print(stas)
		print(tt.confirm_team_allocation_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_team_allocations/0', stas[0]['data'][0]['allocation'], method='POST'))

		stas2 = tt.get_suggested_adjudicator_allocations_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_adjudicator_allocations', method='GET')
		print(stas2)
		print(tt.confirm_team_allocation_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_adjudicator_allocations/0', stas2[0]['data'][0]['allocation'], method='POST'))

		stas3 = tt.get_suggested_venue_allocation_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_venue_allocation', method='GET')
		final_allocation = stas3[0]['data']['allocation']
		print(stas3)
		print(tt.confirm_venue_allocation_exporter(TOURNAMENT_NAME+'/'+str(i)+'/suggested_venue_allocation', final_allocation, method='POST'))

		debater_result = tt.generate_random_speaker_result(final_allocation, STYLE, NUM_TEAMS)
		print(debater_result)
		team_result = tt.generate_team_result(final_allocation, STYLE, debater_result, NUM_TEAMS)
		print(team_result)
		adjudicator_result = tt.generate_adjudicator_result(final_allocation, STYLE)
		print(adjudicator_result)
		break
