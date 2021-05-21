from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.crypto import get_random_string
from faker import Faker

from product.models import Category
from core.management.commands.populate import (
    accounts,
    products,
    store,
    webtraffic,
)


fake = Faker()
Faker.seed(999)


class Command(BaseCommand):
    help = 'Populate the database'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        total = kwargs['total']

        accounts.populate_users(total)
        webtraffic.populate(total)
        products.populate(total)

        store.populate()