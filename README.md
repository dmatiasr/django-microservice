# django-microservice


### How to install:
#### docker-compose up --build 


### stop docker-compose and run:

#### docker-compose run django_app python character_project/manage.py migrate
#### docker-compose run django_app python character_project/manage.py collecstatic
### again runserver:
#### docker-compose up --build 


### How to use:

Open Postman app or similar app:

##### GET: http://localhost:8000/character/3/
##### HEADERS : Authorization - Token f9cf22b1a6533a6eceec39ef1f15689345d5e6c7

##### RESPONSE:
{
    "name": "R2-D2",
    "height": "96",
    "mass": "32",
    "hair_color": "n/a",
    "skin_color": "white, blue",
    "eye_color": "red",
    "birth_year": "33BBY",
    "gender": "n/a",
    "homeworld": {
        "name": "Naboo",
        "population": "4500000000",
        "known_residents_count": 10
    },
    "species": "Droid",
    "average_rating": 3.6666666666666665,
    "max_rating": 5
}

##### POST: http://localhost:8000/character/30/rating/
##### HEADERS : Authorization - Token f9cf22b1a6533a6eceec39ef1f15689345d5e6c7


##### RESPONSE:
Simil to, 
{
    "score": 2,
    "related_character": {
        "pk": 9,
        "slug": "30",
        "avg": 2.0,
        "max_score": 2
    }
}


> This example has database included just for Test. Not use in production enviroment

