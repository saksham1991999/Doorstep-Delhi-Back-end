from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


website_category_choices = (
    ("S", "Safe"),
    ("A", "Adult"),
    ("P", "PTP"),
    ("WS", "with Sounds"),
)


class UserPreference(models.Model):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    category = models.CharField(max_length=5, choices=website_category_choices)


traffic_source_choices = (
    ("D", "Direct"),
    ("R", "Referer"),
    ("U", "User-Agent"),
)


class Website(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    url = models.URLField()
    timer = models.PositiveIntegerField()
    category = models.CharField(max_length=5, choices=website_category_choices)
    daily_hits = models.PositiveSmallIntegerField()
    total_hits = models.PositiveIntegerField()
    status = models.CharField(max_length=5)
    traffic_source = models.CharField(max_length=5, choices = traffic_source_choices)
    high_quality = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    page_scroll = models.BooleanField(default=False)
    clicks = models.BooleanField(default=False)
    reload_page = models.BooleanField(default=False)

    cost_per_visit = models.PositiveIntegerField()


website_hit_type_choices = (
    ("O", "App On-Screen"),
    ("B", "App Background"),
    ("W", "Website"),
    ("D", "Desktop Application"),
)


class WebsiteHit(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)
    website = models.ForeignKey("webtraffic.Website", on_delete=models.CASCADE)
    type = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender = Website)
def my_call(sender, instance,*args,**kwargs):
    cost = 2*instance.timer
    if instance.category == "WS":
        cost += 10
    elif instance.category == "P":
        cost += 25
    elif instance.category == "A":
        cost += 20

    if instance.high_quality:
        cost += 40
    if instance.page_scroll:
        cost += 20
    if instance.clicks:
        cost += 20
    if instance.reload_page:
        cost += 20
    instance.cost_per_visit = cost

