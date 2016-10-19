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

```
 model____classes
            |
            |_internal
            |    |
            |    |_properties
            |    |
            |    |_grid_classes
            |    |    |_bit
            |    |
            |    |_entity_classes
            |    |    |_tools
            |    |
            |    |_select
            |    |    |_property
            |    |    |_grid_classes
            |    |    	    |_properties
            |    |
            |    |_filters
            |         |_bit
            |         |_properties
            |_bit
            |
        	|_result
            |    |_tools
            |
        	|_entity_classes
                 |_tools
```
