# Adjudicator Results

[/v1.0/{tournament_name}/{round_num}/results/adjudicators]

### List Adjudicator Results [GET]

+ Response 200 (application/json)
```
{
    "errors": null,
    "data": undef
}
```
### Send Adjudicator Result [PUT]

+ Request (application/json)
```
{
    "override": false,
    "result":
    {
        "from": "chair", /* "chair", "panel", or "team" */
        "from_id": 34, /* sender's id */
        "chair": true, /* if the adj to be evaluated was a chair */
        "adjudicator_id": 2, /* id of adj to be evaluated */
        "score": 8,
        "teams": [1, 2], /* teams' ids that the adj judged (必要?) */
        "comment": "worst judge ever",
        "round": 1
    }
}
```
+ Response 200 (application/json)
```
{
    "errors": null,
    "data" : null
}
```