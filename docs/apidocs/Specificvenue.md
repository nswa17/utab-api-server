# Specific Venue 

[/v1.0/{tournament_name}/venues/{venue_id}]

### Get Venue [GET]

+ Response 200 (application/json)
```
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
```
### Create Venue [POST]

+ Request (application/json)
```
{
    "name": '383',
    "available": true,
    "priority": 1,
    "url": "www.google.com"
}
```
+ Response 200 (application/json)
```
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
```