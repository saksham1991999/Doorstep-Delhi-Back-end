from django.db import models


class ClientLog(models.Model):
    path = models.CharField(max_length=150)
    host = models.CharField(max_length=150)
    request_method = models.CharField(max_length=150)
    user_agent = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


class SupportCategory(models.Model):
    title = models.CharField(max_length=200)


class SupportSubCategory(models.Model):
    category = models.ForeignKey("core.SupportCategory", on_delete=models.CASCADE)
    title = models.CharField(max_length=512)


class Support(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    subcategory = models.ForeignKey("core.SupportSubCategory", null=True, on_delete=models.SET_NULL)
    message = models.TextField()
    file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SupportReply(models.Model):
    support = models.ForeignKey("core.Support", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)