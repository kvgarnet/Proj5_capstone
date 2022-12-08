#  Capstone Project

## Content

1. [Motivation](#motivation)
2. [Setup Project](#setup_project)
3. [API Documentation](#api)
4. [Authentification](#authentification)

<a name="motivation"></a>
## Motivation 
### What is Capstone
This is a flask REST API service for final project of `Udacity-Full-Stack-Nanodegree`.
This app helps a Casting Agency models a company that is responsible for creating
movies and managing and assigning actors to those movies. Besides, it also manages 
actors' remuneration relationship between movies and actors
### How can I access the app?
The casting app has been deployed to Heroku at this link:
https://kvzhang-capstone-1213.herokuapp.com/

Inspired by https://auth0.com/docs/quickstart/webapp/python/interactive,
I made basic login/logout endpoint for easy interaction with Auth0

- Click **login** link to log in with predefined user in auth0 dashboard, app will return JWT based on the roles predefined on auth0, which I saved in config.py for easy test
- Click **logout** link to log out.
### Tech topics
It covers following technical topics :
*  Python3 coding with flask including: 
    -  Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
    -  REST API app to 
       - perform CRUD Operations on database with `Flask` (see `app.py`)
       - perform on basic login/logout feature to authenticate with Auth0 (see `app.py`)
    -  Automated testing with `Unittest` (see `test_app,py`)
* Authorization & Role based Authentification with `Auth0` 
    - Auth0 dashboard APP and API setup
    - code integration with auth0 APP and API to handle the authentication login, (see `auth/auth.py`) 
* Deployment on `Heroku`

<a name="setup_project"></a>
## Setup Project Overview
This app can be deployed in two ways:
- locally for easy POC 
- heroku 

we will cover both ways below. 

### Setup locally
To access the app locally, you need a database, a virtual environment, dependencies installed, and environment variables set up. 
You also need an account with Auth0, an authentication service.

 I validated 3.8.9/15 version of [Python 3](https://www.python.org/downloads/)
and version 14.5 of [postgres](https://www.postgresql.org/download/) installed .

1. Initialize and activate a virtualenv:
`cd` into project root folder 
  ```bash
  $ python3 -mvenv proj5_venv  
  $ source proj5_venv/bin/activate
  ```

2. Install the dependencies:
```bash
$ pip install -r requirements.txt
```
3. Change database config so it can connect to your local postgres database.
Update based on your configuration like:
 ```python
db_name="capstone"
db_user='postgres'
db_password='postgres'
db_host="localhost:5432"
SQLALCHEMY_DATABASE_URI =f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
```

4. Setup Auth0 

See [Authentification](#authentification) for details 

If you only want to test API, you can simply take the existing bearer tokens in `config.py`.


5. Run the development server:
  ```bash 
  $ python3 app.py
  ```
access it on http://127.0.0.1:8080

6. init database: create database, tables and seed init data
 NOTE init_db.py WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
,ONLY NECESSARY ON FIRST RUN

  ```bash 
  $ createdb capstone
  $ python3 init_db.py --env local_prod
  ```
7. execute tests functions

configure test DB vars like step 3 in `config.py`,like:
* note: we use python-dotenv as way to import them as env vars
```bash
test_db_name = getenv("TEST_DATABASE_NAME")
test_db_user=getenv("DATABASE_USER")
test_db_password = getenv("DATABASE_PASS")
test_db_path = f"postgresql://{test_db_user}:{test_db_password}@localhost:5432/{test_db_name }"
```
create db and init it 
```bash 
$ createdb test_capstone
$ python3 init_db.py --env local_test
```
it should give this response if everything went fine:

```bash
$ python test_app.py
.........................
----------------------------------------------------------------------
Ran 26 tests in 20.894s

OK

```
### Setup via Heroku
1. clone the github repo in a new folder
2. remove existing .git folder
3. based on requirement of heroku deployment, add below files
   reference: https://devcenter.heroku.com/articles/getting-started-with-python
  - Procfile
  - runtime.txt
4. based on section 6, deployed to heroku as below steps
   - **note: since heroku does not support free plan, we have to subscribe a paid plan for dynos and postgress DB**
 ```bash
#init heroku
heroku login -i
git init
# create heroku app and DB
heroku create myapp-${RANDOM} --buildpack heroku/python 
heroku addons:create heroku-postgresql:mini --app {app_created_last_step}
#list DATABASE_URL
heroku config --app {app_created_last_step}
export DATABASE_URL="***"
# add DATABASE_URL in heroku dashboard UI
# commit and push to heroku git repo
git add .
git commit -am "first commit"
git push heroku main
# click the heroku app url to verify application
``` 

## API Documentation
<a name="api"></a>

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL
**_https://kvzhang-capstone-1213.herokuapp.com_**
### Authentification
Please see [API Authentification](#authentification-bearer)
### How to work with each endpoint
Prerequisites:
On auth0 dashboard, RBAC roles needs to be ready and 3 users assigned to the roles needs to be authenticated to access
different endpoints with different JWT access token.see auth0 configration section for details

To test API, you can simply take the existing bearer tokens in `config.py`.

**Authorication Endpoints**

#### GET /login
- Redirects the user to the Auth0 login page, where the user can log in or sign up
- Roles authorized: all users
- Sample: ```curl http://127.0.0.1:8080/login```

#### GET /post-login
- Handles the response from the access token endpoint and stores the user's information in a Flask session
- Roles authorized: casting assistant, casting_director,executive producer
- Sample: ```curl http://127.0.0.1:8080/callback```

#### GET /logout
- Clears the user's session and logs them out
- Roles authorized: all users
- Sample: ```curl http://127.0.0.1:8080/logout```

**Business Endpoints**

Click on a link to directly get to the ressource.

1. Actors
   1. [GET /actors](#get-actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors](#delete-actors)
   4. [PATCH /actors](#patch-actors)
2. Movies
   1. [GET /movies](#get-movies)
   2. [POST /movies](#post-movies)
   3. [DELETE /movies](#delete-movies)
   4. [PATCH /movies](#patch-movies)

Each resource documentation is structured as below:
1. Description in a few words
2. `curl` example that can directly be used in terminal
3. More descriptive explanation of input & outputs.
4. Required permission
5. Example Response.
6. Error Handling (`curl` command to trigger error + error response)


# <a name="get-actors"></a>
### 1. GET /actors

Query all actors.

```bash
$ curl -X GET https://kvzhang-capstone-1213.herokuapp.com/actors \  
  -H "Authorization: Bearer xxxx"
```
**Note**: if you like to check via browsers, use https://modheader.com/ to add Token got from /login endpoint 
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Headers: **Authorization Header**
- Requires permission: `read:actors`
- Returns: 
  1. List of dict of 'actors' with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
      - **list** `movies` (list of movie names that actor starred in)
  2. **boolean** `success`

#### Example response
```js
{
    "actors": [
        {
            "age": 62,
            "gender": "female",
            "id": 1,
            "movies": [
                "You've got mails"
            ],
            "name": "Meg Ryan"
        },
        ......
    ],
    "success": true
}
```
#### Errors
If you try fetch an endpoint which does not have any actors, you will encounter an error which looks like this:

```bash
$ curl -X GET https://kvzhang-capstone-1213.herokuapp.com/no_actors \
  -H "Authorization: Bearer xxxx"
```
will return
```js
{
"error": 404,
"message": "Resource Not Found",
"success": false
}
```

# <a name="post-actors"></a>
### 2. POST /actors

Insert new actor into database.

```bash
$curl -X POST https://kvzhang-capstone-1213.herokuapp.com/actors/new \
 -H "Authorization: Bearer XXXX" \
     -H "Content-Type:application/json" \
 --data '{"name":"tom","age":42,"gender":"male"}'
```

- Request Arguments: **None**
- Request Headers: 
    - (_application/json_)
        1. **string** `name` 
        2. **integer** `age` 
        3. **string** `gender`
    - **Authorization Header**
- Requires permission: `create:actors`
- Returns: 
  1. List of dict of 'actors' created
  2. **boolean** `success`

#### Example response
```js
{
  "actor": [
    {
      "age": 42,
      "gender": "male",
      "id": 4,
      "movies": [],
      "name": "tom"
    }
  ],
  "success": true
}
```
#### Errors
If you try to create a new actor without a required permission
it will throw a `403` error:

```js
{
  "code": "unauthorized",
  "message": "Permission not found.",
  "success": false
}
}
```
if you try to create a new actor without complete input, it will throw a '400' error like:
```js
{
  "error": 400,
  "message": "Bad Input format",
  "success": false
}
```

# <a name="patch-actors"></a>
### 3. PATCH /actors

Edit an existing Actor

```bash
$ curl -X PATCH https://kvzhang-capstone-1213.herokuapp.com/actors/5
 -H "Authorization: Bearer XXXX" \
     -H "Content-Type:application/json" \
 --data '{"name":"TomLeeJones","age":42,"gender":"male"}'
```

- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: 
    - (_application/json_)
        1. **string** `name`
        2. **integer** `age`
        3. **string** `gender`
    - **Authorization Header**
- Requires permission: `edit:actors`
- Returns: 
  1. **boolean** `success`
  2. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`

#### Example response
```js
{
  "actor": [
    {
      "age": 42,
      "gender": "male",
      "id": 4,
      "movies": [],
      "name": "TomLeeJones"
    }
  ],
  "success": true
}
```
#### Errors
If you try to update an actor with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://kvzhang-capstone-1213.herokuapp.com/actors/125
 -H "Authorization: Bearer XXXX" \
     -H "Content-Type:application/json" \
 --data '{"name":"TomLeeJones","age":42,"gender":"male"}'
```

will return

```js
{
  "error": 404,
  "message": "Resource Not Found",
  "success": false
}
```

# <a name="delete-actors"></a>
### 4. DELETE /actors

Delete an existing Actor

```bash
$ curl -X DELETE https://kvzhang-capstone-1213.herokuapp.com/actors/4 \ 
 -H "Authorization: Bearer xxx"
```

- Request Arguments: **integer** `id from actor you want to delete`
- Request Headers: 
    - **Authorization Header**
- Requires permission: `delete:actors`
- Returns: 
  1. **integer** `id from deleted actor`
  2. **boolean** `success`

#### Example response
```js
{
  "deleted_actor": 4,
  "success": true
}
```
#### Errors
If you try to delete actor with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://kvzhang-capstone-1213.herokuapp.com/actors/125
 -H "Authorization: Bearer xxx"
```

will return

```js
{
  "error": 404,
  "message": "Resource Not Found",
  "success": false
}
```

# <a name="get-movies"></a>
### 5. GET /movies


```bash
$ curl -X GET https://kvzhang-capstone-1213.herokuapp.com/movies \
 -H "Authorization: Bearer XXX"
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Headers: 
    - **Authorization Header**
- Requires permission: `read:movies`
- Returns: 
  1. List of dict of movies with following fields:
      - **integer** `id`
      - **string** `title`
      - **date** `release_date`
  2. **boolean** `success`

#### Example response
```js
{
  "movies": [
    {
      "actors": [
        "Meg Ryan",
        "Tom Hanks"
      ],
      "id": 1,
      "release_date": "1998-12-18",
      "title": "You've got mails"
    },
    {
      "actors": [
        "Tom Hanks",
        "Robin Wright"
      ],
      "id": 2,
      "release_date": "1994-06-23",
      "title": "Forrest Gump"
    },
    {
      "actors": [],
      "id": 3,
      "release_date": "1994-09-10",
      "title": "The Shawshank Redemption"
    }
  ],
  "success": true
}
```
#### Errors
If you try fetch a wrong movies endpoint, you will encounter an '404' error this:

```bash
$ curl -X GET https://kvzhang-capstone-1213.herokuapp.com/no_movies \
 -H "Authorization: Bearer XXX"
```

will return

```js
{
  "error": 404,
  "message": "Resource Not Found",
  "success": false

```

# <a name="post-movies"></a>
### 6. POST /movies

Insert new Movie into database.

```bash
$ curl -X POST https://kvzhang-capstone-1213.herokuapp.com/movies/new \
  -H "Content-Type: application/json" -H "Authorization: Bearer XXX" \
--data '{"title": "dummy movie5","release_date": "12-25-2009"}'
```

- Request Arguments: **None**
- Request Headers:
    - (_application/json_)
        1. **string** `title`
        2. **string** `release_date`
    - **Authorization Header**
- Requires permission: `create:movies`
- Returns: 
  1. **list of dict**: `new_movie` (format output of newly created movie)
  2. **boolean** `success`

#### Example response
```js
{
  "new_movie": [
    {
      "actors": [],
      "id": 6,
      "release_date": "2023-12-25",
      "title": "dummy movie5"
    }
  ],
  "success": true

```
#### Errors
If you try to create a new movie without a required field like `title`,
it will throw a `400` error:

```bash
$ curl -X GET https://kvzhang-capstone-1213.herokuapp.com/movies/new \
  -H "Content-Type: application/json" -H "Authorization: Bearer XXX" \
--data '{"title": "dummy movie5"}'
```

will return

```js
{
  "error": 400,
  "message": "Bad Input format",
  "success": false
}
```

# <a name="patch-movies"></a>
### 7. PATCH /movies

Edit an existing Movie

```bash
$ curl -X PATCH https://kvzhang-capstone-1213.herokuapp.com/movies/6
-H "Content-Type: application/json" \
-H "Authorization: Bearer XXX" \
--data '{"title": "dummy movie6","release_date": "12-25-2023"}'

```

- Request Arguments: **integer** `id from movie you want to update`
- Request Headers:
    - (_application/json_)
        1. **string** `title`
        2. **string** `release_date`
    - **Authorization Header**
- Requires permission: `edit:movies`
- Returns: 
  1. **boolean** `success`
  2. List of dict of movies with following fields:
        - **integer** `id`
        - **string** `title` 
        - **date** `release_date` 

#### Example response
```js
{
    "movie": [
        {
            "actors": [],
            "id": 6,
            "release_date": "2023-12-25",
            "title": "dummy movie6"
        }
    ],
    "success": true
}
```
#### Errors
If you try to update an movie with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://kvzhang-capstone-1213.herokuapp.com/movies/125
```

will return

```js
{
  "error": 404,
  "message": "Resource Not Found",
  "success": false
}
```
# <a name="delete-movies"></a>
### 8. DELETE /movies

Delete an existing movie

```bash
$ curl -X DELETE https://kvzhang-capstone-1213.herokuapp.com/movies/6
-H "Content-Type: application/json" \
-H "Authorization: Bearer XXX"
```

- Request Arguments: **integer** `id from movie you want to delete`
- Request Headers:
    - **Authorization Header**
- Requires permission: `delete:movies`
- Returns: 
  1. **integer** `id from deleted movie`
  2. **boolean** `success`

#### Example response
```js
{
  "deleted_movie": 6,
  "success": true
}
```
#### Errors
If you try to delete movie with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://kvzhang-capstone-1213.herokuapp.com/movies/125
```

will return

```js
{
    "error": 404,
    "message": "Resource Not Found",
    "success": false
}
```

# <a name="authentification"></a>
## Authentification

All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 accordingly

### Setup Auth0 for locally use
#### Create an App & API
- create APP
1. Login to https://manage.auth0.com/ 
2. Click on Applications Tab
3. Create Application
4. Give it a name like `CapstoneAPP` and select "Regular Web Application"
5. Go to Settings
   - find `domain`. Copy & paste it into value of  'AUTH0_DOMAIN' of `auth/.env`  (i.e. replace `"kvzhang.us.auth0.com"`)
   - find `Client id`. Copy & paste it into value of  'AUTH0_CLIENT_ID' of `auth/.env`     
   - find `Client Secret`. Copy & paste it into value of  'AUTH0_CLIENT_SECRET' of `auth/.env`
6. set callback URL based on the host and endpoints(app.py), e.g. http://127.0.0.1:8080/callback
7. set logout URL based on the host and endpoints(app.py), e.g. http://127.0.0.1:8080
- create API
1. Click on API Tab 
2. Create a new API:
   1. Name: `CapstoneAPI`
   2. Identifier `capstone`
   3. Keep Algorithm as it is
3. Go to Settings and find `Identifier`. Copy & paste it into value of 'API_IDENTIFIER' of `auth/.env` (i.e. `"capstone"`)

#### Create Roles & Permissions

1. Before creating `Roles & Permissions`, you need to `Enable RBAC` in your API (API => Click on your API Name => Settings = Enable RBAC => Save)
2. Also, check the button `Add Permissions in the Access Token`.
2. First, create a new Role under `Users and Roles` => `Roles` => `Create Roles`
3. Give it a descriptive name like `Casting Assistant`.
4. Go back to the API Tab and find your newly created API. Click on Permissions.
5. Create & assign all needed permissions accordingly 
6. After you created all permissions this app needs, go back to `Users and Roles` => `Roles` and select the role you recently created.
7. Under `Permissions`, assign all permissions you want this role to have. 
8. Under `Users`, assign specific users you want with this role. 

# <a name="authentification-bearer"></a>
### Auth0 to use existing API
If you want to access the real, temporary API, bearer tokens for all 3 roles are included in the `config.py` file.

### Setup Auth0 for heroku
#### Create an App 
- create APP
Use same steps as setup for locally
only difference from auth0 setup for local use is use the heroku URL for callback and logout URL

- create API
do not need to recreate API, use above API 

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (view:actors): Can see all actors
  - GET /movies (view:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (add:actors): Can create new Actors
  - PATCH /actors (modify:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (modify:movies): Can edit existing Movies
3. Exectutive Director (everything from Casting Director plus)
  - POST /movies (add:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Movies from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

For example: (Bearer token for `Executive Director`)
```js
{
    "Authorization": "Bearer XXXXXX"
}
```
