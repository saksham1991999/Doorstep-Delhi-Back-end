from django.db import models


class ClientLog(models.Model):
    path = models.CharField(max_length=150)
    host = models.CharField(max_length=150)
    request_method = models.CharField(max_length=150)
    user_agent = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)