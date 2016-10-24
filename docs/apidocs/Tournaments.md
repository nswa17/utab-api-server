# Tournaments 

[/v1.0/tournaments]

### List All Tournaments [GET]

+ Response 200 (application/json)

```
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
    "resource_url":"/v1.0/tournaments"
}
```