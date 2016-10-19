from bit import *

class GL:
	def __init__(self):
		self.adoptbits = 0
		self.adoptbitslong = 0
		self.adoptbits_strict = 0
		self.adoptness1 = 0
		self.adoptness2 = 0
		self.adoptness1long = 0
		self.adoptness2long = 0
		self.adoptness_strict1 = 0
		self.adoptness_strict2 = 0
		self.adoptness_weight1 = 0
		self.adoptness_weight2 = 0
		self.availables = [True]*49
		self.warnings = []
		self.large_warnings = []

	def get_available(self, pid):
		return self.availables[pid]

	def set_available(self, *args):
		if len(args) == 0:
			self.availables = [True]*49
		else:
			self.availables[args[0]] = True

	def set_not_available(self, *args):
		if len(args) == 0:
			self.availables = [False]*49
		else:
			self.availables[args[0]] = False

	def set_adoptness1(self):
		for k, bit in enumerate(eachbit(self.adoptbits)):
			if bit == 0:
				self.adoptness1 = k
				break

	def set_adoptness2(self):
		count = 0
		for k, bit in enumerate(eachbit(self.adoptbits)):
			if bit == 1:
				count += 1
		self.adoptness2 = count

	def set_adoptness1long(self):
		for k, bit in enumerate(eachbit(self.adoptbitslong)):
			if bit == 0:
				self.adoptness1long = k
				break
		
	def set_adoptness2long(self):
		count = 0
		for k, bit in enumerate(eachbit(self.adoptbitslong)):
			if bit == 1:
				count += 1
		self.adoptness2long = count
		
	def set_adoptness_strict1(self):
		for k, bit in enumerate(eachbit(self.adoptbits_strict)):
			if bit == 0:
				self.adoptness_strict1 = k
				break
		
	def set_adoptness_strict2(self):
		count = 0
		for k, bit in enumerate(eachbit(self.adoptbits_strict)):
			if bit == 1:
				count += 1
		self.adoptness_strict2 = count
		
	def set_adoptness_weight1(self):
		count = 0
		for k, bit in enumerate(eachbit(self.adoptbits_strict)):
			if bit == 1:
				count += 1-k*0.04
		self.adoptness_weight1 = count
		
	def set_adoptness_weight2(self):
		count = 0
		for k, bit in enumerate(eachbit(self.adoptbitslong)):
			if bit == 1:
				count += 1-k*0.04
		self.adoptness_weight2 = count

	def set_adoptness(self):
		self.set_adoptness1()
		self.set_adoptness2()
		self.set_adoptness1long()
		self.set_adoptness2long()
		self.set_adoptness_strict1()
		self.set_adoptness_strict2()
		self.set_adoptness_weight1()
		self.set_adoptness_weight2()

class Grid(GL):
	def __init__(self, teams):
		GL.__init__(self)
		self.teams = teams
		self.past_match = 0
		self.power_pairing = None
		self.related_grids = []
		self.bubble_ranking = 0
		self.bubble = 10

	def initialize(self):
		GL.__init__(self)
		self.past_match = 0
		self.power_pairing = None
		self.bubble_ranking = 0
		self.bubble = 10

	def related(self, grid2):
		for team in self.teams:
			if team in grid2.teams:
				return True
		else:
			return False

	def __eq__(self, other):
		if self.teams == other.teams:
			return True
		else:
			return False

	def __ne__(self, other):
		if self.teams != other.teams:
			return True
		else:
			return False

	def __hash__(self):
		hash_value = 0
		for k, team in enumerate(self.teams):
			hash_value += team.code<<10*k
		return hash_value

	def __str__(self):
		string = ""
		for team in self.teams:
			string = string + team.name
		return string

class Lattice(GL):
	def __init__(self, grid, chair):
		GL.__init__(self)
		self.grid = grid
		self.chair = chair
		self.panel = []
		self.venue = None
		#self.avoid_by_conflict = False
		#self.adj_unfair = False
		#self.strength_coordinating = 0
		#self.uncoordinateness = 0
		#self.conflict = False
		#self.personal_conflict = False

	def related(self, lattice2):
		if self.chair == lattice2.chair:
			return True
		else:
			return self.grid.related(lattice2.grid)

	def __eq__(self, other):
		if self.chair == other.chair and self.grid.teams == other.grid.teams:
			return True
		else:
			return False

	def __ne__(self, other):
		if self.chair != other.chair or self.grid.teams != other.grid.teams:
			return True
		else:
			return False

	def __hash__(self):
		hash_value = ord(self.chair.name[0])
		for k, team in enumerate(self.grid.teams):
			hash_value += team.code<<10*k
		return hash_value

	def __str__(self):
		string = self.chair.name + ":" if self.chair else ""
		for team in self.grid.teams:
			string = string + team.name
		return string

	def grid_type(self):
		return self.__class__.__name__

class Grid_list(list):
	def __init__(self, *args):
		list.__init__(self, *args)
		self.power_pairing_indicator = None
		self.adopt_indicator = None
		self.adopt_indicator_sd = None
		self.adopt_indicator2 = None
		self.same_institution_indicator = None
		self.num_of_warnings = None
		self.scatter_indicator = None
		self.matchups_no = None
		self.large_warnings = []
		self.comment = ""
		self.grid_type = "Grid"
		self.internal_algorithm = ""

class Lattice_list(list):
	def __init__(self, *args):
		list.__init__(self, *args)
		self.strong_strong_indicator = None
		self.num_of_warnings = None
		self.large_warnings = []
		self.allocation_no = None
		self.comment = ""
		self.grid_type = "Lattice"
		self.internal_algorithm = ""

		