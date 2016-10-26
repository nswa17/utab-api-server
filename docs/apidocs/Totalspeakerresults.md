# Total Speaker Results

[/v1.0/{tournament_name}/results/speakers]

### Download Total Speaker Results [GET]

+ Response 200 (application/json)

```
{
	'errors': [],
	'data':
	{
		speaker_id:
		{
			'id': 4,
			'name':'Debater4',
			'team': 'Team2',
			'ranking': 4,
			'sum': 74.33,
			'average': 74.33,
			'sd': 0,
			'average1': 74.33,
			'round1-1': 0.0,
			'round1-2': 74.0,
			'round1-3': 37.5
		}
	},
	'resource_url': "/v1.0/{tournament_name}/results/speakers"
}
```