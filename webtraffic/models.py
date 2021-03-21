from django.db import models


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
    ("", "App On-Screen"),
    ("", "App Background"),
    ("", "Website"),
    ("", "Desktop Application"),
)


class WebsiteHit(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)
    website = models.ForeignKey("webtraffic.Website", on_delete=models.CASCADE)
    type = models.CharField(max_length=1)

