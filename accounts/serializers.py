from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import User, Address


class UserSerializer(serializers.ModelSerializer):
    """Serializes User instances"""

    profile_pic = VersatileImageFieldSerializer(
        sizes=[
            ("full_size", "url"),
            ("thumbnail", "thumbnail__100x100"),
            ("medium_square_crop", "crop__400x400"),
            ("small_square_crop", "crop__50x50"),
        ]
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "profile_pic",
            "email",
        )


class AddressSerializer(serializers.ModelSerializer):
    """ Serializes Addresses """

    user = UserSerializer(many=False)

    class Meta:
        model = Address
        fields = [
            "user",
            "full_name",
            "street_address_1",
            "street_address_2",
            "city",
            "state",
            "postal_code",
            "country",
            "country_area",
            "phone",
        ]

    def create(self, validated_data):

        user = validated_data.pop('user')
        addresses = Address.objects.create(**validated_data)
        for address in addresses:
            Address.objects.create(user=user, **address)
        return addresses
