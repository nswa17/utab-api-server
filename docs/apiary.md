FORMAT: 1A
HOST: http://polls.apiblueprint.org/

# UTabAPIs

By which you can operate UTab  (Todo: backup, import)

Version: v0.1

speaker, institution -> team

institution -> adjudicator

Get -> GET
Create -> POST(force=false)
Create/Update-if-exist -> PUT
Update -> PATCH
Delete -> DELETE

## Tournaments [/v0.1/tournaments]

### List All Tournaments [GET]

+ Response 200 (application/json)

        {
            "errors": null,
            "data":
                [
                    {
                        "name": "test tournament",
                        "num_of_rounds": 3,
                        "id": 0,
                        "style": "PDA",
                        "url": "www.goodtournament.com",
                        "judge_criterion":[
                            {
                                "judge_test_percent":100,
                                "judge_repu_percent":0,
                                "judge_perf_percent":0
                            }
                        ]
                    }
                ]
            },
            "resource_url":"/v0.1/tournaments"
        }

## Specific Tournaments [/v0.1/{tournament_name}]

+ Parameters
    + tournament_name (required, string, `test`)

### Get Tournament [GET]

+ Response 200 (application/json)

        {
            "errors": null,
            "data":
            {
                "url": ""
                "id": 0,
                "name": "testtournament",
                "style": "PDA",
                "host": "terrible TD kym",
                "num_of_rounds": 3,
                "judge_criterion":
                [
                    {
                        "judge_test_percent":100,
                        "judge_repu_percent":0,
                        "judge_perf_percent":0
                    }
                ],
                "break_team_num": 0
            },
            "resource_url":""
        }

### Create Tournament [POST]

+ Request (application/json)

        {
            "args": {
              "force": false
            },
            "data":
            {
                "url": "",
                "name": "testtournament",
                "style": "PDA",
                "host": "Great TD",
                "judge_criterion":
                [
                    {
                        "judge_test_percent":100,
                        "judge_repu_percent":0,
                        "judge_perf_percent":0
                    }
                ],
                "break_team_num": 0
            }
        }

+ Response 200 (application/json)

        {
            "errors": null
            "data": same as above,
            "resource_url": "v0.1/testtournament"
        }

### Send Judge Criterion [PUT]

+ Request (application/json)

        {
            "judge_criterion":
            [
                {
                    "judge_test_percent":100,
                    "judge_repu_percent":0,
                    "judge_perf_percent":0
                }
            ]
        }

+ Response 200 (application/json)

        {
            "errors": null
            "data":
            {
                "judge_criterion":
                [
                    {
                        "judge_test_percent":100,
                        "judge_repu_percent":0,
                        "judge_perf_percent":0
                    }
                ]
            },
            "resource_url": "/v0.1/tournaments"
        }

## Available Styles [/v0.1/styles]

### List All Styles [GET]

+ Response 200 (application/json)

        {
            "errors": null,
            "data":
            [
                {
                    "style_name": "PDA",
                    "debater_num_per_team": 4,
                    "team_num": 2,
                    "score_weights": [1, 1, 1, 0.5],
                    "replies": [0, 1],(replier cnadidates) candidates. if 2nd speaker does reply, 1 */
                    "num_of_replies_per_team": 1
                }
            ],
            "resource_url": ""
        }

## Round [/v0.1/{tournament_name}/{round_num}]

### Get Round Information [GET]

+ Response 200 (application/json)

        {
            "errors":null
            "data":
            {
                "current_round": 1,
                "status": 0,
                "constants":
                [
                    {
                        "random_pairing":4,
                        "des_power_pairing":1,
                        "des_w_o_same_a_insti":2,
                        "des_w_o_same_b_insti":0,
                        "des_w_o_same_c_insti":0,
                        "des_with_fair_sides":1 /*property (int): preference(1 = most preferred)*/
                    }
                ],
                "constants_of_adj":
                [
                    {
                        "random_allocation":4,
                        "des_strong_strong":2,
                        "des_with_fair_sides":3,
                        "des_avoiding_conflicts":1,
                        "des_avoiding_past":0,
                        "des_priori_bubble":0,
                        "des_chair_rotation":0
                    }
                ]
            },
            "resource_url": ""
        }

### Send Round Config [PUT]

+ Request (application/json)

        {
            "constants": (defined above),
            "constants_of_adj": (defined above)
        }

+ Response 200 (application/json)

        {
            "errors": null,
            "data": same as above,
            "resource_url":""
        }

### Finish Current Round [POST]

+ Request (application/json)

        {
            "args": {"force": true},
            "data":
            {
                "current_round": 1
            }
        }

+ Response 200 (application/json)

        {
            "errors": [],
            "data":
            {
                "current_round": 1
            },
            "resource_url": ""
        ]

## All Suggested Team Allocations [/v0.1/{tournament_name}/{round_num}/suggested_team_allocations]

+ Parameters
    + tournament_name (required, string, `test`)
    + round_num (required, number, `1`)

### Get All Suggested Team Allocations [POST]

+ Request (application/json)

        {
            "args": {"force": false}
        }

+ Response 200 (application/json)

        {
            "errors": [],
            "data":
            [
                {
                    "algorithm": "",
                    "indices": {
                        "power_pairing_indicator": 1.0, /* 1 <-> inf. */
                        "adopt_indicator": , /* the higher the better */
                        "adopt_indicator2": , /* the higher the better */
                        "adopt_indicator_sd": 10, /* Standard Diviation */
                        "gini_index": 0.0, /* 0 <-> 1 */
                        "scatter_indicator": 0.0 /* the lower the better */
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
                }
            ],
            "resource_url": ""
        }


### Check Team Allocaiton [PATCH]

+ Request (application/json)

        [
            {
                "teams": [0, 1],
                "chairs": [],
                "panels": [],
                "venue": null,
                "trainees": []
            }
        ]

+ Response 200 (application/json)

### Send Team Allocation [POST] /* この上でも良い?(id不要) */

+ Request(application/json)

        [  
            {
                "teams": [0, 1],
                "chairs": [],
                "panels": [],
                "venue": null,
                "trainees": []
            }
        ]

+ Response 200 (application/json)

        {
            "errors": [],
            "data": null
        }

## All Suggested Adjudicator Allocations [/v0.1/{tournament_name}/{round_num}/suggested_adjdicator_allocations]

+ Parameters
    + tournament_name (required, string, `test`)
    + round_num (required, number, `1`)

### Get All Suggested Adudicator Allocations [GET]

+ Response 200 (application/json)

        {
            "errors": [],
            "data":
            [
                {
                    "algorithm": "",
                    "indices": {
                        "power_pairing_indicator": 1.0, /* 1 - inf. */
                        "adopt_indicator": , /*  */
                        "adopt_indicator2": , /*  */
                        "adopt_indicator_sd": 10, /* Standard Diviation */
                        "gini_index": 0.0, /* 0-1 */
                        "scatter_indicator": 0.0 /*  */
                    },
                    "large_warings": [""],
                    "allocation":
                    [
                        {
                            "warnings": [{}]
                            "teams": [0, 1]
                            "chairs": [0],
                            "panels": [1, 2],
                            "venue": null,
                            "trainees": []
                        }
                    ]
                }
            ],
            "resource_url": ""
        }

### Check Adjudicator Allocation [PUT]

    [
        {
            "teams": [0, 1],
            "chairs": [0],
            "panels": [1, 2],
            "venue": null,
            "trainees": []
        }
    ]

## Adjudicator Allocation [/v0.1/{tournament_name}/{round_num}/suggested_adjdicator_allocations/{allocation_id}]

+ Parameters
    + tournament_name (required, string, `test`)
    + round_num (required, number, `1`)


### Send Adjudicator Allocation [POST]

+ Request

        [
            {
                "teams": [0, 1]
                "chairs": [0],
                "panels": [1, 2],
                "venue": null,
                "trainees": []
            }
        ]

+ Response 200 (application/json)

## Venue Allocation [/v0.1/{tournament_name}/{round_num}/suggested_venue_allocation]

+ Parameters
    + tournament_name (required, string, `test`)
    + round_num (required, number, `1`)

### Get Venue Allocation [GET]

+ Response 200 (application/json)

        {
            "errors": [],
            "data":
            [
                {
                    "teams": [0, 1]
                    "chairs": [0],
                    "panels": [1, 2],
                    "trainees": [],
                    "venue": 3 /* venue id */
                }
            ],
            "resource_url": ""
        }

### Check Venue Allocation [PUT]

### Send Venue Allocation [POST]

+ Request (application/json)

+ Response 200 (application/json)

## Adjudicators [/v0.1/{tournament_name}/adjudicators]

### List All Adjudicators [GET]

+ Response 200 (application/json)

        {
        }

## Specific Adjudicator [/v0.1/{tournament_name}/adjudicators/{adjudicator_id}]

### Get Specific Adjudicator [GET]

+ Response 200 (application/json)

        {
            "errors":
            "data":
            {
                "id": 3
                "name": "a1",
                "reputation": 6,
                "judge_test": 10,
                "institutions": [0],
                "conflicts": [],
                "url": "",
                "available": true
            },
            "resource_url": ""
        }

### Create Adjudicator [POST]

+ Request (application/json)

        {
            "name": "a1",
            "reputation": 6,
            "judge_test": 10,
            "institutions": [0],
            "conflicts": [],
            "url": "",
            "available": true
        }

+ Response 200 (application/json)

        {
            "errors": null,
            "data":
            {
                "code": 0,
                "name": "a1",
                "reputation": 6,
                "judge_test": 10,
                "institutions": [0],
                "conflicts": [],
                "url": "",
                "available": true
            }
        }


## Speakers [/v0.1/{tournament_name}/speakers]

### List All Speakers [GET]

+ Response 200 (application/json)

        {
        }

## Specific Speaker [/v0.1/{tournament_name}/speakers/{speaker_id}]

### Get Specific Speaker [GET]

+ Response 200 (application/json)

        {
            "errors":
            "data":
            {
                "id": 1,
                "name": "kym",
                "team": 0,
                "url": ""
            },
            "resource_url": ""
        }

### Create Speaker [POST]

+ Request (application/json)

        {
        }

+ Response 200 (application/json)

        {
        }

## Teams [/v0.1/{tournament_name}/teams]

### List All Teams [GET]

+ Response 200 (application/json)

        {
        }

## Specific Team [/v0.1/{tournament_name}/teams/{team_id}]

### Get Team [GET]

+ Response 200 (application/json)

        {
            "errors": null,
            "data":
            {
                "id": id,
                "name": team_name,
                "speakers": [speaker],
                "available": team_available,
                "url": team_url
            },
            "resource_url": ""
        }

### Create Team [POST]

+ Request (application/json)

        {
        }

+ Response 200 (text/plain)

        "Thank you, "

### Create/Update-if-exist Team [PUT]

+ Request (application/json)

        {
        }

+ Response 200 (text/plain)

        "Thank you, "

### Update Team [PATCH]

+ Request (application/json)

        {
        }

+ Response 200 (application/json)

        {
        }

### Delete Team [DELETE]

+ Request (application/json)

        {
        }

+ Response 200 (application/json)

        {
        }

## Venues [/v0.1/{tournament_name}/venues]

### List All Venues [GET]

+ Response 200 (application/json)

## Specific Venue [/v0.1/{tournament_name}/venues/{venue_id}]

### Get Venue [GET]

+ Response 200 (application/json)

        {
            "errors": null,
            "data":
            {
                "id": 3,
                "name": '383',
                "available": true,
                "priority": 1,
                "url": "www.google.com"
            },
            "resource_url": ""
        }

### Create Venue [POST]

+ Request (application/json)

        {
        }

+ Response 200 (application/json)

        {
        }

## Institutions [/v0.1/{tournament_name}/institutions]

### List All Institutions [GET]

+ Response 200 (application/json)

        {
        }

## Specific Institution [/v0.1/{tournament_name}/institutions/{institution_id}]

### Get Institution [GET]

+ Response 200 (application/json)

        {
            "errors": null,
            "data":
            {
                "id": institution_id,
                "name": institution_name,
                "url": institution_url,
                "scale": 'a',
            },
            "resource_url": ""
        }

### Create Institution [POST]

+ Request (application/json)

        {
        }

+ Response 200 (application/json)

        {
        }


## Team Results [/v0.1/{tournament_name}/{round_num}/results/teams]

### List Team Results [GET]

+ Response 200 (application/json)

        {
            "errors": null,
            [
                {
                    "team": 3,
                    "team_name": "KYM1",
                    "win": 1 /* when in BP win must be points(0, 1, 2, 3), when in NA win points be (0, 1:win)*/
                }
            ]
        }

## Speaker Results [/v0.1/{tournament_name}/{round_num}/results/speakers]

### List Speaker Results [GET]

+ Response 200 (application/json)

### Send Speaker Result [PUT]

+ Request (application/json)

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

+ Response 200 (application/json)

        {
            "errors": null,
            "data": (same as above),
            "resource_url": ""
        }

## Adjudicator Results [/v0.1/{tournament_name}/{round_num}/results/adjudicators]

### List Adjudicator Results [GET]

+ Response 200 (application/json)

        {
            "errors": null,
            "data": undef
        }

### Send Adjudicator Result [PUT]

+ Request (application/json)

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

+ Response 200 (application/json)

        {
            "errors": null,
            "data" : null
        }

## Total Team Results [/v0.1/{tournament_name}/results/teams]

preparing

### Download Team Results [GET]

<!-- Modify Results [POST] : not supported by current api version -->

+ Response 200 (application/json)

        {
            "errors": null,
            "data": undef,
            "resource_url": ""
        }

## Total Adjudicator Results [/v0.1/{tournament_name}/results/adjudicators]

preparing

## Total Speaker Results[/v0.1/{tournament_name}/results/speakers]

## Backups [/v0.1/{tournament_name}/backups]

### List All Available Backups [GET]

+ Response 200 (application/json)

        {
            "errors":null,
            "data":
            [
                {
                    "date": "2016/01/04-23:59:10",
                    "comment": "test",
                    "backup_code": "fda23fds",
                    "current_round": 1 /* in which the backup is made */
                }
            ],
            "resource_url": ""
        }

### Back to Particular Point [PUT]

+ Request (application/json)

        {
            "errors": null,
            "data":
            {
                "backup_code": "fda23fds"
            }
        }

+ Response 200 (application/json)

        {
            "errors": null,
            "data": null,
            "resource_url": ""
        }
