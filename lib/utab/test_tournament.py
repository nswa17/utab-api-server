# -*- coding: utf-8 -*-
import json
import os

from tournament import *



#round_num
#tournament_code
#tournament_name
#style

if __name__ == "__main__":


	"""
	Test code
	"""

	t = Tournament(1, "test", 2, styles["NA"])
	
	t.add_judge_criterion(
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

	t.add_institution(code=1, name="insti1", scale="a", url="")
	t.add_institution(code=2, name="insti2", scale="a", url="")
	t.add_debater(code=1, name="deb1", url="")
	t.add_debater(code=2, name="deb2", url="")
	t.add_debater(code=3, name="deb3", url="")
	t.add_debater(code=4, name="deb4", url="")
	#t.add_debater(5, "deb5")
	#t.add_debater(6, "deb6")
	#t.add_debater(7, "deb7")
	#t.add_debater(8, "deb8")
	t.add_team(code=1, name="team1", debater_codes=[1, 2], institution_codes=[1], url="", available=True)
	t.add_team(code=2, name="team2", debater_codes=[3, 4], institution_codes=[2], url="", available=True)
	#t.add_team(3, "team3", [t.debater_list[4], t.debater_list[5]], [t.institution_list[0]])
	#t.add_team(4, "team4", [t.debater_list[6], t.debater_list[7]], [t.institution_list[1]])
	t.add_adjudicator(code=1, name="a1", reputation=0, judge_test=5, institution_codes=[1], conflict_team_codes=[], url="", available=True)
	t.add_adjudicator(code=2, name="a2", reputation=0, judge_test=8, institution_codes=[2], conflict_team_codes=[], url="", available=True)
	#t.add_adjudicator(2, "adj2", 8, 10, [t.institution_list[1]], [])
	t.add_venue(code=1, name="venue1", url="", available=True, priority=1)
	#t.add_venue(2, "venue2")
	#t.add_venue(2, "venue2")

	for i in range(2):

		t.rounds[i].set_constants()
		t.rounds[i].set_constants_of_adj()
		r = t.start_round()
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

