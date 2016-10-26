# Speaker Results

[/v1.0/{tournament_name}/{round_num}/results/speakers]

### List Speaker Results [GET]

+ Response 200 (application/json)

preparing

### Send Speaker Result [PUT]

+ Request (application/json)
```
{
    "override": false,
    "result":
    {
        "from_id": 3, /* adj id */
        "debater_id": 34,
        "current_round": 1,/* round1 => 1 */
        "team_id": 1,
        "scores": [76, 0, 38.5], /* 0 if he/she has no role */
        "win_point": 1 /* in NA, 1=win, 0=lose in BP, it must be win-points the team get */,
        "opponents": [2],
        "side": "gov" /* in BP, "og", "oo", "cg", "co". in 2side game, "gov", "opp"
    }
}
```
+ Response 200 (application/json)
```
{
    "errors": null,
    "data": (same as above),
    "resource_url": ""
}
```