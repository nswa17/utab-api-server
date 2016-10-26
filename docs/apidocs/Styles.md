# Styles 

[/v1.0/styles]

### List All Styles [GET]

+ Response 200 (application/json)
```
{
    "errors": null,
    "data":
    [
        {
            "style_name": "PDA",
            "debater_num_per_team": 4,
            "team_num": 2,
            "score_weights": [1, 1, 1, 0.5],
            "replies": [0, 1], /*replier candidates. if either 1st or 2nd speaker may do reply, [0, 1] */
            "num_of_replies_per_team": 1
        }
    ],
    "resource_url": ""
}
```