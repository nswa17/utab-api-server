from .tools import *

class Team:
	def __init__(self, code, name, url, debaters, institutions):
		self.code = code
		self.name = name
		self.url = url
		self.institutions = institutions
		self.debaters = debaters
		self.past_opponents = []
		self.past_sides = []
		self.past_sides_sub = []
		self.wins = []
		self.wins_sub = []
		self.scores = []
		self.scores_sub = []
		self.score = 0
		self.margin = 0
		self.ranking = 0
		self.available = True
		for debater in self.debaters:
			debater.team = self

	def get_debater_of_id(self, code):
		return find_element_by_id(self.debaters, code)

	def is_belonging(self, debater_or_code):
		if type(debater_or_code) == 'int':
			return debater_or_code in [d.code for d in self.debaters]
		else:
			return debater_or_code in self.debaters

	def average(self):
		if len(self.scores) == 0:
			return 0
		else:
			return sum(self.scores)/len(self.scores)

	def sum_scores(self):
		return sum(self.scores)

	def sum_wins(self):
		return sum(self.wins)

	def sd(self):
		if len(self.scores) == 0:
			return 0
		else:
			avrg = self.average()
			return math.sqrt(sum([(score - avrg)**2 for score in self.scores])/len(self.scores))

	def __eq__(self, other):
		return self.code == other

	def __ne__(self, other):
		return self.code != other

	def __hash__(self):
		return self.code

	def __str__(self):
		return self.name

	def finishing_process(self, opponents, score, position, win_point, margin):
		self.past_opponents.extend(opponents)
		self.past_sides.append(position)
		self.past_sides_sub.append(position)
		self.scores.append(score)
		self.score = score
		self.wins.append(win)
		self.scores_sub.append(score)
		self.wins_sub.append(win_point)
		self.margin += margin

	def dummy_finishing_process(self):
		self.scores_sub.append('n/a')
		self.wins_sub.append('n/a')
		self.past_sides_sub.append('n/a')

class Adjudicator:
	def __init__(self, code, name, url, reputation, judge_test, institutions, conflict_teams):
		self.code = code
		self.name = name
		self.url = url
		self.reputation = reputation
		self.judge_test = judge_test
		self.institutions = [institution for institution in institutions if institution != '']
		self.absent = False#absent?
		self.score = 0
		self.scores = []
		self.scores_sub = []
		self.watched_debate_score = 0
		self.watched_debate_scores = []
		self.watched_debate_scores_sub = []
		self.watched_debate_ranks = []
		self.watched_debate_ranks_sub = []
		self.watched_teams = []
		self.watched_teams_sub = []
		self.active_num = 0
		self.active_num_as_chair = 0
		self.ranking = 0
		self.active = False
		self.evaluation = 0
		self.conflict_teams = [conflict_team for conflict_team in conflict_teams if conflict_team != '']
		self.comments_list = []

	def __hash__(self):
		return self.code

	def average(self):
		if len(self.scores) == 0:
			return 0
		else:
			return sum(self.scores)/len(self.scores)

	def sum_scores(self):
		return sum(self.scores)

	def sd(self):
		if len(self.scores) == 0:
			return 0
		else:
			avrg = self.average()
			return math.sqrt(sum([(score - avrg)**2 for score in self.scores])/len(self.scores))

	def finishing_process(self, score, teams, watched_debate_score, chair, comments):
		self.score = score
		self.scores.append(score)
		self.scores_sub.append(score)
		self.active_num += 1
		self.active = False
		if chair:
			self.active_num_as_chair += 1
		self.watched_teams.extend(teams)
		self.watched_teams_sub.extend(teams)
		self.watched_debate_score = watched_debate_score
		self.watched_debate_scores.append(watched_debate_score)
		self.watched_debate_scores_sub.append(watched_debate_score)
		self.comments_list.append(comments)

	def dummy_finishing_process(self, team_num):
		self.scores_sub.append('n/a')
		self.watched_debate_scores_sub.append('n/a')
		self.watched_teams_sub.extend(['n/a' for i in range(team_num)])

	def __eq__(self, other):
		return self.code == other

	def __ne__(self, other):
		return self.code != other

	def __hash__(self):
		return self.code

	def __str__(self):
		return self.name

class Institution:
	def __init__(self, code, name, url, scale):
		self.code = code
		self.name = name
		self.url = url
		self.scale = scale

	def __eq__(self, other):
		return self.code == other

	def __ne__(self, other):
		return self.code != other

	def __hash__(self):
		return self.code

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name

	def __unicode__(self):
		return self.name

class Debater:
	def __init__(self, code, name, url):
		self.code = code
		self.name = name
		self.url = url
		self.team = None
		self.score_lists = []
		self.scores = []
		self.score_lists_sub = []
		self.scores_sub = []

	def average(self, style_cfg):
		score_weight = style_cfg["score_weight"]
		average_list = []
		for i in range(len(self.score_lists_sub)):
			avrg_in_r = self.average_in_round(i+1, style_cfg)
			if avrg_in_r != 'n/a':
				average_list.append(avrg_in_r)

		if len(average_list) == 0:
			return 0
		else:
			return sum(average_list)/len(average_list)

	def average_in_round(self, round_num, style_cfg):
		score_weight = style_cfg["score_weight"]
		average_list = []
		weight = 0
		avrg = 0
		if 'n/a' in self.score_lists_sub[round_num-1]:
			return 'n/a'
		else:
			for score, w in zip(self.score_lists_sub[round_num-1], score_weight):
				if score != 0:
					avrg += score
					weight += w
			if weight != 0:
				return avrg/weight
			else:
				return 0

	def sum_scores(self, style_cfg):
		s = 0
		for i in range(len(self.score_lists)):
			avrg_in_r = self.average_in_round(i+1, style_cfg)
			if avrg_in_r != 'n/a':
				s += avrg_in_r
		return s

	def sd(self, style_cfg):
		avrg = self.average(style_cfg)
		sd = 0
		n = 0
		for i in range(len(self.score_lists_sub)):
			avrg_in_r = self.average_in_round(i, style_cfg)
			if avrg_in_r != 'n/a':
				sd += (avrg_in_r-avrg)**2
				n += 1
		if n == 0:
			return 0
		else:
			return math.sqrt(sd/n)

	def finishing_process(self, score_list, score):
		self.score_lists.append(score_list)
		self.score_lists_sub.append(score_list)
		self.scores.append(score)
		self.scores_sub.append(score)

	def dummy_finishing_process(self, style_cfg):
		self.score_lists_sub.append(['n/a']*len(style_cfg["score_weight"]))
		self.scores_sub.append('n/a')

	def __eq__(self, other):
		return self.code == other

	def __ne__(self, other):
		return self.code != other

	def __hash__(self):
		return self.code

	def __str__(self):
		return self.name

class Venue:
	def __init__(self, code, name, url, available, priority):
		self.code = code
		self.name = name
		self.available = available
		self.priority = priority
		self.url = url

	def __hash__(self):
		return self.code

	def __str__(self):
		return self.name

		