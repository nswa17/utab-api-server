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
tournament
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

## Usage

```python
    tournament = Tournament(tournament_code, tournament_name, round_num, style)

    #                           #
    #    ARRANGING TOURNAMENT   #
    #                           #

    for i in range(round_num):

        while True:

            #                       #
            #    ARRANGING ROUND    #
            #                       #

            try:
                round = tournament.round(force=False)
                break
            except:
                pass

        round.compute_matchups()
        round.set_matchup(matchup)

        round.compute_allocations()
        round.set_allocation(allocation)

        round.compute_panel_allocation()
        round.set_panel_allocation(panel_allocation)

        round.compute_venue_allocation()
        round.set_venue_allocation(venue_allocation)

        while True:

            #                           #
            #     COLLECTING RESULTS    #
            #                           #

            round.process_result(force=False)##########endと統合?
            round.process_result_of_adj(force=False)##########endと統合?
            round.end(force=False) && break
        
    tournament.end()
```