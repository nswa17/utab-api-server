# -*- coding: utf-8 -*-
from .classes import *
from .bit_modules import *
from .property_modules import *
from . import interaction_modules
from datetime import datetime
import random
import shutil
import csv
import sys
import os
import math
import copy
import re
import itertools
try:
	import readline
except:
	pass

def round_str2float(ele, m):
	if ele == 'n/a':
		return 'n/a'
	else:
		return round(ele, m)
	
def export_blank_results(allocations, round_num, style_cfg, filename):
	if os.path.exists(filename):
		if not interaction_modules.overwrite("the file", filename, "already exists"):return

	with open(filename, "w") as g:
		writer = csv.writer(g)
		if style_cfg["team_num"] == 4:
			win_text = "Win-points[0, 1, 2, 3]"
			position_text = "Position[og, oo, cg, co]"
			sides = ["og", "oo", "cg", "co"]
		else:
			win_text = "Win[0:lose, 1:win]"
			position_text = "Side[gov, opp]"
			sides = ["gov", "opp"]
		writer.writerow(["team_name", "name"]+["R"+str(round_num)+"-"+str(i+1) for i in range(len(style_cfg["score_weight"]))]+[win_text]+["Opponent"+str(i+1) for i in range(style_cfg["team_num"]-1)]+[position_text])

		for lattice in allocations:
			for k, team in enumerate(lattice.grid.teams):
				for member in team.debaters:
					writer.writerow([team.name, member.name]+[0 for i in range(len(style_cfg["score_weight"]))]+[""]+list(set([t.name for t in lattice.grid.teams])-set(team.name))+[sides[k]])


def export_random_result(allocations, round_num, style_cfg, filename):
	if os.path.exists(filename):
		if not interaction_modules.overwrite("the file", filename, "already exists"):return
	with open(filename, "w") as g:
		writer = csv.writer(g)
		if style_cfg["team_num"] == 4:
			win_text = "Win-points[0, 1, 2, 3]"
			position_text = "Position[og, oo, cg, co]"
			sides = ["og", "oo", "cg", "co"]
		else:
			win_text = "Win[0:lose, 1:win]"
			position_text = "Side[gov, opp]"
			sides = ["gov", "opp"]
		writer.writerow(["team_name", "name"]+["R"+str(round_num)+"-"+str(i+1) for i in range(len(style_cfg["score_weight"]))]+[win_text]+["Opponent"+str(i+1) for i in range(style_cfg["team_num"]-1)]+[position_text])

		for lattice in allocations:
			teams_score_lists_raw = []
			for i in range(style_cfg["team_num"]):
				teams_score_lists_raw.append([random.randint(73, 77)*float(w) for w in style_cfg["score_weight"]])
			teams_member_lists_raw = [copy.copy(lattice.grid.teams[i].debaters) for i in range(style_cfg["team_num"])]
			teams_member_lists = [random.shuffle(team_member_list) for team_member_list in teams_member_lists_raw]

			teams_score_lists_all_info = []#=>[[ [a_1, a_2, a_3], [] ],[],[],[]]
			for team_score_list_raw in teams_score_lists_raw:
				team_score_list_all_info = []
				for score in team_score_list_raw:
					team_score_list_all_info.append([score + random.randint(-2,+2), score + random.randint(-2,+2), score + random.randint(-2,+2)])
				teams_score_lists_all_info.append(team_score_list_all_info)

			teams_score_lists_averaged = []
			for team_score_list_all_info in teams_score_lists_all_info:
				team_score_list_averaged = []
				for score_list in team_score_list_all_info:
					team_score_list_averaged.append(sum(score_list[0:len(lattice.panel)+1])/(len(lattice.panel)+1))
				teams_score_lists_averaged.append(team_score_list_averaged)

			if style_cfg["team_num"] == 4:
				sides = ["og", "oo", "cg", "co"]
			else:
				sides = ["gov", "opp"]
			teams_dict = {side: sum(team_score_list_raw) for side, team_score_list_raw in zip(sides, teams_score_lists_raw)}
			teams_dict_sorted = sorted(list(teams_dict.items()), key=lambda x:x[1])
			for i, k in enumerate(teams_dict_sorted):
				teams_dict[k[0]] = i

			win_points = [teams_dict[side] for side in sides]

			teams_score_lists_each = []

			if style_cfg["reply"]:
				reply_indexes = style_cfg["reply"]
				random.shuffle(reply_indexes)
				reply_indexes_chosen = reply_indexes[:style_cfg["num_of_reply"]]
				for team_score_list_averaged in teams_score_lists_averaged:
					team_score_lists_each = []
					for k in range(len(team_score_list_averaged)-1):
						team_score_list_each = [0 for i in range(len(style_cfg["score_weight"]))]
						team_score_list_each[k] = team_score_list_averaged[k]
						if k in reply_indexes_chosen:
							team_score_list_each[-1] = team_score_list_averaged[-1]
						team_score_lists_each.append(team_score_list_each)
					teams_score_lists_each.append(team_score_lists_each)
			else:
				for team_score_list_averaged in teams_score_lists_averaged:
					team_score_lists_each = []
					for k, score in enumerate(team_score_list_averaged):
						team_score_list_each = [0 for i in range(len(style_cfg["score_weight"]))]
						team_score_list_each[k] = score
						team_score_lists_each.append(team_score_list_each)
					teams_score_lists_each.append(team_score_lists_each)

			for k, team_score_list_each in enumerate(teams_score_lists_each):
				for j, score_list in enumerate(team_score_list_each):
					writer.writerow([lattice.grid.teams[k].name, lattice.grid.teams[k].debaters[j].name]+score_list+[win_points[k]]+list(set([t.name for t in lattice.grid.teams])-set([lattice.grid.teams[k].name]))+[sides[k]])					

def read_teams(filename, style_cfg, institution_list):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	debater_num_per_team = style_cfg["debater_num_per_team"]
	teams = []
	for code, raw_row in enumerate(reader):
		row = [raw_one.strip() for raw_one in raw_row]
		institutions = [institution for institution in institution_list if institution.name in row[1+debater_num_per_team]]
		if row[0] != '':
			teams.append(Team(code, row[0], [row[1+i] for i in range(debater_num_per_team)], institutions))#=>code, name, member_names
	return teams

def read_institutions(filename):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	institutions = []
	for code, raw_row in enumerate(reader):
		row = [raw_one.strip() for raw_one in raw_row]
		if row[0] != '':
			institutions.append(Institution(code, row[0], row[1]))#=>code, name, member_names
	return institutions

def create_rows_for_results_of_debaters(team_list, style_cfg):
	individual_score_rows = []
	score_weight = style_cfg["score_weight"]
	for team in team_list:
		for debater in team.debaters:
			row = [debater.name, team.name]
			for i, score_list in enumerate(debater.score_lists_sub):
				row.extend([round_str2float(score, 2) for score in score_list])
				avr = debater.average_in_round(i+1, style_cfg)
				if avr == 'n/a':
					row.append('n/a')
				else:
					row.append(round(avr, 2))
				
			row.insert(2, round(debater.average(style_cfg), 2))

			row.insert(2, round(debater.sum_scores(style_cfg), 2))
			row.insert(4, round(debater.sd(style_cfg), 2))
			individual_score_rows.append(row)

	header = ["ranking", "name", "team name", "sum", "average", "sd"]
	for i in range(int(len(individual_score_rows[0])-5)//(len(style_cfg["score_weight"])+1)):
		header.extend(["Round"+str(i+1)+"-"+str(j+1) for j in range(len(style_cfg["score_weight"]))]+["round"+str(i+1)+" average"])

	return [header]+individual_score_rows
	
def insert_ranking_for_results_of_debaters(individual_score_rows):
	individual_score_rows_cp = copy.copy(individual_score_rows)
	header = individual_score_rows_cp.pop(0)
	individual_score_rows_cp.sort(key=lambda row: (row[2], -row[4]), reverse=True)
	ranking = 1
	stay = 0
	for k in range(len(individual_score_rows_cp)-1):
		if individual_score_rows_cp[k][2] != individual_score_rows_cp[k+1][2]:
			individual_score_rows_cp[k].insert(0, ranking)
			ranking += 1 + stay
			stay = 0
		else:
			individual_score_rows_cp[k].insert(0, ranking)
			stay += 1
	individual_score_rows_cp[-1].insert(0, ranking)

	return [header] + individual_score_rows_cp

def create_rows_for_results_of_teams(team_list, style_cfg):
	score_rows = []
	for team in team_list:
		row = [team.name]
		scores2_sub = [round_str2float(score, 2) for score in team.scores_sub]

		row.append(team.sum_wins())
		row.append(round(team.sum_scores(), 2))
		row.append(round(team.margin, 2))
		row.append(round(team.average(), 2))
		row.append(round(team.sd(), 2))
		row.extend(scores2_sub)
		score_rows.append(row)

	if style_cfg["team_num"] == 2:
		win_text = "wins"
	else:
		win_text = "win-points"
	header = ["ranking", "team name"]+[win_text]+["sum", "margin", "average", "sd"]
	for i in range(len(score_rows[0])-6):
		header.append("round"+str(i+1))

	return [header]+score_rows

def insert_ranking_for_results_of_teams(score_rows, style_cfg):
	score_rows_cp = copy.copy(score_rows)
	header = score_rows_cp.pop(0)
	score_rows_cp.sort(key=lambda row: (row[1], row[2], row[3], -row[5]), reverse=True)

	ranking = 1
	stay = 0
	for k in range(len(score_rows_cp)-1):
		if score_rows_cp[k][2] != score_rows_cp[k+1][2] or score_rows_cp[k][1] != score_rows_cp[k+1][1] or score_rows_cp[k][3] != score_rows_cp[k+1][3]:
			score_rows_cp[k].insert(0, ranking)
			ranking += 1 + stay
			stay = 0
		else:
			score_rows_cp[k].insert(0, ranking)
			stay += 1
	score_rows_cp[-1].insert(0, ranking)

	return [header] + score_rows_cp

def create_rows_for_results_of_adjudicators(adjudicator_list):
	adjudicator_score_rows = []
	for adjudicator in adjudicator_list:
		row = [adjudicator.name, round(adjudicator.average(), 2), round(adjudicator.sd(), 2)] + [round_str2float(ele, 2) for ele in adjudicator.scores_sub]#->[name, average_score, scores]
		adjudicator_score_rows.append(row)

	header = ["ranking", "name", "average", "sd"]
	header += ["R"+str(i+1)+" average" for i in range(len(adjudicator_score_rows[0])-3)]

	return [header] + adjudicator_score_rows

def insert_ranking_for_results_of_adjudicators(adjudicator_score_rows):
	adjudicator_score_rows_cp = copy.copy(adjudicator_score_rows)
	header = adjudicator_score_rows_cp.pop(0)
	adjudicator_score_rows_cp.sort(key=lambda row: (row[1], -row[2]), reverse=True)

	ranking = 1
	stay = 0
	for k in range(len(adjudicator_score_rows_cp)-1):
		if adjudicator_score_rows_cp[k][1] != adjudicator_score_rows_cp[k+1][1]:
			adjudicator_score_rows_cp[k].insert(0, ranking)
			ranking += 1 + stay
			stay = 0
		else:
			adjudicator_score_rows_cp[k].insert(0, ranking)
			stay += 1

	adjudicator_score_rows_cp[-1].insert(0, ranking)

	return [header] + adjudicator_score_rows_cp

def create_rows_for_adj_info(adjudicator_list):
	adjudicator_score_rows = []
	for adjudicator in adjudicator_list:
		institutions_text = ""
		watched_teams_text = ""
		conflict_teams_text  = ""
		watched_teams = list(set(adjudicator.watched_teams))
		for institution in adjudicator.institutions:
			institutions_text += institution + ", "
		for watched_team in watched_teams:
			watched_teams_text += watched_team.name + ", "
		for conflict_team in adjudicator.conflict_teams:
			conflict_teams_text += conflict_team + ", "
		adjudicator_score_rows.append([str(adjudicator.active_num_as_chair), str(adjudicator.active_num-adjudicator.active_num_as_chair), institutions_text, conflict_teams_text, watched_teams_text])

	header = ["chair", "panel", "institutions", "conflict", "watched teams"]

	return [header]+adjudicator_score_rows

def export_adj_info(adjudicator_list, filename_adj_info):
	adjudicator_score_rows1 = create_rows_for_results_of_adjudicators(adjudicator_list)
	adjudicator_score_rows2 = create_rows_for_adj_info(adjudicator_list)
	adjudicator_score_rows = [row1+row2 for row1, row2 in zip(adjudicator_score_rows1, adjudicator_score_rows2)]

	adjudicator_score_rows_with_ranking = insert_ranking_for_results_of_adjudicators(adjudicator_score_rows)

	if os.path.exists(filename_adj_info):
		if not interaction_modules.overwrite("the file", filename_adj_info, "already exists"):
			return
	with open(filename_adj_info, "w") as g:
		writer = csv.writer(g)
		for row in adjudicator_score_rows_with_ranking:
			writer.writerow(row)

def export_results(tournament, filename_adj_res, filename_deb_res, filename_tm_res, style_cfg):
	individual_score_rows = create_rows_for_results_of_debaters(tournament["team_list"], style_cfg)
	individual_score_rows = insert_ranking_for_results_of_debaters(individual_score_rows)

	if os.path.exists(filename_adj_res):
		if not interaction_modules.overwrite("the file", filename_adj_res, "already exists"):
			return
	with open(filename_deb_res, "w") as g:
		writer = csv.writer(g)
		for row in individual_score_rows:
			writer.writerow(row)

	score_rows = create_rows_for_results_of_teams(tournament["team_list"], style_cfg)
	score_rows = insert_ranking_for_results_of_teams(score_rows, style_cfg)

	if os.path.exists(filename_tm_res):
		if not interaction_modules.overwrite("the file", filename_tm_res, "already exists"):return
	with open(filename_tm_res, "w") as g:
		writer = csv.writer(g)
		for row in score_rows:
			writer.writerow(row)
	
	adjudicator_score_rows = create_rows_for_results_of_adjudicators(tournament["adjudicator_list"])
	adjudicator_score_rows = insert_ranking_for_results_of_adjudicators(adjudicator_score_rows)

	if os.path.exists(filename_adj_res):
		if not interaction_modules.overwrite("the file", filename_adj_res, "already exists"):return
	with open(filename_adj_res, "w") as g:
		writer = csv.writer(g)
		for row in adjudicator_score_rows:
			writer.writerow(row)

def export_teams(filename_teams, team_list, style_cfg):
	with open(filename_teams, "w") as g:
		writer = csv.writer(g)
		writer.writerow(["team name"]+["name" for i in range(style_cfg["debater_num_per_team"])]+["institution1", "institution2", "institution3", "institution4", "institution5", "institution6"])
		for team in team_list:
			export_row = [team.name]+[d.name for d in team.debaters]
			export_row.extend(team.institutions)
			writer.writerow(export_row)

def export_institutions(filename_institutions, institution_list):
	with open(filename_institutions, "w") as g:
		writer = csv.writer(g)
		writer.writerow(["institution name", "scale"])
		for institution in institution_list:
			export_row = [institution.name, institution.scale]
			writer.writerow(export_row)
			


def save(tournament, fnames, style_cfg):
	export_filename_aj = fnames["export_filename_aj"]
	export_filename_vn = fnames["export_filename_vn"]
	export_filename_tm = fnames["export_filename_tm"]
	export_filename_is = fnames["export_filename_is"]
	with open(export_filename_aj, "w") as g:
		writer = csv.writer(g)
		for adjudicator in tournament["adjudicator_list"]:
			tf = 1 if adjudicator.absent else 0
			export_row = [adjudicator.name, tf, adjudicator.reputation, adjudicator.judge_test]
			export_row.extend(adjudicator.institutions)
			export_row.extend(["" for i in range(10-len(adjudicator.institutions))])
			export_row.extend(adjudicator.conflict_teams)
			writer.writerow(export_row)
	with open(export_filename_vn, "w") as g:
		writer = csv.writer(g)
		for venue in tournament["venue_list"]:
			tf = 1 if venue.available else 0
			export_row = [venue.name, tf, venue.priority]
			writer.writerow(export_row)
	with open(export_filename_tm, "w") as g:
		writer = csv.writer(g)
		for team in tournament["team_list"]:
			tf = 1 if team.available else 0
			export_row = [team.name, tf]
			export_row.extend([debater.name for debater in team.debaters])
			export_row.extend(team.institutions)
			writer.writerow(export_row)
	with open(export_filename_is, "w") as g:
		writer = csv.writer(g)
		for institution in tournament["institution_list"]:
			export_row = [institution.name, institution.scale]
			writer.writerow(export_row)
	export_teams(fnames["teams"], tournament["team_list"], style_cfg)
	export_venues(fnames["venues"], tournament["venue_list"])
	export_adjudicators(fnames["adjudicators"], tournament["adjudicator_list"])
	export_institutions(fnames["institutions"], tournament["institution_list"])

def load(tournament, style_cfg, fnames):
	export_filename_aj = fnames["export_filename_aj"]
	export_filename_vn = fnames["export_filename_vn"]
	export_filename_tm = fnames["export_filename_tm"]
	export_filename_is = fnames["export_filename_is"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	try:
		f = open(export_filename_is, 'r')
		reader = csv.reader(f)
		for row in reader:
			for institution in tournament["institution_list"]:
				if row[0] != institution.name:
					break
			else:
				new_institution = Institution(len(tournament["institution_list"]), row[0], row[1])
				tournament["institution_list"].append(new_institution)

		f = open(export_filename_aj, 'r')
		reader = csv.reader(f)
		for row in reader:
			for adjudicator in tournament["adjudicator_list"]:
				if row[0] == adjudicator.name:
					if int(row[1]) == 1:
						adjudicator.absent = True
					else:
						adjudicator.absent = False
			else:
				new_adj = Adjudicator(len(tournament["adjudicator_list"]), row[0], row[2], row[3], row[4:14], row[14:])
				new_adj.absent = True if int(row[1]) == 1 else False
				tournament["institution_list"].append(new_institution)
		f = open(export_filename_vn, 'r')
		reader = csv.reader(f)
		for row in reader:
			for venue in tournament["venue_list"]:
				if row[0] == venue.name:
					if int(row[1]) == 1:
						venue.available = True
					else:
						venue.available = False
					venue.priority = int(row[2])
					break
			else:
				new_venue = Venue(len(tournament["venue_list"]), row[0], row[2])
				new_venue.available = True if int(row[1]) == 1 else False
				tournament["venue_list"].append(new_venue)
		f = open(export_filename_tm, 'r')
		reader = csv.reader(f)
		for row in reader:
			for team in tournament["team_list"]:
				if row[0] == team.name:
					if int(row[1]) == 1:
						team.available = True
					else:
						team.available = False
					break
			else:
				institutions = [institution for institution in tournament["institution_list"] if institution.name in [ele.strip() for ele in row[2+debater_num_per_team:]]]
				new_team = Team(len(tournament["team_list"]), row[0], [row[2+i] for i in range(debater_num_per_team)], institutions)
				new_team.available = True if int(row[1]) == 1 else False
				tournament["team_list"].append(new_team)
	except:
		pass
		"""
		print "Unexpected error:", sys.exc_info()[0]
		print "load failed"
		"""






def read_matchup(filename_matchup, teamnum):
	f = open(filename_matchup, 'r')
	reader = csv.reader(f)
	header = next(reader)
	raw_data_rows = []
	for row in reader:
		raw_data_rows.append([row[i] for i in range(4+teamnum)])
	return raw_data_rows

def str2float(ele):
	if ele == "n":
		return 0
	else:
		return float(ele)

def read_venues(filename):
	venue_list = []
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	for j, row in enumerate(reader):
		venue_list.append(Venue(j, row[0], int(row[1])))
	return venue_list

def read_adjudicators(filename):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	csv_data = []

	for row in reader:
		csv_data.append(row)

	code = 0
	adjudicator_list = []
	for row in csv_data:
		if row[0] != '':
			adjudicator_list.append(Adjudicator(code, row[0], float(row[1]), float(row[2]), row[3:13], row[13:]))
			code += 1

	return adjudicator_list

def export_random_result_adj(allocations, round_num, style_cfg, filename):
	teamnum = style_cfg["team_num"]
	if os.path.exists(filename):
		if not interaction_modules.overwrite("the file", filename, "already exists"):return
	with open(filename, "w") as g:
		writer = csv.writer(g)
		if teamnum == 4:
			sides = ["og", "oo", "cg", "co"]
		elif teamnum == 2:
			sides = ["gov", "opp"]
		writer.writerow(["name"]+["R"+str(round_num)+" "+side for side in sides]+["R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair"]+["team"+str(i+1) for i in range(teamnum)])
		
		for lattice in allocations:
			adjudicator_base_scores = [random.randint(3,8), random.randint(3,8), random.randint(3,8)]
			chair_scores_all_info = [adjudicator_base_scores[0] + random.randint(-2,+2) for i in range(teamnum+2)]
			panels_scores = [random.randint(-2,+2) + adjudicator_base_scores[1], random.randint(-2,+2) + adjudicator_base_scores[2]]

			writer.writerow([lattice.chair.name]+[chair_scores_all_info[i] for i in range(teamnum+len(lattice.panel))]+[0 for i in range(2-len(lattice.panel))]+[0]+[team.name for team in lattice.grid.teams])
			for panel in lattice.panel:
				writer.writerow([panel.name]+[0 for i in range(teamnum+2)]+[panels_scores[0]]+[team.name for team in lattice.grid.teams])

			"""
			if len(lattice.panel) == 2:
				writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
			elif len(lattice.panel) == 1:
				writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
			else:
				writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
			"""
	"""
	if len(allocations[0].grid.teams) == 2:
		with open("private/Results_of_adj"+str(round_num)+".csv", "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" team1", "R"+str(round_num)+" team2", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2"])
			for lattice in allocations:
				chair_base_score = random.randint(3,8)
				chair_score_from_team1 = random.randint(-2,+2) + chair_base_score
				chair_score_from_team2 = random.randint(-2,+2) + chair_base_score
				chair_score_from_panel1 = random.randint(-2,+2) + chair_base_score
				chair_score_from_panel2 = random.randint(-2,+2) + chair_base_score
				panel1_base_score = random.randint(3,8)
				panel2_base_score = random.randint(3,8)
				panel1_score_from_chair = random.randint(-2,+2) + panel1_base_score
				panel2_score_from_chair = random.randint(-2,+2) + panel2_base_score

				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_panel1, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				else:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
	else:
		with open("private/Results_of_adj"+str(round_num)+".csv", "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" og", "R"+str(round_num)+" oo", "R"+str(round_num)+" cg", "R"+str(round_num)+" co", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2", "team3", "team4"])
			
			for lattice in allocations:
				chair_base_score = random.randint(3,8)
				chair_score_from_team1 = random.randint(-2,+2) + chair_base_score
				chair_score_from_team2 = random.randint(-2,+2) + chair_base_score
				chair_score_from_team3 = random.randint(-2,+2) + chair_base_score
				chair_score_from_team4 = random.randint(-2,+2) + chair_base_score
				chair_score_from_panel1 = random.randint(-2,+2) + chair_base_score
				chair_score_from_panel2 = random.randint(-2,+2) + chair_base_score
				panel1_base_score = random.randint(3,8)
				panel2_base_score = random.randint(3,8)
				panel1_score_from_chair = random.randint(-2,+2) + panel1_base_score
				panel2_score_from_chair = random.randint(-2,+2) + panel2_base_score

				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				else:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
	"""

def export_blank_results_of_adj(allocations, round_num, filename):
	if len(allocations[0].grid.teams) == 2:

		if os.path.exists(filename):
			if not interaction_modules.overwrite("the file", filename, "already exists"):return

		with open(filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" team1", "R"+str(round_num)+" team2", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2"])
			for lattice in allocations:
				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				else:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
	else:

		if os.path.exists(filename):
			if not interaction_modules.overwrite("the file", filename, "already exists"):return
		with open(filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" og", "R"+str(round_num)+" oo", "R"+str(round_num)+" cg", "R"+str(round_num)+" co", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2", "team3", "team4"])
			
			for lattice in allocations:
				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name,0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				else:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
	

def export_matchups(matchups, exportcode, round_num, workfolder_name):
	export_filename = workfolder_name+"temp/matchups_for_round_"+str(round_num)+"_"+str(exportcode)+".csv"

	if os.path.exists(export_filename):
		if not interaction_modules.overwrite("the file", export_filename, "already exists"):return

	with open(export_filename, "w") as g:
		writer = csv.writer(g)
		if len(matchups[0].teams) == 2:
			header = ["Gov", "Opp", "Chair", "Panel1", "Panel2", "Venue", "Warnings"]
		elif len(matchups[0].teams) == 4:
			header = ["OG", "OO", "CG", "CO", "Chair", "Panel1", "Panel2", "Venue", "Warnings"]
		writer.writerow(header)
		for grid in matchups:
			export_row = [team.name for team in grid.teams]+["", "", "", ""]
			export_row.extend(grid.warnings)
			writer.writerow(export_row)

def export_allocations(allocations, exportcode, round_num, workfolder_name):
	export_filename = workfolder_name+"temp/matchups_for_round_"+str(round_num)+"_"+str(exportcode)+".csv"
	if os.path.exists(export_filename):
		if not interaction_modules.overwrite("the file", export_filename, "already exists"):return
		input("Press Enter to overwrite the file > ")
	if len(allocations[0].grid.teams) == 2:
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["Gov", "Opp", "Chair", "Panel1", "Panel2", "Venue", "Warnings"])
			for lattice in allocations:
				if lattice.venue:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name]
				else:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", ""]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", ""]
				export_row.extend(lattice.warnings)
				writer.writerow(export_row)
	else:
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["OG", "OO", "CG", "CO", "Chair", "Panel1", "Panel2", "Venue", "Warnings"])
			for lattice in allocations:
				if lattice.venue:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, "", "", lattice.venue.name]
				else:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, "", ""]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, "", "", ""]
				export_row.extend(lattice.warnings)
				writer.writerow(export_row)

def export_official_matchups(allocations, round_num, workfolder_name):
	export_filename = workfolder_name+"public/matchups_for_round_"+str(round_num)+".csv"
	if os.path.exists(export_filename):
		if not interaction_modules.overwrite("the file", export_filename, "already exists"):return

	if len(allocations[0].grid.teams) == 2:
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["Gov", "Opp", "Chair", "Panel1", "Panel2", "Venue"])
			for lattice in allocations:
				if lattice.venue:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name]
				else:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", ""]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", ""]
				writer.writerow(export_row)
	else:
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["OG", "OO", "CG", "CO", "Chair", "Panel1", "Panel2", "Venue"])
			for lattice in allocations:
				if lattice.venue:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, "", "", lattice.venue.name]
				else:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, "", ""]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, "", "", ""]
				writer.writerow(export_row)

def export_venues(filename_venues, venue_list):
	with open(filename_venues, "w") as g:
		writer = csv.writer(g)
		writer.writerow(["name", "priority"])
		for venue in venue_list:
			export_row = [venue.name, venue.priority]
			writer.writerow(export_row)

def export_adjudicators(filename_adjudicators, adjudicator_list):
	with open(filename_adjudicators, "w") as g:
		writer = csv.writer(g)
		header = ["name", "Reputation[0, 10]", "Judge test[0, 10]"]+["institution"]*10+["conflicting team"]*10
		writer.writerow(header)
		for adjudicator in adjudicator_list:
			export_row = [adjudicator.name, adjudicator.reputation, adjudicator.judge_test]
			institutions = [""]*10
			for k, institution in enumerate(adjudicator.institutions):
				institutions[k] = institution
			conflict_teams = [""]*10
			for k, conflict_team in enumerate(adjudicator.conflict_teams):
				conflict_teams[k] = conflict_team
			export_row.extend(institutions)
			export_row.extend(conflict_teams)
			writer.writerow(export_row)

def export_dummy_results_adj(allocations, round_num, style_cfg, workfolder_name):
	if len(allocations[0].grid.teams):
		with open(workfolder_name+"dummyresults/Results_of_adj"+str(round_num)+".csv", "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" team1", "R"+str(round_num)+" team2", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2"])
			
			for lattice in allocations:
				chair_base_score = random.randint(3,8)
				chair_score_from_team1 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_team2 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_panel1 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_panel2 = 0#random.randint(-2,+2) + chair_base_score
				panel1_base_score = random.randint(3,8)
				panel2_base_score = random.randint(3,8)
				panel1_score_from_chair = 0#random.randint(-2,+2) + panel1_base_score
				panel2_score_from_chair = 0#random.randint(-2,+2) + panel2_base_score

				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_panel1, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				else:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
	else:
		with open(workfolder_name+"dummyresults/Results_of_adj"+str(round_num)+".csv", "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" team1", "R"+str(round_num)+" team2", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2"])
			
			for lattice in allocations:
				chair_base_score = random.randint(3,8)
				chair_score_from_team1 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_team2 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_team3 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_team4 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_panel1 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_panel2 = 0#random.randint(-2,+2) + chair_base_score
				panel1_base_score = random.randint(3,8)
				panel2_base_score = random.randint(3,8)
				panel1_score_from_chair = 0#random.randint(-2,+2) + panel1_base_score
				panel2_score_from_chair = 0#random.randint(-2,+2) + panel2_base_score

				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				else:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])

def reset_except_dat_cfg(workfolder_name):
	filename_list = ['temp/tm.csv', 'temp/vn.csv', 'temp/aj.csv', 'private/final_result/Results_of_adjudicators.csv', 'private/final_result/Results_of_debaters.csv', 'private/final_result/Results_of_teams.csv']
	filename_list.extend(['private/Results'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/Results_of_adj'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['blankresults/Results'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['blankresults/Results_of_adj'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['dummyresults/Results'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['dummyresults/Results_of_adj'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['public/matchups_for_round_'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['matchups_imported/matchups_for_round_'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/round_info/Results_of_debaters_by_R'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/round_info/Results_of_teams_by_R'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/round_info/Results_of_adjudicators_by_R'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/round_info/Adjudicators_info_by_R'+str(i)+'.csv' for i in range(50)])
	filename_list = [workfolder_name+filename for filename in filename_list]
	for filename in filename_list:
		try:
			os.remove(filename)
			#print filename
		except:
			continue

	try:
		shutil.rmtree(workfolder_name+"temp")
		os.mkdir(workfolder_name+"temp")
	except:
		pass

	#return to_folder




pass