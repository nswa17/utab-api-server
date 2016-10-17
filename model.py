from system.modules.classes import *
#from system.modules import interaction_modules
"""KOYAMAs
from system.modules.mstat_modules import *
import system.modules.plot_modules as plt
import numpy as np
"""

#TODO: modified gale shapley
#    : don't consider breaknum when breaknum = 0
#	 : complete model, define controller/view, define exceptions, set logger
#    : round herasu ni taiou

#################### ROLE OF EACH MODULE ####################
# main: model
# internal: functions for iternal process of grids/lattices
# io: export and import data
# classes: classes to operate a tournament
# entity_classes: classes of Team/Adj/Venue/Debater/Institution
# error_classes: classes related to matchup warnings
# property: extract information from grids/lattices
# filter: functions to add adoptness for grids/lattices
# select: functions to choose best grids/lattices
# bit: wrappers for bit calculation on adoptness
#
# mstat: functions to analyze results
# plot: functions to plot analyzed data
#
# main____internal
#       |      |
#       |      |_property
#       |      |
#       |      |_error_classes
#       |      |
#       |      |_entity_classes
#       |      |
#       |      |_select
#       |      |    |_property
#       |      |    |_interaction
#       |      |
#       |      |_filter
#       |      |    |_bit
#       |      |    |_property
#       |      |
#       |      |_io
#       |           |_classes
#       |           |_bit
#       |           |_property
#       |           |_interaction
#       |
#       |_classes
#       |	 |_internal
#       |	 |_io
#       |	 |_entity_classes
#       |
#	   ===
#       | 
#       |__ mstat
#       |      |_property
#       | 
#       |__ plot
#              |_mstat
#
#



if __name__ == "__main__":

	tournaments = {
						#"a1":Tournament("a1", 1, 4, 'BP'),
						#"a2":Tournament("a2", 2, 4, 'BP')
				  }

	styles = {# => {style name, debater num per team, team num, [score weight], reply indexes}
	"ACADEMIC":{"style_name": "ACADEMIC", "debater_num_per_team":4, "team_num":2, "score_weights":[1, 1, 1, 1], "replies":[], "num_of_replies":0},
	"NA":{"style_name": "NA", "debater_num_per_team":2, "team_num":2, "score_weights":[1, 1, 0.5], "replies":[1], "num_of_replies":0},
	"NAFA":{"style_name": "NAFA", "debater_num_per_team":2, "team_num":2, "score_weights":[1, 1, 1, 1], "replies":[], "num_of_replies":0},
	"PDA":{"style_name": "PDA", "debater_num_per_team":3, "team_num":2, "score_weights":[1, 1, 1], "replies":[], "num_of_replies":0},
	"ASIAN":{"style_name": "ASIAN", "debater_num_per_team":3, "team_num":2, "score_weights":[1, 1, 1, 0.5], "replies":[0, 1], "num_of_replies":1},
	"BP":{"style_name": "BP", "debater_num_per_team":2, "team_num":4, "score_weights":[1, 1], "replies":[], "num_of_replies":0},
	"SMALLBP":{"style_name": "SMALLBP", "debater_num_per_team":1, "team_num":4, "score_weights":[1], "replies":[], "num_of_replies":0},
	"PF":{"style_name": "PF", "debater_num_per_team":2, "team_num":2, "score_weights":[1, 1, 1, 1], "replies":[0, 1], "num_of_replies":2},
	"SMALL":{"style_name": "SMALL", "debater_num_per_team":1, "team_num":2, "score_weights":[1, 0.5], "replies":[0], "num_of_replies":1}
	}
	#round_num
	#tournament_code
	#tournament_name
	#style

	tournament = Tournament(tournament_code, tournament_name, round_num, style)

	for i in range(round_num):

		while True:

			#	 						#
			#	 ARRANGING TOURNAMENT	#
			#							#

			tournament.round[i].set(force=False) && break # check data

		tournament.round[i].compute_matchups()
		tournament.round[i].set_matchup(matchup)

		tournament.round[i].compute_allocations()
		tournament.round[i].set_allocation(allocation)

		tournament.round[i].compute_panel_allocation()
		tournament.round[i].set_panel_allocation(panel_allocation)

		tournament.round[i].compute_venue_allocation()
		tournament.round[i].set_venue_allocation(venue_allocation)

		while True:

			#							#
			#	  COLLECTING RESULTS	#
			#							#

			tournament.round[i].end(force=False) && break
		
	tournament.end()
