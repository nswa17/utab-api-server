# Venue Allocation 

[/v1.0/{tournament_name}/{round_num}/suggested_venue_allocation]

### Get Venue Allocation [GET]

+ Response 200 (application/json)
```
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
```
### Check Venue Allocation [PUT]

+ Request (application/json)
```
{
    [
        {
            "teams": [0, 1]
            "chairs": [0],
            "panels": [1, 2],
            "venue": 33,
            "trainees": []
        }
    ]
}
```
+ Response 200 (application/json)
```
{
    "errors": null,
    "data": [
        {
            "teams": [0, 1]
            "chairs": [0],
            "panels": [1, 2],
            "venue": 33, /* venue id */
            "trainees": []
        }
    ]
}

### Confirm Venue Allocation [POST]

+ Request (application/json)
```
{
    [
        {
            "teams": [0, 1]
            "chairs": [0],
            "panels": [1, 2],
            "venue": 33,
            "trainees": []
        }
    ]
}
```
+ Response 200 (application/json)
```
{
    "errors": null,
    "data": [
        {
            "teams": [0, 1]
            "chairs": [0],
            "panels": [1, 2],
            "venue": 33, /* venue id */
            "trainees": []
        }
    ]
}
```