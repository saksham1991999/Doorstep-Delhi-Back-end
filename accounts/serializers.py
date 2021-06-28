from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_framework.authtoken.models import Token

from .models import User, Address


class CustomRegisterSerializer(RegisterSerializer):
    referral_code = serializers.CharField(allow_blank = True, allow_null=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField(allow_blank = True, allow_null=True)
    email = serializers.EmailField(allow_blank = True, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'mobile', 'first_name', 'last_name')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'mobile': self.validated_data.get('referral_code', ''),

        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        # referral_code = self.cleaned_data.get('referral_code')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key', 'user')


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
    # addresses = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_pic',
            'email',
            # 'addresses',
            'password'
        )

    def get_addresses(self, obj):
        adresses = Address.objects.filter(user=obj)
        serializer = AddressSerializer(adresses, many=True)
        return serializer.data


class FullUserSerializer(serializers.ModelSerializer):
    """Serializes User instances"""

    # profile_pic = VersatileImageFieldSerializer(
    #     sizes=[
    #         ("full_size", "url"),
    #         ("thumbnail", "thumbnail__100x100"),
    #         ("medium_square_crop", "crop__400x400"),
    #         ("small_square_crop", "crop__50x50"),
    #     ]
    # )
    addresses = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            # 'profile_pic',
            'email',
            'addresses',
            'password'
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
            "phone",
        ]

class FullAddressSerializer(serializers.ModelSerializer):
    user = FullUserSerializer()

    class Meta:
        model = Address
        fields = [
            "id",
            "user",
            "full_name",
            "street_address_1",
            "street_address_2",
            "city",
            "state",
            "postal_code",
            "phone",
        ]