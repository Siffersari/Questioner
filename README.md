# Questioner

Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize
questions to be answered. Other users can vote on asked questions and they bubble to the top.

### Background Knowledge
---

This branch contains the API Endpoints for Questioner platform

### Enpoints
---
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

