# Routes

* /post
* /post?id
* /upvote?id
* /downvote?id
* /posts

# Running

## Pre-requisites

    pip install flask

## Run

    cd web
    python app.py 
    
## Docker Image Build

    docker build ./ -t posts:latest
   
## Run the Docker Container

    docker run -d -p 5000:5000 --name posts posts   
 
or 

    docker-compose up -d
# Tasks

* ~~Flask routes - done~~
* ~~Git tags~~
* ~~Docker file - done~~
* ~~DAL - done~~
* ~~DB structure~~
* ~~Unit tests - done~~
* Docker compose
* Wilson score support for ranking
* Redis support
* User login
* Single voting
  