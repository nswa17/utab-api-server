# Backups

[/v1.0/{tournament_name}/backups]

### List All Available Backups [GET]

+ Response 200 (application/json)
```
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
```
### Back to Particular Point [PUT]

+ Request (application/json)
```
{
    "errors": null,
    "data":
    {
        "backup_code": "fda23fds"
    }
}
```
+ Response 200 (application/json)
```
{
    "errors": null,
    "data": null,
    "resource_url": ""
}
```