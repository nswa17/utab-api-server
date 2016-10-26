# Specific Tournament

[/v1.0/tournament/{tournament_id}]

### Delete Tournament [DELETE]

+ Request (application/json)

```json
        {
            "id": 0,
            "name": "testtournament"
        }

+ Response 200 (application/json)
```json
        {
            "errors": null,
            "data":
            {
                "id": 0,
                "name": "testtournament"
            },
            "resource_url": ""
        }
```

# Available Styles

[/v2.0/styles]

### Add An User Defined Style [PUT]

+ Request (application/json)
```json
        {
            "style_name": "PDA",
            "debater_num_per_team": 4,
            "team_num": 2,
            "score_weights": [1, 1, 1, 0.5],
            "replies": [0, 1],
            "num_of_replies_per_team": 1
        }
```
+ Response 200 (application/json)
```json
        {
            "errors": null,
            "data": same as above,
            "resource_url": ""
        }
```

# Team Allocation

[/v2.0/{tournament_name}/{round_num}/suggested_team_allocations/{allocation_id}]

### Get Team Allocation [GET]

+ Response 200 (application/json)
```json
        {
            "errors": [],
            "data":
            {
                "algorithm": "",
                "indices": {
                    "power_pairing_indicator": 1.0,
                    "adopt_indicator": 1,
                    "adopt_indicator2": 2,
                    "adopt_indicator_sd": 10,
                    "gini_index": 0.0,
                    "scatter_indicator": 0.0
                },
                "large_warings": [""],
                "allocation": [
                    {
                        "teams": [0, 1],
                        "chairs": [],
                        "panels": [],
                        "trainees": [],
                        "venue": null,
                        "warnings": [""]
                    }
                ],
                "allocation_no": 0
            },
            "resource_url": ""
        }
```

* `power_pairing_indicator` 1 <-> inf
* `adopt_indicator` the higher the better
* `adopt_indicator2` the higher the better
* `adopt_indicator_sd` Standard Diviation
* `gini_index` 0 <-> 1
* `scatter_indicator` the lower the better

# Adjudicator Allocation

[/v2.0/{tournament_name}/{round_num}/suggested_adjdicator_allocations/{allocation_id}]

### Get Adudicator Allocation [GET]

+ Response 200 (application/json)
```json
        {
            "errors": [],
            "data":
            {
                "algorithm": "",
                "indices": {

                },
                "large_warings": [""],
                "allocation":
                [
                    {
                        "warnings": [""],
                        "teams": [0, 1],
                        "chairs": [0],
                        "panels": [1, 2],
                        "venue": null,
                        "trainees": []
                    }
                ]
            },
            "resource_url": ""
        }
```
# Specific Adjudicator

[/v2.0/{tournament_name}/adjudicators/{adjudicator_id}]

### Update Adjudicator [PUT] /* if not exist, returns an error */

+ Request (application/json)

        same as create adjudicator

+ Response 200 (application/json)

        same as create adjudicator

### Delete An Adjudicator [DELETE]

+ Request (application/json)
```json
        {
            "id": 3,
            "name": "kym"
        }
```
+ Response 200 (application/json)
```json
        {
            "errors": null,
            "data":
            {
                "id": 3,
                "name": "kym"
            }
        }
```
# Specific Speaker

[/v2.0/{tournament_name}/speakers/{speaker_id}]

### Create/Update-if-exist Speaker [PUT]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (application/json)
```json
        {
        }
```
### Delete A Speaker [DELETE]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (application/json)
```json
        {
        }
```
# Specific Team

[/v2.0/{tournament_name}/teams/{team_id}]

### Create/Update-if-exist Team [PUT]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (text/plain)
```json
        "Thank you, "
```
### Update Team [PATCH]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (application/json)
```json
        {
        }
```
### Delete Team [DELETE]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (application/json)
```json
        {
        }
```
# Venues 

[/v2.0/{tournament_name}/venues]

### Create/Update-if-exist Venue [PUT]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (application/json)
```json
        {
        }
```
### Update Venue [PATCH]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (application/json)
```json
        {
            "hello": 3
        }
```
### Delete Venue [DELETE]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (application/json)
```json
        {
        }
```
# Specific Institution

[/v2.0/{tournament_name}/institutions/{institution_id}]

### Create/Update-if-exist Institution [PUT]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (application/json)
```json
        {
        }
```
### Update Institution [PATCH]

+ Request (application/json)
```json
        {
        }
```
+ Response 200 (application/json)
```json
        {
        }
```
### Delete Institution [DELETE]

+ Request (application/json)
```json
        {
        }
```

+ Response 200 (application/json)
```json
        {
        }
```

# Total Team Results

[/v2.0/{tournament_name}/results/teams]

### Modify Results [POST]

# Total Adjudicator Results

[/v2.0/{tournament_name}/results/adjudicators]

### Modify Results [POST]

# Total Speaker Results

[/v2.0/{tournament_name}/results/speakers]

### Modify Results [POST]

# Backups

[/v2.0/{tournament_name}/backups]

### Save Current State [POST]

+ Request (application/json)
```json
        {
            "errors": null,
            "data":
            {
                "comment": "backupthis"
            }
        }
```

+ Response 200 (application/json)
```json
        {
            "errors":null,
            "data":
            [
                {
                    "date": "2016/01/04-23:59:10",
                    "comment": "test",
                    "backup_code": "fda23fds"
                }
            ],
            "resource_url": ""
        }
```

# Adjudicator Comments

[/v2.0/{tournament_name}/results/adjudicators/comments]

### Download Comments on Adjudicator [GET]

+ Response 200 (application/json)
```json
        {
            "errors":null,
            "data":
            [
                {
                    "round": 1,
                    "comments":
                    [
                        {
                            "comment": "worst judge ever",
                            "from": "team",
                            "from_id": 23,
                            "from_name": "UTK1"
                        }
                    ]
                }
            ],
            "resource_url": ""
        }
```
