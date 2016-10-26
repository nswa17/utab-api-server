# Total Team Results 

[/v1.0/{tournament_name}/results/teams]

### Download Total Team Results [GET]

+ Response 200 (application/json)
```
{
	'errors': [],
	'data':
	{
		3:
		{
			'id': 3,
			'name': 'Team3',
			'ranking': 1,
			'wins': 1,
			'sum': 189.5,
			'margin': 5.0,
			'sd': 0.0,
			'average': 189.5,
			'round1': 189.5
		}
	},
	'resource_url': '/v1.0/testtournament/results/teams'
}
```