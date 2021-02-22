from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializes User instances"""
    profile_pic = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'profile_pic',
            'email',
        )

