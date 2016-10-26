# All Suggested Team Allocations 

[/v1.0/{tournament_name}/{round_num}/suggested_team_allocations]

### Get All Suggested Team Allocations [POST]

+ Request (application/json)
```
{
    "args": {"force": false}
}
```
+ Response 200 (application/json)
```
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
```

### Check Team Allocaiton [PATCH]

+ Request (application/json)
```
[
    {
        "teams": [0, 1],
        "chairs": [],
        "panels": [],
        "venue": null,
        "trainees": []
    }
]
```
+ Response 200 (application/json)

{
    "errors": null,
    "data":
    [
        {
            "teams": [0, 1],
            "chairs": [],
            "panels": [],
            "venue": null,
            "trainees": []
        }
    ],
    "resource_url": ""
}

### Confirm Team Allocation [POST]

+ Request(application/json)
```
[  
    {
        "teams": [0, 1],
        "chairs": [],
        "panels": [],
        "venue": null,
        "trainees": []
    }
]
```
+ Response 200 (application/json)
```
{
    "errors": [],
    "data": null,
    "resource_url": ""
}
```