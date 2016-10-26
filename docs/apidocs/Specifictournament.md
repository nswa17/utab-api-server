# Specific Tournament 

[/v1.0/{tournament_name}]

### Get Tournament [GET]

+ Response 200 (application/json)
```
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
```
### Create Tournament [POST]

+ Request (application/json)
```
{
    "url": "",
    "name": "testtournament",
    "style": "PDA",
    "host": "Great TD",
    "num_of_rounds": 4,
    "judge_criterion":
    [
        {
            "judge_test_percent":100,
            "judge_repu_percent":0,
            "judge_perf_percent":0
        }
    ]
    "break_team_num": 0
}
```
+ Response 200 (application/json)
```
{
    "errors": null
    "data": {
        "id": 0,
        "name": "testtournament",
        "num_of_rounds": 4,
        "style": "PDA,
        "host": "Great TD",
        "url": "",
        "judge_criterion":
        [
            {
                "judge_test_percent":100,
                "judge_repu_percent":0,
                "judge_perf_percent":0
            }
        ],
        "break_team_num": 10
    },
    "resource_url": "v1.0/testtournament"
}
```
### Send Judge Criterion [PUT]

+ Request (application/json)
```
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
```
+ Response 200 (application/json)
```
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
    "resource_url": "/v1.0/tournaments"
}
```