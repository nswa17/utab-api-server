# Utab

**Utab** is a online tab software for all debates.
This document describes Web API interface for utab.

## API Version

This document is for **utab API Version 1**

## Base URL

URL must start with `<protocol>://<host>/<version>` like:

		http://api.utab.com/v0.1

Note: currently, no one implements and publicates this api.

# Errors

## Error Handling Policy

There are two types of errors in Web-based API.
One is "System Error" and the other is "Application Error".
These errors must be shown to end-users with maximum information for technical supports.

See "errors.md" for more details on errors.

## System Errors

System Errors are errors which are thrown from infrastructure level.
For example:

* Internet connection errors
* URI errors (Resource Not Found, Resource Temporary Moved, ...etc.)
* Bugs in source code (Internal Server Error)
* Required fields are not fullfilled (Bad Request)

These errors must use HTTP Status Codes.

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

```json
		{
			"errors": [
				<-- Error Object -->
				{
					"statusCode": 0,	/* the error type code which is unique to each errors <Integer, required> */
					"statusText": "Unknown Error",	/* one-line description of the error type <String, required> */
					"message": "We are sorry, but unknown error occurs. Please contact technical support team.",	/* Supporting message usually shown to end-users <String, optional> */
					"from": "unknown point"	/* where the error occurs <String, optional> */
				}
			],
			"data" : /* Any kind of objects */
		}
```

When no error occurs, `errors` should be `[]`.
Thus, usually, when `GET` Request is successfully finished, Response will be following with Status Code `200 OK`:

```json
		{
			"errors": [],
			"data": /* Any kind of objects */
		}
```

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

```json
		{
				"venue_id": "Sample%20Venue%201"	/* <URI String, id(Venue Object)> */
		}
```

This Request will replace `id(obj)` field by `obj` and return following Response:

```json
		{
				"venue": <Venue Object>
		}
```

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

```
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
```

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
