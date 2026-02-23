from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create Users
        users = [
            User(email='ironman@marvel.com', username='Iron Man', team=marvel),
            User(email='captainamerica@marvel.com', username='Captain America', team=marvel),
            User(email='spiderman@marvel.com', username='Spider-Man', team=marvel),
            User(email='batman@dc.com', username='Batman', team=dc),
            User(email='superman@dc.com', username='Superman', team=dc),
            User(email='wonderwoman@dc.com', username='Wonder Woman', team=dc),
        ]
        User.objects.bulk_create(users)

        # Refresh users with IDs
        users = list(User.objects.all())
        user_map = {u.username: u for u in users}

        # Create Activities
        Activity.objects.bulk_create([
            Activity(user=user_map['Iron Man'], type='run', duration=30, date=timezone.now().date()),
            Activity(user=user_map['Captain America'], type='cycle', duration=45, date=timezone.now().date()),
            Activity(user=user_map['Spider-Man'], type='swim', duration=25, date=timezone.now().date()),
            Activity(user=user_map['Batman'], type='run', duration=40, date=timezone.now().date()),
            Activity(user=user_map['Superman'], type='fly', duration=60, date=timezone.now().date()),
            Activity(user=user_map['Wonder Woman'], type='row', duration=35, date=timezone.now().date()),
        ])

        # Create Workouts
        w1 = Workout.objects.create(name='Pushups', description='Upper body strength')
        w2 = Workout.objects.create(name='Situps', description='Core strength')
        w3 = Workout.objects.create(name='Squats', description='Lower body strength')
        w1.suggested_for.set([marvel, dc])
        w2.suggested_for.set([marvel])
        w3.suggested_for.set([dc])

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, score=120)
        Leaderboard.objects.create(team=dc, score=110)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
