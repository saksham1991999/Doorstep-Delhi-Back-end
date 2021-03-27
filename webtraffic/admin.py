from django.contrib import admin
<<<<<<< HEAD
from .models import Website
# Register your models here.
admin.site.register(Website)
=======

from .models import Website, WebsiteHit


admin.register(Website)
admin.register(WebsiteHit)
>>>>>>> 4d14e6a2e2de577beb52a1de5a8e03347ab78c5d
