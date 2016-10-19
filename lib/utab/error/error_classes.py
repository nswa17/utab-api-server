# -*- coding: utf-8 -*-

class SameInstitution(Exception):
	def __init__(self, institution):
		self.institution = institution

	def __str__(self):
		return self.shortwarning()

	def shortwarning(self):
		return "wrn(same insti("+self.institution.scale+"))"

	def longwarning(self):
		return "warning : a team matching with the same institution(scale:"+self.institution.scale+")"

class PastOpponent(Exception):
	def __init__(self, team1, team2):
		self.team1 = team1
		self.team2 = team2

	def __str__(self):
		return self.shortwarning()

	def shortwarning(self):
		return "wrn(past opponent)"

	def longwarning(self):
		return "warning : a team matching again with past opponent: "+self.team1.name+self.team2.name

class Sided(Exception):
	def __init__(self, team, side, side_counts):
		self.team = team
		self.side = side
		self.side_counts = side_counts

	def __str__(self):
		return self.shortwarning()

	def shortwarning(self):
		return "wrn(unfair side)"

	def longwarning(self):
		string = "(" + ":".join([str(i) for i in self.side_counts])+")"
		return "warning : a team's side unfair :"+str(self.team.name)+string

class AllSided(Exception):
	def __init__(self, team, side, side_count):
		self.team = team
		self.side = side
		self.side_count = side_count

	def __str__(self):
		return self.shortwarning()

	def shortwarning(self):
		return "wrn(one sided)"

	def longwarning(self):
		return "warning : a team's side all {0} ({1})".format(self.side, self.team.past_sides.count(self.side))

class PowerPairing(Exception):
	def __init__(self, team1, team2, difference):
		self.team1 = team1
		self.team2 = team2
		self.difference = difference

	def __str__(self):
		return self.shortwarning()

	def shortwarning(self):
		return "wrn(diff {0:d}%, {1}:{2})".format(self.difference, sum(self.team1.wins), sum(self.team2.wins))

	def longwarning(self):
		return "warning : stronger vs weaker team, {0:12s}:{1:12s}, ranking difference: {2:d}%, wins: {3:d}-{4:d}".format(self.team1.name, self.team2.name, self.difference, sum(self.team1.wins), sum(self.team2.wins))

class PersonalConflict(Exception):
	def __init__(self, adjudicator, teams):
		self.adjudicator = adjudicator
		self.teams = teams

	def __str__(self):
		return self.shortwarning()

	def shortwarning(self):
		return "wrn(perso conflict)"

	def longwarning(self):
		return "warning : a judge watching a team of his/her personal conflict :"+"-".join([t.name for t in self.teams])+": "+str(self.adjudicator.conflict_teams)

class InstitutionConflict(Exception):
	def __init__(self, adjudicator, teams):
		self.adjudicator = adjudicator
		self.teams = teams

	def __str__(self):
		return self.shortwarning()

	def shortwarning(self):
		return "wrn(insti conflict)"

	def longwarning(self):
		return "warning : a judge watching a team of his/her conflict :"+"-".join([t.name for t in self.teams])+": "+str(self.adjudicator.institutions)

class BubbleRound(Exception):
	def __init__(self, teams):
		self.teams = teams

	def __str__(self):
		return self.shortwarning()

	def shortwarning(self):
		return "att(bbl "+":".join([str(sum(t.wins)) for t in self.teams])+")"

	def longwarning(self):
		return "attention : bubble round :"+"-".join([t.name for t in self.teams])+": "+"-".join([str(sum(t.wins)) for t in self.teams])

class WatchingAgain(Exception):
	def __init__(self, adjudicator, teams):
		self.adjudicator = adjudicator
		self.teams = teams

	def __str__(self):
		return self.shortwarning()

	def shortwarning(self):
		return "wrn(watching again)"

	def longwarning(self):
		return "warning : a judge watching a team again :"+"-".join([t.name for t in self.teams])+": "+self.adjudicator.name+"("+",".join([t.name for t in self.adjudicator.watched_teams])+")"
