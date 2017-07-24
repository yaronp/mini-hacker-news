# Requirements

# Tasks

* ~~Flask routes - done~~
* ~~Git tags~~
* Docker file - skeleton done
* ~~DAL - done~~
* ~~DB structure~~
* ~~Unit tests - done~~

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

   docker build -t posts:latest
   
## Run the Docker Container

  docker run -d -p 5000:5000 posts   