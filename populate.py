import os, django

from core.management.commands.populate import store

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doorstepdelhi.settings")
django.setup()


store.add_shipping_zones(10)