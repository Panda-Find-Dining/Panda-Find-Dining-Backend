# Find Dining Backend Application    

This will store our endpoints and instructions

## Models

### User
- friends: M2M

### Meal    
- creator: Fk
- created_date: DateTimeField
- invitee: M2M
- location: CharField
- radius: Int
- lat: Float
- lon: Float

### Restaurant
- name: Char
- lat: Float
- lon: Float
- formatted_address: Char
- place_id: Char
- hours: Char
- business_status: Bool
- icon: URLfield
- meal: Fk

## Base URL


```shell
https://find-dining-panda.herokuapp.com/
```


## API Endpoints
    

|Method|Endpoint|Description|Deployed|
|-|-|-|-|
|POST|[/api/auth/users/](#register-a-new-user)|register a new user|Yes|
|POST|[/api/auth/token/login/](#log-in)|login with existing user|Yes|
|POST|[/api/auth/token/logout/](#log-out)|logout with existing user|Yes|
|GET|[/api/meals/](#list-all-meals)|List all meals|Yes|
|GET|[/api/meals/{id}](#retrieve-a-specific-meal)|Retrieve a specific meal|Yes|
|POST|[/api/meals/](#create-a-new-meal)|Add a new meal|Yes|
|PUT|[/api/meals/{id}](#update-an-existing-meal)|Update an existing meal|Yes|
|PATCH|[/api/meals/{id}](#update-an-existing-meal)|Update part of an existing meal|Yes|
|DELETE|[/api/meals/{id}](#delete-meal)|Delete an existing meal|Yes|
|POST|[/api/users/](#get-list-of-all-users)|Get list of all users|Yes|
|POST|[/api/follow/](#follow-user)|Follow (or friend) a new user|Yes|
|DELETE|[/api/unfollow/](#unfollow-user)|Unfollow (or unfriend) a user|Yes|


<!-------------------------- Unfollow or Unfriend a User  ------------------------------>

## Unfollow user


[Back to Endpoints](#api-endpoints)


### request


User must be logged in and authenticated with Token in header


```txt
DELETE / api / unfollow / <pk> 
```

### response

```txt
HTTP 200 OK
Allow: DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```

```json
{
	"Requested": "Deleted!"
}
```



<!-------------------------- Follow or Friend a User  ------------------------------>

## Follow user


[Back to Endpoints](#api-endpoints)


### request


User must be logged in and authenticated with Token in header


```txt
POST / api / follow / <pk> 
```

### response

```txt
HTTP 200 OK
Allow: POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```

```json
{
	"Requested": "Save request has been sent!!"
}
```




<hr>

<!-------------------------- Get list of all users  ------------------------------>

## Get list of all users


[Back to Endpoints](#api-endpoints)


### request


User must be logged in and authenticated with Token in header


```txt
GET / api / users 
```

### response

```txt
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```

```json
[
    {
        "id": 2,
        "username": "Ryan",
        "friends": []
    },
    {
        "id": 3,
        "username": "Paul",
        "friends": []
    },
    {
        "id": 4,
        "username": "Tyler",
        "friends": []
    },
    {
        "id": 5,
        "username": "KE",
        "friends": []
    },
    {
        "id": 1,
        "username": "admin",
        "friends": []
    }
]
```


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

```txt
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



```txt

HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

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

```txt

HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

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





<!-------------------------- Get Meal Details  ------------------------------>

## Retrieve a specific meal

[Back to Endpoints](#api-endpoints)

### request

User must be logged in and authenticated with Token in header

```txt
GET / api / meals / {id} 
```

### response



```txt

HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

```




```json
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
    "creator": 3,
    "invitee": [1,
        2,
        3,
        4,
        5
    ],
    "location": "Cary, NC",
    "radius": 20,
    "lat": null,
    "lon": null
}

```

### response


```txt

HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```



```json
{
  "id": 10,
  "creator": 3,
  "created_date": "2022-04-27T10:06:16.694038-05:00",
  "invitee": [
    2,
    3,
    4,
    5,
    1
  ],
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


```txt

HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

```




```json
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


```txt

201 Created

```



```json
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


```txt

200 OK
400 Bad Request

```



```json
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


