# flask-api-monitoring
Flask application for monitoring a service's usage using "Tags". 
The idea is to schedule a ping to this application's endpoints internally whenever a part of the service is used.

This is a barebones implementation, and I suggest you implement some form of authentication for security.

## Usage Example

Someone visits example.com/page1 --> example.com delivers the content as normal, but it also schedules/sends a ping to `/update?tag=page1`

Then, the usage statistics for `tag=page1` will update, and total usage stats/a usage history is available at `/get?tag=page1` or `/history?tag=page1` for the "page1" tag.

# Installation

First, clone this repository and edit `docker-compose.yml` to fit your needs. With Docker installed, you'll just need to run `docker compose up` in the directory with flask-api-monitoring's files.


## /create Endpoint

Usage: `/create?tag=TagName`

Possible Responses:
```
Scenario: TagName already exists in the database.
  Text: "Tag already exists!"
  Code: 409
```
```
Scenario: ?tag= isn't set
  Text: "Invalid Data"
  Code: 412
```
```
Scenario: Success
  Text: "Tag Created Successfully"
  Code: 200
```

## /update Endpoint

Usage: `/update?tag=TagName`

Possible Responses:
```
Scenario: TagName doesn't exist in the database.
  Text: "Tag does not exist!"
  Code: 404
```
```
Scenario: ?tag= isn't set
  Text: "Invalid Data"
  Code: 412
```
```
Scenario: Success
  Action: Adds +1 to TagName's Use Count
  Text: <TagName's Use Count>
  Code: 200
```
## /get Endpoint

Usage: `/get?tag=TagName`

Possible Responses:
```
Scenario: TagName doesn't exist in the database.
  Text: "Tag does not exist!"
  Code: 404
```
```
Scenario: ?tag= isn't set
  Text: "Invalid Data"
  Code: 412
```
```
Scenario: Success
  Action: TagName's Use Count is unchanged
  Text: <TagName's Use Count>
  Code: 200
```
## /history Endpoint

Usage: `/history?tag=TagName`

Possible Responses:
```
Scenario: Tag doesn't exist, or is inactive
  Text: "No Data Found!"
  Code: 404
```
```
Scenario: ?tag= isn't set
  Text: "Invalid Data"
  Code: 412
```
```
Scenario: Success
  Text: <JSON Dictionary>
  Example: {"1": {"date": "datetime"}, "2": {"date": "datetime"}}
  Code: 200
```


