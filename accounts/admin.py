from django.contrib import admin

from .models import User

admin.site.site_header = 'Doorstep Delhi'
admin.site.register(User)
