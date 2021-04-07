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
    addresses = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'profile_pic',
            'email',
            'addresses',
        )

    def get_addresses(self, obj):
        adresses = Address.objects.filter(user=obj)
        serializer = AddressSerializer(adresses, many=True)
        return serializer.data


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

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

