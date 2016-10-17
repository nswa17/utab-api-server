import shutil
import csv
import sys
import os
import copy
import itertools
import re

def check_results(round, style):
	regexp = re.compile(r'^[0-9A-Za-z. ¥-]+$')

	results_lists = []

	positions = len(style["score_weight"])
	team_num = style["team_num"]
	debater_num_per_team = style["debater_num_per_team"]

	for row in reader:
		for ele in row:
			hit = regexp.search(ele)
			if hit is None:
				interaction_modules.warn(("warning: results file is using unknown character(fullwidth forms or other symbols)", ele))
		results_lists.append([row[0], row[1]]+[float(row[2+i]) for i in range(positions)]+[int(row[2+positions])]+[row[3+positions+j] for j in range(team_num-1)]+[row[2+positions+team_num]])

	if team_num == 4:
		for i in range(int(len(results_lists)/debater_num_per_team)):
			team_names = [results_lists[debater_num_per_team*i+j][0] for j in range(debater_num_per_team)]
			teams_name_pairs = list(itertools.combinations(team_names, 2))
			for teams_name_pair in teams_name_pairs:
				if teams_name_pair[0] != teams_name_pair[1]:
					interaction_modules.warn(("error in team name column, row:"+str(debater_num_per_team*i+3)))
					return True

		multi2 = {results_list[1]:0 for results_list in results_lists}

		for results_list in results_lists:
			multi2[results_list[1]] += 1


		wins = [0 for i in range(team_num)]
		try:
			for i, results_list in enumerate(results_lists):
				wins[results_list[2+positions]] += 1
		except:
			interaction_modules.warn(("error in win column, unexpected value, row:")+str(i+3))
			interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
			return True

		wins_pairs = list(itertools.combinations(wins, 2))
		for wins_pair in wins_pairs:
			if wins_pair[0] != wins_pair[1]:
				interaction_modules.warn("error in win column")
				return True

		if team_num == 4:
			sides = {"og":0, "oo":0, "cg":0, "co":0}
		else:
			sides = {"gov":0, "opp":0}

		try:
			for i, results_list in enumerate(results_lists):
				sides[results_list[2+positions+team_num]] += 1
		except:
			interaction_modules.warn(("error in side column, unexpected value, row:")+str(i+3))
			interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
			return True

		sides_pairs = list(itertools.combinations(list(sides.values()), 2))
		for sides_pair in sides_pairs:
			if sides_pair[0] != sides_pair[1]:
				interaction_modules.warn("error in side column")
				return True

		if team_num == 4:
			opponents1, opponents2, opponents3, opponents4 = [], [], [], []
			for results_list in results_lists:
				opponents1.extend([results_list[3+positions], results_list[4+positions], results_list[5+positions]])
				opponents2.extend([results_list[0], results_list[4+positions], results_list[5+positions]])
				opponents3.extend([results_list[0], results_list[3+positions], results_list[5+positions]])
				opponents4.extend([results_list[0], results_list[3+positions], results_list[4+positions]])
			if set(opponents1) != set(opponents2) or set(opponents1) != set(opponents3) or set(opponents1) != set(opponents4) or set(opponents2) != set(opponents3) or set(opponents2) != set(opponents4) or set(opponents3) != set(opponents4):
				interaction_modules.warn("error in team and the opponent column")
				return Trueaa
		else:
			opponents = {results_list[0]:results_list[3+positions] for results_list in results_lists}
			opponents2 = {results_list[3+positions]:results_list[0] for results_list in results_lists}

			if opponents != opponents2:
				interaction_modules.warn("error in team and the opponent column")
				return True

		return False