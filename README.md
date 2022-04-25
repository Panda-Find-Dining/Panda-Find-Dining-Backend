# Find Dining Backend Application    

This will store our endpoints and instructions



## Base URL


```shell
https://find-dining-panda.herokuapp.com/
```


## API Endpoints
    

|  Method  |  Endpoint  |  Description |  Deployed  |
| -------- | ---------- | ------------ | ---------- |
|POST|[/auth/users/](#register-a-new-user)|register a new user|Yes|
|POST|[/auth/token/login/](#log-in)|login with existing user|Yes|
|POST|[/auth/token/logout/](#log-out)|logout with existing user|Yes|
|GET|[/meals/](#list-all-meals)|List all meals|Yes|
|GET|[/meals/{id}](#retrieve-a-specific-meal)|Retrieve a specific meal|Yes|
|POST|[/meals/](#create-a-new-meal)|Add a new meal|Yes|
|PUT|[/meals/{id}](#update-an-existing-meal)|Update an existing meal|Yes|
|PATCH|[/meals/{id}](#update-an-existing-meal)|Update part of an existing meal|Yes|
|DELETE|[/meals/{id}](#delete-meal)|Delete an existing meal|Yes|






<!-------------------------- Delete an Existing Meal  ------------------------------>

## Delete an existing meal


[Back to Endpoints](#api-endpoints)


### request


User must be logged in and authenticated with Token in header
Required fields: id(of meal)


```txt
DELETE / api / meals / {id} 
```

### response

```json

HTTP 204 No Content
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```



<!-------------------------- Update part of an Existing Meal  ------------------------------>

## Update an existing meal

[Back to Endpoints](#api-endpoints)

### request

User must be logged in and authenticated with Token in header
Required fields: id

```txt
PATCH / api / meals / {id} 
```

```json
{
    "id": 5,
    "creator": 1,
    "created_date": "2022-04-25T09:51:24.026446-05:00",
    "invitee": [],
    "location": "North Myrtle Beach, SC",
    "radius": 30,
    "lat": null,
    "lon": null
}
```

### response

```json
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 5,
    "creator": 1,
    "created_date": "2022-04-25T09:51:24.026446-05:00",
    "invitee": [],
    "location": "North Myrtle Beach, SC",
    "radius": 30,
    "lat": null,
    "lon": null
}
```




<!-------------------------- Update Existing Meal  ------------------------------>

## Update an existing meal

[Back to Endpoints](#api-endpoints)

### request

User must be logged in and authenticated with Token in header
Required fields: id

```txt
PUT / api / meals / {id} 
```

```json
{
    "id": 5,
    "creator": 1,
    "created_date": "2022-04-25T09:51:24.026446-05:00",
    "invitee": [],
    "location": "North Myrtle Beach",
    "radius": 30,
    "lat": null,
    "lon": null
}
```

### response

```json
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 5,
    "creator": 1,
    "created_date": "2022-04-25T09:51:24.026446-05:00",
    "invitee": [],
    "location": "North Myrtle Beach",
    "radius": 30,
    "lat": null,
    "lon": null
}
```





<!-------------------------- Get Meal Details  ------------------------------>

## Retrieve a specific meal

[Back to Endpoints](#api-endpoints)

### request

User must be logged in and authenticated with Token in header

```txt
GET / api / meals / {id} 
```

### response

```json
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 5,
    "creator": 1,
    "created_date": "2022-04-25T09:51:24.026446-05:00",
    "invitee": [],
    "location": "North Myrtle Beach",
    "radius": 20,
    "lat": null,
    "lon": null
}
```




<!-------------------------- Create a new meal  ------------------------------>


 ## Create A New meal

[Back to Endpoints](#api-endpoints)


### request

User must be logged in and authenticated with Token in header
Required fields: creator(auto), location (string for search), radius

```
POST /api/meal/
```

```json
{
    "creator": 1,
    "invitee": [],
    "location": "Cary, NC",
    "radius": 20,
    "lat": null,
    "lon": null
}
```

### response

```json
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 4,
    "creator": 1,
    "created_date": "2022-04-25T09:51:24.026446-05:00",
    "invitee": [],
    "location": "Cary, NC",
    "radius": 20,
    "lat": null,
    "lon": null
}
```



<!-------------------------- List meals ------------------------------>


## List All meals

[Back to Endpoints](#api-endpoints)


### request


User must be logged in and authenticated with Token in header


```
GET /api/meal/
```

### response


User must be logged in and authenticated.  Token in header


```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 3,
        "creator": 1,
        "created_date": "2022-04-24T17:40:22.850266-05:00",
        "invitee": [],
        "location": "Raleigh",
        "radius": 20,
        "lat": null,
        "lon": null
    },
    {
        "id": 4,
        "creator": 1,
        "created_date": "2022-04-25T09:51:02.586210-05:00",
        "invitee": [],
        "location": "Cary",
        "radius": 20,
        "lat": null,
        "lon": null
    },
    {
        "id": 5,
        "creator": 1,
        "created_date": "2022-04-25T09:51:24.026446-05:00",
        "invitee": [],
        "location": "North Myrtle Beach",
        "radius": 20,
        "lat": null,
        "lon": null
    }
]
```




<!--------------------------- Register new User ------------------------------>
## Register a new user

[Back to Endpoints](#api-endpoints)

### request

Username and password are required.

```json
POST /api/auth/users

{
  "username": "admin",
  "password": "admin"
}
```

### response

```json
201 Created

{
  "email": "",
  "username": "admin",
  "id": 3
}

```

<!-------------------------- LOGIN ------------------------------>
## Log In

[Back to Endpoints](#api-endpoints)

### request

```
POST /api/auth/token/login
```

```json
{
  "username": "admin",
  "password": "admin"
}
```

### response

```json
200 OK
400 Bad Request

{
  "auth_token": "c312049c7f034a3d1b52eabc2040b46e094ff34c"
}
``` 



<!-------------------------- LOGOUT ------------------------------>
## Log Out 

[Back to Endpoints](#api-endpoints)

### request

```
POST /api/auth/token/logout
```

### response

```txt
204 No Content
```


## TemplateHeader

[Back to Endpoints](#api-endpoints)

### request

User must be logged in 

User must be logged in and authenticated with Token in header
Required Fields:

```txt
POST 
```

```json

```

### response

```txt
200 Message
```

```json

```


