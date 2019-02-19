import os


class Data:
    """
    This class TestData contains all the data
    used for testing across every test """

    def __init__(self):

        self.test_user = {
            "firstname": "User",
            "lastname": "Test",
            "othername": "UserTest",
            "email": "test@test.com",
            "phoneNumber": "0712332112",
            "username": "testuser",
            "password": "P@5sword",
            "confirmPass": "P@5sword"
        }

        self.admin_data = {
            "username": 'Bjorn',
            "password": 'TestP@ssw0rd'
        }

        self.meetup = {
            "location": "Angle House, Nairobi",
            "images": ["img1.jgp", "img2.jpg"],
            "topic": "Do It Yourself",
            "happeningOn": "Feb 4 2020 10:30AM",
            "tags": ["Creative", "Technology"]
        }

        self.meetup2 = {
            "location": "Kenyatta University, Kiambu",
            "images": ["img1.jgp", "img2.jpg"],
            "topic": "Main Graduation",
            "happeningOn": "Feb 8 2020 10:30AM",
            "tags": ["Creative", "Technology"]
        }

        self.fetch_meetup_data = {
            "topic": "Do It Yourself",
            "location": "Angle House, Nairobi"
        }

        self.wrong_meet_topic = {
            "topic": "This wont be found",
            "location": "Angle House, Nairobi"
        }

        self.missing_meetup_details = {
            "location": "Jungle House, Mombase",
            "images": ["img1.jgp", "img2.jpg"],
            "happeningOn": "Jan 13 2019 10:30AM",
            "tags": ["Creative", "Technology"]
        }

        self.imageless_meetup_details = {
            "location": "Angle House, Nairobi",
            "topic": "Go Imagesless",
            "happeningOn": "Feb 15 2019 10:30AM",
            "tags": ["Creative"]
        }

        self.question = {
            "meetup": 1,
            "title": "Leather bag price",
            "body": "How much would a good leather bag cost"
        }

        self.comment = {
            "question": 1,
            "comment": "Just a sample comment"
        }

        self.image = {
            "images": ["tumbl.url.com", "insta.com"]
        }

        self.tag = {
            "tags": ["Instagram", "ruby"]
        }

        self.rsvp = {
            "response": "yes"
        }
