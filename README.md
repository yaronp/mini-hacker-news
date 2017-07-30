# Routes

* /v0/post
* /v0/post?id
* /v0/upvote?id
* /v0/downvote?id
* /v0/topstories

# Running (stand alone)

## Pre-requisites

    pip install flask
    pip install pymongo   
    
    running mongodb server on port 27017, no security

## Run

    cd web
    python app.py 
    
## Docker Image Build

    docker-compose build
   
## Run the Docker Container

    docker-compose up -d
    
# Tasks

* ~~Flask routes - done~~
* ~~Git tags~~
* ~~Docker file - done~~
* ~~DAL - done~~
* ~~DB structure~~
* ~~Unit tests - done~~
* ~~Docker compose~~
* ~~Wilson score support for ranking~~
* ~~MongoDB support~~
* User login
* Single voting
  