# Specific Team 

[/v1.0/{tournament_name}/teams/{team_id}]

### Get Team [GET]

+ Response 200 (application/json)
```
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
```
### Create Team [POST]

+ Request (application/json)
```
{
    "name": team_name,
    "speakers": [speaker],
    "available": team_available,
    "url": team_url
}
```
+ Response 200 (text/plain)

```
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
```