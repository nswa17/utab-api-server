# Specific Adjudicator 

[/v1.0/{tournament_name}/adjudicators/{adjudicator_id}]

### Get Specific Adjudicator [GET]

+ Response 200 (application/json)
```
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
```
### Create Adjudicator [POST]

+ Request (application/json)
```
{
    "name": "a1",
    "reputation": 6,
    "judge_test": 10,
    "institutions": [0],
    "conflicts": [],
    "url": "",
    "available": true
}
```
+ Response 200 (application/json)
```
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
    },
    "resource_url": ""
}
```