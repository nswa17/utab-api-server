# Teams 

[/v1.0/{tournament_name}/teams]

### List All Teams [GET]

+ Response 200 (application/json)

```
{
	"errors": null,
	"data":
	[
	    {
	        "id": id,
	        "name": team_name,
	        "speakers": [speaker],
	        "available": team_available,
	        "url": team_url
    	}
    ],
    'resource_url': ''
}
```