# -*- coding: utf-8 -*-
import json

from tournament import *

with open(os.path.dirname(__file__)+'/dat/styles.json') as f:
	styles = json.load(f)

tournaments = {
			  }


#round_num
#tournament_code
#tournament_name
#style

if __name__ == "__main__":

	"""usage

	tournament = Tournament(tournament_code, tournament_name, round_num, style)

	#	 						#
	#	 ARRANGING TOURNAMENT	#
	#	   						#

	for i in range(round_num):

		round = tournament.round()

		while True:

			#	 					#
			#	 ARRANGING ROUND	#
			#	   					#

			round.set(force=False) && break # check data

		round.compute_matchups()
		round.set_matchup(matchup)

		round.compute_allocations()
		round.set_allocation(allocation)

		round.compute_panel_allocation()
		round.set_panel_allocation(panel_allocation)

		round.compute_venue_allocation()
		round.set_venue_allocation(venue_allocation)

		while True:

			#							#
			#	  COLLECTING RESULTS	#
			#							#

			round.process_result(force=False)##########belowと統合?
			round.process_result_of_adj(force=False)##########belowと統合?
			round.end(force=False) && break
		
	tournament.end()

	"""

	"""
	Test code
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
		print("sub", {a.name: a.scores_sub for a in t.adjudicator_list})

