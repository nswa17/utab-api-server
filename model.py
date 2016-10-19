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
#    : blocking for api server#single thread is much better?
#    : set status
#    : algorithm selection
#    : teamnum and team_num_per_round

#################### ROLE OF EACH MODULE ####################
# main: model
# internal: functions for iternal process of grids/lattices
# result: functions to process results
# classes: classes to operate a tournament
# entity_classes: classes of Team/Adj/Venue/Debater/Institution
# grid_classes: internal classes for algorithm
# error_classes: classes related to matchup warnings
# property: extract information from grids/lattices
# filter: functions to add adoptness for grids/lattices
# select: functions to choose best grids/lattices
# bit: wrappers for bit calculation on adoptness
# tools: tools
#
# mstat: functions to analyze results
# plot: functions to plot analyzed data
#
# model____classes
#       |	 |
#       |	 |_internal
#       |    |    |
#       |    |    |_property
#       |    |    |
#       |    |    |_grid_classes
#       |    |    |    |_bit
#       |    |    |
#       |    |    |_entity_classes
#       |    |    |    |_tools
#       |    |    |
#       |    |    |_select
#       |    |    |    |_property
#       |    |    |    |_grid_classes
#       |    |    |    	    |_property
#       |    |    |
#       |    |    |_filter
#       |    |         |_bit
#       |    |         |_property
#       |	 |_bit
#       |    |
#       |	 |_result
#       |    |    |_tools
#       |    |
#       |	 |_entity_classes
#       |         |_tools
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

if __name__ == "__main__":
	pass
	"""
	tournament = Tournament(tournament_code, tournament_name, round_num, style)

	for i in range(round_num):

		while True:

			#	 						#
			#	 ARRANGING TOURNAMENT	#
			#	   						#

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

			tournament.round[i].process_result_of_adj(force=False)##########belowと統合?
			tournament.round[i].process_result(force=False)##########belowと統合?
			tournament.round[i].end(force=False) && break
		
	tournament.end()
	"""

	"""
	Example code
	"""

	t = Tournament(1, "test", 2, styles["NA"])
	
	t.set_judge_criterion(
		[
            {
                "judge_test_percent":100,
                "judge_repu_percent":0,
                "judge_perf_percent":0
            },
            {
                "judge_test_percent":100,
                "judge_repu_percent":0,
                "judge_perf_percent":0
            }
        ]
    )

	t.add_institution(1, "insti1")
	t.add_institution(2, "insti2")
	t.add_debater(1, "deb1")
	t.add_debater(2, "deb2")
	t.add_debater(3, "deb3")
	t.add_debater(4, "deb4")
	#t.add_debater(5, "deb5")
	#t.add_debater(6, "deb6")
	#t.add_debater(7, "deb7")
	#t.add_debater(8, "deb8")
	t.add_team(1, "team1", [t.debater_list[0], t.debater_list[1]], [t.institution_list[0]])
	t.add_team(2, "team2", [t.debater_list[2], t.debater_list[3]], [t.institution_list[1]])
	#t.add_team(3, "team3", [t.debater_list[4], t.debater_list[5]], [t.institution_list[0]])
	#t.add_team(4, "team4", [t.debater_list[6], t.debater_list[7]], [t.institution_list[1]])
	t.add_adjudicator(1, "adj1", 10, 10, [t.institution_list[0]], [])
	t.add_adjudicator(3, "adj3", 10, 10, [t.institution_list[0]], [])
	#t.add_adjudicator(2, "adj2", 8, 10, [t.institution_list[1]], [])
	t.add_venue(1, "venue1")
	#t.add_venue(2, "venue2")
	#t.add_venue(2, "venue2")

	for i in range(2):

		r = t.round()
		r.set_constants()
		r.set_constants_of_adj()
		r.set()

		r.compute_matchups()
		r.set_matchup(r.candidate_matchups[0])
		r.compute_allocations()

		r.set_allocation(r.candidate_allocations[0])

		r.compute_panel_allocation()
		r.compute_venue_allocation()

		r.set_result(
			{
				"debater_id": 1,
				"result":
				{
					"round": 1,
					"team_id": 1,
					"scores": [70, 0, 35],
					"win_point": 0,
					"opponent_ids": [2],
					"position": "gov"
				}
			}
		)

		r.set_result(
			{
				"debater_id": 1,
				"result":
				{
					"round": 1,
					"team_id": 1,
					"scores": [71, 0, 35.5],
					"win_point": 0,
					"opponent_ids": [2],
					"position": "gov"
				}
			}
		)

		r.set_result(
			{
				"debater_id": 2,
				"result":
				{
					"round": 1,
					"team_id": 1,
					"scores": [0, 72, 0],
					"win_point": 0,
					"opponent_ids": [2],
					"position": "gov"
				}
			}
		)

		r.set_result(
			{
				"debater_id": 3,
				"result":
				{
					"round": 1,
					"team_id": 2,
					"scores": [76, 0, 37],
					"win_point": 1,
					"opponent_ids": [1],
					"position": "gov"
				}
			}
		)


		r.set_result(
			{
				"debater_id": 4,
				"result":
				{
					"round": 1,
					"team_id": 2,
					"scores": [0, 75, 0],
					"win_point": 1,
					"opponent_ids": [1],
					"position": "gov"
				}
			}
		)

		r.set_result_of_adj(# from team1
			{
				"adj_id": 1,
				"result":
				{
					"round": 1,
					"from": "team",
					"from_id": 1,
					"from_name": "team1",
					"chair": True,
					"point": 8,
					"team_ids": [1, 2],
					"comment": "good",
				}
			}
		)

		r.set_result_of_adj(#from team2
			{
				"adj_id": 1,
				"result":
				{
					"round": 1,
					"from": "team",
					"from_id": 2,
					"from_name": "team2",
					"chair": True,
					"point": 9,
					"team_ids": [1, 2],
					"comment": "good judge",
				}
			}
		)

		r.process_result()
		r.process_result_of_adj()
		r.end()
		print({t.name:(t.score, t.margin, t.wins) for t in t.team_list})
		print({d.name: d.scores for d in t.debater_list})
		print({a.name: a.scores for a in t.adjudicator_list})

