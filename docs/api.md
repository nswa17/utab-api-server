
# utab

**utab** is a online tab software for all debates.
This document describes Web API interface for utab.

## API Version

This document is for **utab API Version 1.0.0**

## Base URL

URL must start with `<protocol>://<host>/<version>` like:

		http://api.utab.com/v1

Note: currently, no one implements and publicates this api.

# Errors

## Error Handling Policy

There are two types of errors in Web-based API.
One is "System Error" and the other is "Application Error".
These errors must be shown to end-users with maximum information for technical supports.

See "utab-api-errors.md" for more details on errors.

## System Errors

System Errors are errors which are thrown from infrastructure level.
For example:

* Internet connection errors
* URI errors (Resource Not Found, Resource Temporary Moved, ...etc.)
* Bugs in source code (Internal Server Error)
* Required fields are not fullfilled (Bad Request)

These errors must be use HTTP Status Code.

 + `400 Bad Request`
 + `401 Unauthorized`
 + `403 Forbidden`
 + `404 Not Found`
 + `500 Internal Server Error`
 + `501 Not Implemented`
 + `503 Service Unavailable`

## Application Errors

Application Errors are errors which occur in application level.
For Example:

* Same team appears in one draw
* Number of teams is not enough

These errors can also use HTTP Status Code, however, use Response Body containing `Error Object` as following definition.

		{
			"errors": [
				/* Error Object */
				{
					"statusCode": 0,	/* the error type code which is unique to each errors <Integer, required> */
					"statusText": "Unknown Error",	/* one-line description of the error type <String, required> */
					"message": "We are sorry, but unknown error occurs. Please contact technical support team.",	/* Supporting message usually shown to end-users <String, optional> */
					"from": "unknown point"	/* where the error occurs <String, optional> */
				}
			],
			"data" : /* Any kind of objects */
		}

When no error occurs, `errors` should be `null`.
Thus, usually, when `GET` Request is successfully finished, Response will be following with Status Code `200 OK`:

		{
			"errors": null,
			"data": /* Any kind of objects */
		}

When both `errors` and `data` are `null`, then use Status Code `204 No Content` and Response Body should be nothing.

# Type definitions

In this document, following type definitions will be used.

		<Type Name, Attributes>

`Type Name` is a type name of the value.
`Attributes` are comma-separated list of attributes selected from followings:

* `required`
* `optional`
* `auto` - the field will be mutable and automatically added by server
* `id(obj)` - the field is id of obj

`auto` fields can be omitted in GET Requests.

`id(obj)` fields will be used in Request and related `obj` will be returned in Response.
For example:

		{
				"venue_id": "Sample%20Venue%201"	/* <URI String, id(Venue Object)> */
		}

This Request will replace `id(obj)` field by `obj` and return following Response:

		{
				"venue": <Venue Object>
		}

Note that these type definitions doesn't show how to implement these data as internal object.
You can/should implement Speaker Object and Adjudicator Object to inherit the same base-class, named `Person` for example.

### URI String

String which can be used safe in URI.

* Use `urllib.parse.quote()` in Python 3
* Use `encodeURIComponent()` in JavaScript

### ID String

String which represents an ID.

		[A-Z][a-z][0-9][_]

### Date String

String which represents a Date in UTC.
See alse: ISO 8601

# Filtering Fields by Query

For example, when the client want to get `name` of a tournament, the Request will be:

		GET /tournaments/0

Then, the Response will be:

		200 OK (application/json)
		{
			"errors": null,
			"data": {
				"id": "The%201st%20Sample%20Tournament",
				"name": "The 1st Sample Tournament",
				"url": "/The%201st%20Sample%20Tournament",
				"style": 0,
				"host_id": "Sample Debate Association",
				"user_id": "mr_sample",
				"pre_rounds": 4,
				"break_rounds": 4
			}
		}

However, this is inefficient when you need only the `name` and `url` fields.
In this case, use `fields` query instead of getting all the data by changing the Request to:

		GET /tournaments/0?fields=name,url

Then, the Request will be:

		200 OK (application/json)
		{
			"errors": null,
			"data": {
				"name": "The 1st Sample Tournament",
				"url": "/The%201st%20Sample%20Tournament"
			}
		}

`fields` query should be following format:

		fields={field_name}[,{field_name},...]

# Common Method implementations

Definitions of common implementations of methods.
In each Data sections, implementations of each methods will be omitted and there are only descriptions which methods should be implemented in the object. 

Following example means Tournament Object should implements `DELETE` method.

		Delete /tournaments/{Tournament.id}

This is the same as:

		Request
		
				DELETE /tournaments/{Tournament.id} (text/plain)
		
		Response
		
				204 No Content (text/plain)

## List /items

List all items.

### Request

		GET /items (application/json)

### Response

		200 OK (application/json)
		{
			"errors": null,
			"data": [
				<Object>, ...
			]
		}

## Create /items

Create a new item.

### Request

		POST /items (application/json)
		<Object>

### Response

		201 Created (application/json)
		Location: /items/id
		{
			"errors": null,
			"data": <Object>
		}

## Get /items/id

Get an item

### Request

		GET /items/id (application/json)

### Response

		200 OK (application/json)
		{
			"errors": null,
			"data": <Object>
		}

## Update /items/id

Update an item.

### Request

		POST /items/id (application/json)
		<Object>	/* only partial fields can be admitted */

### Response

		201 Created (application/json)
		{
			"errors": null,
			"data": <Object>
		}

## Delete /items/id

Delete an item.

### Request

		DELETE /items/id (text/plain)

### Response

		204 No Content (text/plain)


# Tournaments Data

## Tournament Object

		{
			"id": "The%201st%20Sample%20Tournament", /* <URI string, auto> */
			"name": "The 1st Sample Tournament", /* <String, required> */
			"url": "/The%201st%20Sample%20Tournament",	/* relative URI for this tournament object <URI String, auto> */
			"style": 0, /* UID for debate style <Integer, required> */
			"host": "Sample Debate Association", /* name of tournament host <String, required> */
			"user_id": "mr_sample",	/* User ID of user who create this data <ID String, required> */
			"date": "20160416T163025",	/* UTC of time when this data is created <Date String, auto> */
			"current_round_id": "Round%201"	/* <URI String, optional, auto> */
		}

## Methods

+ List /tournaments
+ Create /tournaments
+ Get /tournaments/{Tournament.id} and /{Tournament.id}
+ Update /tournaments/{Tournament.id} and /{Tournament.id}
+ Delete /tournaments/{Tournament.id} and /{Tournament.id}

# Venues Data

## Venue Object

		{
			"id": "Sample%20Venue%201",	/* <URI String, auto> */
			"tournament": <Tournament Object>,	/* <Tournament Object, auto> */
			"name": "Sample Venue 1",	/* <String, required> */
			"url": "/The%201st%20Sample%20Tournament/venues/Sample%20Venue%201"	/* <URI String, auto> */
		}

## Methods

+ List /{Tournament.id}/venues
+ Create /{Tournament.id}/venues
+ Get /{Tournament.id}/venues/{Venue.id}
+ Update /{Tournament.id}/venues/{Venue.id}
+ Delete /{Tournament.id}/venues/{Venue.id}

# Institutions Data

## Institution Object

		{
			"id": "Sample%20Institution%201",	/* <URI string, auto> */
			"tournament": <Tournament Object>,	/* <Tournament Object, auto> */
			"name": "Sample Institution 1",	/* <String, required> */
			"url": "/The%201st%20Sample%20Tournament/institutions/Sample%20Institution%201",	/* <URI String, auto> */
		}

## Methods

+ List /{Tournament.id}/institutions
+ Create /{Tournament.id}/institutions
+ Get /{Tournament.id}/institutions/{Institution.id}
+ Update /{Tournament.id}/institutions/{Institution.id}
+ Delete /{Tournament.id}/institutions/{Institution.id}

# Speakers Data

## Speaker Object

		{
			"id": "Sample%20Speaker%201",	/* <URI string, auto> */
			"tournament": <Tournament Object>,	/* <Tournament Object, auto> */
			"name": "Sample Speaker 1",	/* <String, required> */
			"url": "/The%201st%20Sample%20Tournament/speakers/Sample%20Speaker%201",	/* <URI String, auto> */
			"institutions": [
				<Institution Object>, ...
			],	/* <Institution Object list, required> */
		}

## Methods

+ List /{Tournament.id}/speakers
+ Create /{Tournament.id}/speakers
+ Get /{Tournament.id}/speakers/{Speaker.id}
+ Update /{Tournament.id}/speakers/{Speaker.id}
+ Delete /{Tournament.id}/speakers/{Speaker.id}

# Teams Data

## Team Object

		{
			"id": "Sample%20Team%201",	/* <URI string, auto> */
			"tournament": <Tournament Object>,	/* <Tournament Object, auto> */
			"name": "Sample Speaker 1",	/* <String, required> */
			"url": "/The%201st%20Sample%20Tournament/teams/Sample%20Team%201",	/* <URI String, auto> */
			"speakers": [
				<Speaker Object>, ...
			],	/* <Speaker Object list, required> */
		}

## Methods

+ List /{Tournament.id}/teams
+ Create /{Tournament.id}/teams
+ Get /{Tournament.id}/teams/{Speaker.id}
+ Update /{Tournament.id}/teams/{Speaker.id}
+ Delete /{Tournament.id}/teams/{Speaker.id}

# Adjudicators Data

## Adjudicator Object

		{
			"id": "Sample%20Adjudicator%201",	/* <URI string, auto> */
			"tournament": <Tournament Object>,	/* <Tournament Object, auto> */
			"name": "Sample Adjudicator 1",	/* <String, required> */
			"url": "/The%201st%20Sample%20Tournament/adjudicators/Sample%20Adjudicator%201",	/* <URI String, auto> */
			"institutions": [
				<Institution Object>, ...
			],	/* <Institution Object list, required> */
			"conflict_teams": [
				<Team Object>, ...
			]	/* <Team Object list, optional> */
		}

## Methods

+ List /{Tournament.id}/adjudicators
+ Create /{Tournament.id}/adjudicators
+ Get /{Tournament.id}/adjudicators/{Adjudicator.id}
+ Update /{Tournament.id}/adjudicators/{Adjudicator.id}
+ Delete /{Tournament.id}/adjudicators/{Adjudicator.id}

# Rounds Data

## Round Object

		{
			"id": "Round%201",	/* <URI string, auto> */
			"tournament": <Tournament Object>,	/* <Tournament Object, auto> */
			"name": "Round 1",	/* <String, required> */
			"url": "/The%201st%20Sample%20Tournament/Round%201",	/* <URI String, auto> */
			"previous_id": null,	/* ID of previous round <URI String, optional> */
			"next_id": "Round%202",	/* ID for next round <URI String, optional> */
			"type": 0,	/* UID for round type (preliminary, break, ...) <Integer, required> */
			"method": 0,	/* UID for draw method (how to generate draw) <Integer, required> */
			"available_venues": [
				<Available Venue Object>, ...
			]
		}

## Methods

+ List /{Tournament.id}/rounds
+ Create /{Tournament.id}/rounds
+ Get /{Tournament.id}/rounds/{Round.id} and /{Tournament.id}/{Round.id}
+ Update /{Tournament.id}/rounds/{Round.id} and /{Tournament.id}/{Round.id}
+ Delete /{Tournament.id}/rounds/{Round.id} and /{Tournament.id}/{Round.id}

# Available Venue Data

## Available Venue Object

		{
			"venue_id": "Sample%20Venue%201",	/* <URI String, id(Venue Object)> */
			"available": true	/* <Boolean, required> */
		}

## Methods

+ List /{Tournament.id}/rounds/{Round.id}/available_venues
+ Create /{Tournament.id}/rounds/{Round.id}/available_venues
+ Delete /{Tournament.id}/rounds/{Round.id}/available_venues/{Venue.id} and /{Tournament.id}/{Round.id}/available_venues/{Venue.id}

# Available Team Data

## Available Team Object

		{
			"team_id": "Sample%20Team%201",	/* <URI String, id(Team Object)> */
			"available": true	/* <Boolean, required> */
		}

## Methods

+ List /{Tournament.id}/rounds/{Round.id}/available_teams
+ Create /{Tournament.id}/rounds/{Round.id}/available_teams
+ Delete /{Tournament.id}/rounds/{Round.id}/available_teams/{Team.id} and /{Tournament.id}/{Round.id}/available_teams/{Team.id}

# Available Adjudicator Data

## Available Adjudicator Object

		{
			"adjudicator_id": "Sample%20Adjudicator%201",	/* <URI String, id(Adjudicator Object)> */
			"available": true	/* <Boolean, required> */
		}

## Methods

+ List /{Tournament.id}/rounds/{Round.id}/available_adjudicators
+ Create /{Tournament.id}/rounds/{Round.id}/available_adjudicators
+ Delete /{Tournament.id}/rounds/{Round.id}/available_adjudicators/{Adjudicator.id} and /{Tournament.id}/{Round.id}/available_adjudicators/{Adjudicator.id}






