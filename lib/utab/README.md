# UTab

## ROLE OF EACH MODULE

 * main: model
 * internal: functions for internal process of grids/lattices
 * result: functions to process results
 * tournament: classes to operate a tournament
 * entity_classes: classes of Team/Adj/Venue/Debater/Institution
 * grid_classes: internal classes for algorithm
 * error_classes: classes related to matchup warnings
 * properties: extract information from grids/lattices
 * filters: functions to add adoptness for grids/lattices
 * select: functions to choose best grids/lattices
 * bit: wrappers for bit calculation on adoptness
 * tools: tools

## Structure

```
main______src.tournament
        |
        |_src.internal
        |    |
        |    |_src.properties
        |    |
        |    |_src.grid_classes
        |    |    |_src.bit
        |    |
        |    |_src.entity_classes
        |    |    |_src.tools
        |    |
        |    |_src.selects
        |    |    |_src.properties
        |    |    |_src.grid_classes
        |    |    	    |_src.properties
        |    |
        |    |_src.filters
        |         |_src.bit
        |         |_src.properties
        |_src.bit
        |
    	|_src.result
        |    |_src.tools
        |
    	|_src.entity_classes
             |_src.tools
```
