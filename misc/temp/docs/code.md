
# Error Code and Status Code in utab API

## Status

### Round status code
* 0 : before starting round(you can add adjudicators, etc...)
* 1 : computing matchups
* 2 : finished computing matchups
* 3: computing allocations
* 5: computing panel allocation
* 6: finished computing panel allocation
* 7: computing venue allocation
* 8: finished computing venue allocation
* 9: collecting results
* 10: team results processing
* 12: team results processed, adj results processing
* 13: adj results processed
* 14: results processed, prepared to proceed to next round

## Errors

### System Errors

Infrastructure-level errors should be represented by HTTP Status Code.

### Application Errors

Application-level errors should return Error Object in error property of response.

```
{
    "errors": [
        {
            "status_code": 0,
            "status_text": "Tournament Not Found",
            "message": "No such tournament name: 'test tournament'",
        }
    ],
    "data": null
}
```

### Error List

##### [0] Tournament Not Found
<!-- 0 = status code -->

```
{
    "status_code": 0,
    "status_text": "Tournament Not Found",
    "message": "No such tournament name: 'test tournament'",
}
```
