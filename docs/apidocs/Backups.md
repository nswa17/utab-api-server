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
            "date": "20160104235910",
            "comment": "test",
            "name": "testtournament",
            "current_round": 1 /* in which the backup is made */
        }
    ],
    "resource_url": ""
}
```

### Save Current Tournament [POST]

+ Request (application/json)

```
{
    "comment": "testbackup"
}
```

+ Response (application/json)

```
{
    "errors": null,
    "data":
    {
        "date": "20160104235910",
        "comment": "test",
        "name": "testtournament",
        "current_round": 1 /* in which the backup is made */
    },
    "resource_url": ""
}
```

### Back to Particular Point [PUT]

It's possible to import a different tournament backup

+ Request (application/json)
```
{
    "errors": null,
    "data":
    {
        "name": "testtournament",
        "date": 20101001202203
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