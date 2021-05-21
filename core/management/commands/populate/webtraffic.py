import os, django

from faker import Faker

from accounts.models import User
from webtraffic.models import Website, WebsiteHit

fake = Faker()
Faker.seed(999)


def populate(N):
    populate_websites(N)
    populate_website_hits(N)


def populate_websites(N):
    users = User.objects.all()
    users_count = users.count()
    Website.objects.bulk_create(
        [
            Website(
                user=users[fake.random_int(max = users_count-1)],
                name=fake.word(),
                url=fake.url(),
                timer=fake.random_int(min=10, max=100),
                category=fake.random_element(elements=("S", "A", "P", "WS")),
                daily_hits=fake.random_int(min=10, max=100),
                total_hits=fake.random_int(min=100, max=1000),
                status=fake.random_element(elements=("A", "I", "R")),
                traffic_source=fake.random_element(elements=("D", "R", "U")),
                high_quality=fake.pybool(),
                page_scroll=fake.pybool(),
                clicks=fake.pybool(),
                reload_page=fake.pybool(),
                cost_per_visit=fake.random_int(min=10, max=100),
            )
            for _ in range(3*N)
        ]
    )


def populate_website_hits(N):
    users = User.objects.all()
    users_count = users.count()
    websites = Website.objects.all()
    websites_count = websites.count()
    WebsiteHit.objects.bulk_create(
        [
            WebsiteHit(
                user=users[fake.random_int(max=users_count-1)],
                website=websites[fake.random_int(max=websites_count-1)],
                type=fake.random_element(elements=("O", "B", "W", "D")),
            )
            for _ in range(fake.random_int(min=10*N, max=100*N))
        ]
    )