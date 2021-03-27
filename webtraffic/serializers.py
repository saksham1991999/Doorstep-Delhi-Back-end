from rest_framework import serializers
<<<<<<< HEAD
from .models import * # Website

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'
        read_only_fields = ['daily_hits', 'total_hits']
=======
from rest_framework.fields import CurrentUserDefault
from datetime import datetime

from .models import Website


class WebsiteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    cost_per_visit = serializers.IntegerField(read_only=True)

    class Meta:
        model = Website
        fields = (
            "id",
            "user",
            "name",
            "url",
            "timer",
            "category",
            "daily_hits",
            "total_hits",
            "traffic_source",
            "high_quality",
            "page_scroll",
            "clicks",
            "reload_page",
            "status",
            "created_at",
            "updated_at",
            "cost_per_visit",
        )
>>>>>>> 4d14e6a2e2de577beb52a1de5a8e03347ab78c5d
