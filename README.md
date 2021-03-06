# Questioner

Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize
questions to be answered. Other users can vote on asked questions and they bubble to the top.

### Badges
[![Build Status](https://travis-ci.com/Siffersari/Questioner.svg?branch=developv2)](https://travis-ci.com/Siffersari/Questioner) [![Coverage Status](https://coveralls.io/repos/github/Siffersari/Questioner/badge.svg?branch=ft-user-login-163047289)](https://coveralls.io/github/Siffersari/Questioner?branch=ft-user-login-163047289) [![Maintainability](https://api.codeclimate.com/v1/badges/132f7853a5541a616bba/maintainability)](https://codeclimate.com/github/Siffersari/Questioner/maintainability)


### Background Knowledge


This branch contains the API Endpoints for Questioner platform persisted on a database

### Endpoints

This platform has the following endpoints

#### Meetup Endpoints

Method | Endpoint | Purpose
--- | --- | ---
POST | /meetups | Create a meetup record
POST | /meetups/int:meetup-id/rsvps | Respond to meetup RSVP
POST | /meetups/int:meetup-id/tags | Add tags to a meetup
POST | /meetups/int:meetup-id/images | Add images to a meetup
GET | /meetups/int:meetup-id | Fetch a specific meetup record
GET | /meetups/upcoming | Fetch all upcoming meetup records
GET | /meetups/int:meetup_id/questions | Fetches all questions to a specific meetup record
DELETE | /meetups/int:meetup-id | Delete a meetup

#### Question Endpoints

Method | Endpoint | Purpose
--- | --- | ---
POST | /questions | Create a question for a specific meetup
GET | /questions | Fetches all question records
GET | /questions/Int:question_id | Fetches a specific question
GET | /questions/int:question_id/comments | Fetches all comments to a specific question record
PATCH | /questions/int:question-id/upvote | Upvote a specific question
PATCH | /questions/int:question-id/downvote | Downvote a specific question
DELETE | /questions/int:question_id | Deletes a specific question record


#### Comment Endpoints

Method | Endpoint | Purpose
--- | --- | ---

POST | /comments | Comment on a question

GET | /comments/int:comment_id | Fetches a specific comment to a question

DELETE | /comments/int:comment_id | Deletes a specific comment record

#### User Endpoints

Method | Endpoint | Purpose
--- | --- | ---
POST | /auth/signup | Register a new users
POST | /auth/login | Log in registered users
POST | /auth/logout | Log out users 
GET | /users | Fetch details of a specific user
GET | /users/string:email | Request Password Reset Link
POST |/auth/reset_password/token | Reset Password

### Pre-requisites
```
1. Python 3.6 or higher
2. Git
3. Virtualenv
4. Pytest

```
## Getting Started

Clone this repository inside your working repository
```
git clone https://github.com/Siffersari/Questioner.git

```
Navigate into the cloned repository
```
cd Questioner/
```
Switch to develop branch
```
git checkout develop
```


### Installation
Set up a virtual environment

```
virtualenv -p python3 venv
```

Activate the environment

```
source venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```

Run the application
```
flask run
```

### Testing
Run the command
```
pytest app/tests/v2

```


#### Author 
Leewel K. Mwangi