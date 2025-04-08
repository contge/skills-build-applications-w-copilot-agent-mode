from django.core.management.base import BaseCommand
from octofit_tracker.models import User as TrackerUser, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, workouts, and a superuser'

    def handle(self, *args, **kwargs):
        # Create a superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
            self.stdout.write(self.style.SUCCESS('Superuser created: admin / adminpassword'))

        # Create regular test users
        for i in range(1, 6):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username, f'{username}@example.com', 'password')
                self.stdout.write(self.style.SUCCESS(f'Test user created: {username} / password'))

        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            TrackerUser(_id=ObjectId(), name='Thor', email='thor@mhigh.edu', age=30),
            TrackerUser(_id=ObjectId(), name='Tony Stark', email='tony@mhigh.edu', age=45),
            TrackerUser(_id=ObjectId(), name='Steve Rogers', email='steve@mhigh.edu', age=100),
            TrackerUser(_id=ObjectId(), name='Natasha Romanoff', email='natasha@mhigh.edu', age=35),
            TrackerUser(_id=ObjectId(), name='Bruce Banner', email='bruce@mhigh.edu', age=40),
        ]
        TrackerUser.objects.bulk_create(users)

        # Create teams
        team = Team(_id=ObjectId(), name='Blue Team')
        team.save()
        team.members.add(*users)

        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=users[0], activity_type='Cycling', duration=3600),
            Activity(_id=ObjectId(), user=users[1], activity_type='Crossfit', duration=7200),
            Activity(_id=ObjectId(), user=users[2], activity_type='Running', duration=5400),
            Activity(_id=ObjectId(), user=users[3], activity_type='Strength', duration=1800),
            Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=4500),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), team=team, points=100),
            Leaderboard(_id=ObjectId(), team=team, points=90),
            Leaderboard(_id=ObjectId(), team=team, points=95),
            Leaderboard(_id=ObjectId(), team=team, points=85),
            Leaderboard(_id=ObjectId(), team=team, points=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
