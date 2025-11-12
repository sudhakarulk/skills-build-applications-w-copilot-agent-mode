from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db[col].drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample users (super heroes)
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'marvel'},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'marvel'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'dc'},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'dc'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'dc'},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {'name': 'marvel', 'members': ['ironman@marvel.com', 'cap@marvel.com', 'spiderman@marvel.com']},
            {'name': 'dc', 'members': ['batman@dc.com', 'superman@dc.com', 'wonderwoman@dc.com']},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {'user_email': 'ironman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user_email': 'batman@dc.com', 'activity': 'Cycling', 'duration': 45},
            {'user_email': 'spiderman@marvel.com', 'activity': 'Swimming', 'duration': 25},
            {'user_email': 'superman@dc.com', 'activity': 'Yoga', 'duration': 40},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'marvel', 'points': 120},
            {'team': 'dc', 'points': 110},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user_email': 'ironman@marvel.com', 'workout': 'Pushups', 'reps': 50},
            {'user_email': 'wonderwoman@dc.com', 'workout': 'Squats', 'reps': 60},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
