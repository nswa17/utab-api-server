# Specific Institution 

[/v1.0/{tournament_name}/institutions/{institution_id}]

### Get Institution [GET]

+ Response 200 (application/json)
```
{
    "errors": null,
    "data":
    {
        "id": 2,
        "name": "KYM",
        "url": "",
        "scale": 'a',
    },
    "resource_url": ""
}
```
### Create Institution [POST]

+ Request (application/json)
```
{
    "name": "KKM",
    "url": "",
    "scale": 'a',
}
```
+ Response 200 (application/json)
```
{
	"errors": null,
	"data":
	{
        "id": 4,
	    "name": "KKM",
	    "url": "",
	    "scale": 'a',
	}
}
```