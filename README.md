# Questioner

Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize
questions to be answered. Other users can vote on asked questions and they bubble to the top.

### Badges
[![Build Status](https://travis-ci.com/Siffersari/Questioner.svg?branch=develop)](https://travis-ci.com/Siffersari/Questioner) [![Coverage Status](https://coveralls.io/repos/github/Siffersari/Questioner/badge.svg?branch=ft-user-login-163047289)](https://coveralls.io/github/Siffersari/Questioner?branch=ft-user-login-163047289) [![Maintainability](https://api.codeclimate.com/v1/badges/132f7853a5541a616bba/maintainability)](https://codeclimate.com/github/Siffersari/Questioner/maintainability)


### Background Knowledge


This branch contains the API Endpoints for Questioner platform

### Enpoints

The platform should have the following endpoints at minimum

Method | Endpoint | Purpose
--- | --- | ---
POST | /meetups | Create a meetup record
GET | /meetups/int:meetup-id | Fetch a specific meetup record
GET | /meetups/upcoming | Fetch all upcoming meetup records
POST | /questions | Create a question for a specific meetup
PATCH | /questions/int:question-id/upvote | Upvote a specific question
PATCH | /questions/int:question-id/downvote | Downvote a specific question
POST | /meetups/int:meetup-id/rsvps | Respond to meetup RSVP

