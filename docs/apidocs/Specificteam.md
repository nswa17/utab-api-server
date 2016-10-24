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
}
```
+ Response 200 (text/plain)
```
"Thank you, "
```
### Create/Update-if-exist Team [PUT]

+ Request (application/json)
```
{
}
```
+ Response 200 (text/plain)
```
"Thank you, "
```
### Update Team [PATCH]

+ Request (application/json)
```
{
}
```
+ Response 200 (application/json)
```
{
}
```
### Delete Team [DELETE]

+ Request (application/json)
```
{
}
```
+ Response 200 (application/json)
```
{
}
```