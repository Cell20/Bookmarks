from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from account.models import Profile
from django.contrib.auth.models import User
import urllib.request
from datetime import date
import os
import random
from images.models import Image
from decouple import config


LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


class Provider(faker.providers.BaseProvider):
    """Class to provide you custom tags, posts, status or anything custom."""

    def letter(self):
        return self.random_element(LETTERS)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(Provider)

        superusers = User.objects.filter(is_superuser=True)
        if len(superusers) != 1:
            superuser = User.objects.create_superuser(
                username='Cell',
                email=config("EMAIL"),
                password=config("PASSWORD")
            )

        for _ in range(5):
            # Profile fields
            user = fake.unique.first_name()

            user = User.objects.create(
                username=user, password=config("PASSWORD"), first_name=user, last_name=fake.last_name(), email=user+'@gmail.com')

            year = date.today().year
            month = date.today().month
            day = date.today().day

            if os.path.exists(f'media/users/{year}/{month}/{day}/') == False:
                os.makedirs(f'media/users/{year}/{month}/{day}/')

            # urllib.request.urlretrieve(
                # 'https://picsum.photos/200/300.jpg', f"media/users/{year}/{month}/{day}/{user}.jpg")

            Profile.objects.create(user=user, date_of_birth=fake.date())
            # ), photo=f"users/{year}/{month}/{day}/{user.first_name}.jpg")

            # Image fields
            title = f"{fake.word()} {fake.word()} {fake.word()}"
            slug = fake.unique.slug()
            des = fake.unique.text()

            urllib.request.urlretrieve(
                'https://picsum.photos/200/300.jpg', f"media/images/{year}/{month}/{day}/{slug}.jpg")

            current_im = Image.objects.create(user=user, title=title, slug=slug,
                                              url="https://picsum.photos/200/300.jpg", image=f"images/{year}/{month}/{day}/{slug}.jpg", description=des)

            users = User.objects.all()

            # Liking the Images
            users_like = random.sample(list(users), random.randint(1, 25))
            for like in users_like:
                current_im.users_like.add(User.objects.get(id=like.id))

            # Though the above commands can create a Image cuz most fields
            # aren't required but u need to give everyfield value properly to cuz
            # you're in py shell which wasn't the case in UI
