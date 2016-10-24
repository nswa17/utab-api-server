# All Suggested Adjudicator Allocations 

[/v1.0/{tournament_name}/{round_num}/suggested_adjdicator_allocations]

### Get All Suggested Adudicator Allocations [GET]

+ Response 200 (application/json)
```
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
```
### Check Adjudicator Allocation [PUT]
```
[
{
    "teams": [0, 1],
    "chairs": [0],
    "panels": [1, 2],
    "venue": null,
    "trainees": []
}
]
```
### Send Adjudicator Allocation [POST]

+ Request
```
[
    {
        "teams": [0, 1]
        "chairs": [0],
        "panels": [1, 2],
        "venue": null,
        "trainees": []
    }
]
```
+ Response 200 (application/json)
```
{
}
```