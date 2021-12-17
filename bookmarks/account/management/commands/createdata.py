from django.core.management.base import BaseCommand
from faker import Faker
from account.models import Profile
from django.contrib.auth.models import User
import urllib.request
from datetime import date
import os


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):
        fake = Faker()
        # fake.add_provider(Provider)

        superusers = User.objects.filter(is_superuser=True)
        if len(superusers) != 1:
            superuser = User.objects.create_superuser(
                username='Cell',
                email='suhail9453531504@gmail.com',
                password='localpasswd'
            )

        for _ in range(5):
            # Profile fields
            user = fake.unique.first_name()

            user = User.objects.create(
                username=user, password='localpasswd', first_name=user, last_name=fake.last_name(), email=user+'@gmail.com')

            year = date.today().year
            month = date.today().month
            day = date.today().day

            if os.path.exists(f'media/users/{year}/{month}/{day}/') == False:
                os.makedirs(f'media/users/{year}/{month}/{day}/')

            urllib.request.urlretrieve(
                'https://picsum.photos/200/300.jpg', f"media/users/{year}/{month}/{day}/{user}.jpg")

            # for user in User.objects.all():
            Profile.objects.create(user=user, date_of_birth=fake.date(
            ), photo=f"users/{year}/{month}/{day}/{user.first_name}.jpg")
