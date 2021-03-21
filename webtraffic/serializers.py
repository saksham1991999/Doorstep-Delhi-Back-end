from rest_framework import serializers
from .models import * # Website

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'
        read_only_fields = ['daily_hits', 'total_hits']
