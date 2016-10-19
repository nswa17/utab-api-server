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