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





## Retrieve a specific meal
GET / meals / {id}

## Update an existing meal
PUT / meals / {id}

## Update an existing meal
PATCH / meals / {id}

## Delete an existing meal
DELETE / meals / {id}


<!-------------------------- List meals ------------------------------>


 ## Create A New meal

[Back to Endpoints](#api-endpoints)

### request

Required fields:

```
POST /meal/
```

```json

```

### response

```json
201 Created

```



<!-------------------------- List meals ------------------------------>


## List All meals

[Back to Endpoints](#api-endpoints)


### request

```
GET /meal/
```

### response

```json

```




<!--------------------------- Register new User ------------------------------>
## Register a new user

[Back to Endpoints](#api-endpoints)

### request

Username and password are required.

```json
POST auth/users

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
POST auth/token/login
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
POST auth/token/logout
```

### response

```txt
204 No Content
```


