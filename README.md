# API Reference

## **Getting Started**

- Base URL: The backend app is hosted at your local  machine (http://localhost:8080/)
- Heroku URL: This Backend app is hosted in a heroku server at (https://capstonev1-fsnd.herokuapp.com/)
- Authetication: This version of the application requiere authenticationn or API Keys.
    -Casting Producer: all priviligies
    -Casting Director: get actors and movies, update actors and movie, create and delete only actors 
    -Use this URL to login (https://jatobrun.auth0.com/authorize?audience=capstone&response_type=token&client_id=jXXo40PkZ64pP3DucbnTffjHRQg1omMw&redirect_uri=http://localhost:8080/)
    - if u want to be Casting Director login with: castingdirector@gmail.com, castingDirector123.
    - if u want to be Casting Producer login with: castingproducer@gmail.com, castingProducer123.
### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the coman line with migrations. From the  folder in terminal run:

```bash
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

## Running the server

From within the project directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python3 app.py
```

## **Error Handling**

Errors are returned  as JSON objects in the following format:

```
{
    'success': False,
    'error': 404,
    'message': 'Resource Not Found'
}
```

The API will return three error types when a request fail:

- 404 Resource Not Found
- 422 Unprocessable
- Auth errors (401 and 400)

## **Enpoints**

### **GET /actors**
- General :
    - Returns a list of all actors, id:type  (key:value) 
- Sample: curl http://localhost:8080/actors

```
{
  "actors": [
    {
      "age": 20,
      "gender": "Male",
      "id": 3,
      "name": "Marcos"
    },
    {
      "age": 20,
      "gender": "Male",
      "id": 4,
      "name": "Edgar"
    }
  ],
  "success": true
}
```
### **GET /movies**
- General :
    - Returns a list of all movies. This movies contains (title:str, release_date:Date)
- Sample: curl http://localhost:8080/movies/

```
{
  "movies": [
    {
      "id": 1,
      "release_date": "2010/10/15",
      "title": "Thor"
    },
    {
      "id": 3,
      "release_date": "29/01/2020",
      "title": "Spiderman"
    },
    {
      "id": 4,
      "release_date": "29/01/2020",
      "title": "Spiderman"
    }
  ],
  "success": true
}

```

### **DELETE /actors/actors_id**
- General :
    - Deletes a specific actor
    - Returns a message if delete is complete with success = True, else success = False and the id of the user 
- Sample: curl http://localhost:8080/actors/4 -X DELETE

```
{
  "id_actor": 4,
  "succes": true
}    
```

### **DELETE /movies/movie_id**
- General :
    - Deletes a specific movie
    - Returns a message if delete is complete with success = True, else success = False 
- Sample: curl http://localhost:8080/movies/3 -X DELETE

```
{
  "id_movie": 3,
  "succes": true
}
```
### **POST /actors/**
- General :
    - Create an actor
    - Returns a message if create is complete with success = True, else success = False 
- Sample: curl http://localhost:8080/actors/ -X POST -H 'Content-type: application/json' -d "{'name': 'Marcos', 'gender': 'Male', 'movie_id': '1', 'age': '20'}" 

```
{
  "actor": {
    "age": 20,
    "gender": "Male",
    "id": 5,
    "name": "Marcos"
  },
  "success": true
}    
```
### **POST /movies/**
- General :
    - Create a movie
    - Returns a message if create is complete with success = True, else success = False
- Sample: curl http://localhost:8080/movies/ -X POST -H 'Content-type: application/json' -d "{'title': 'Spiderman', 'release_date': '29/01/2020'}" 

```
{
  "movie": {
    "id": 5,
    "release_date": "29/01/2020",
    "title": "Spiderman"
  },
  "success": true
}   
```
### **PATCH /movies/4**
- General :
    - Update a movie
    - Returns a message if update is complete with success = True, else success = False
- Sample: curl http://localhost:8080/movies/4 -X PATCH -H 'Content-type: application/json' -d "{'title': 'Thor', 'release_date': '15/10/2021'}" 

```
{
  "id_movie": 4,
  "succes": true
}
```
### **PATCH /actors/4**
- General :
    - Update an actor
    - Returns a message if update is complete with success = True, else success = False
- Sample: curl http://localhost:8080/actors/4 -X PATCH -H 'Content-type: application/json' -d "{'name': 'Marcos', 'gender': 'Female', 'movie_id' = '2'}" 

```
{
  "id_actor": 4,
  "succes": true
}
```
