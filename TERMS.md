# 統一用語集

## UTab name

You should use UTab instead utab or Utab.

## team allocation

* suggested team allocations (list)
* team allocation (object)

## judge allocation

* suggested judge allocations (list)
* judge allocation (object)

## venue allocation

* suggested venue allocation (object. not list!)
* venue allocation (object)

## modify publicated matchup

* matchup
* modified matchup

## Difference between Grid and Lattice

```python

class Grid(GL):
	def __init__(self, teams):
		self.teams = teams

class Lattice(GL):
	def __init__(self, grid, chair):
		self.grid = grid
		self.chair = chair
		self.panel = []
		self.venue = None
```

## Word usage

1. You should not use abbreviated form of a word unless it is common and can be seen as a formal form.
ex. `adjudicator` is much preferred to `adj`. `args` is no less preferred to `arguments`.

2. 
