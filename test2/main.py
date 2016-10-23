# -*- coding: utf-8 -*-
import os
import sys
from threading import Thread
import testtools as tt

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, path)
from app import *
import cherrypy

STYLE_NAME = "NA"
STYLE = tt.styles[STYLE_NAME]
NUM_INSTITUTIONS = 4
NUM_TEAMS = 8
NUM_DEBATERS = STYLE["debater_num_per_team"] * NUM_TEAMS
NUM_ADJUDICATORS = 6
NUM_VENUES = 4
NUM_OF_ROUNDS = 4
TOURNAMENT_NAME = "testtournament"

tt.set_seed(100)


if __name__ == '__main__':
	th = Thread(target=run, kwargs={"host":'localhost', "port":8080, "debug":True, "server":'cherrypy'})
	th.setDaemon(True)
	th.start()

	print(tt.create_tournament_exporter(STYLE, TOURNAMENT_NAME, NUM_OF_ROUNDS))
	print(tt.add_institution_exporter(NUM_INSTITUTIONS))
	print(tt.add_debater_exporter(NUM_DEBATERS))
	print(tt.add_team_exporter(NUM_TEAMS, NUM_INSTITUTIONS, STYLE))
	print(tt.add_adjudicator_exporter(NUM_ADJUDICATORS, NUM_TEAMS, NUM_INSTITUTIONS))
	print(tt.add_venue_exporter(NUM_VENUES))
	print(tt.set_judge_criterion(NUM_OF_ROUNDS))

	for i in range(NUM_OF_ROUNDS):
		