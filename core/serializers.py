from rest_framework import serializers
from .models import ClientLog, Support, SupportCategory, SupportReply, SupportSubCategory

from .models import Notification, ClientLog, Support, SupportCategory, SupportReply, SupportSubCategory


class NotificationSerializer(serializers.ModelSerializer):
    is_dismissible = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "image",
            "datetime",
            "is_dismissible",
        ]

    def get_is_dismissible(self, obj):
        request = self.context.get('request', None)
        if request:
            if obj.user == request.user:
                return True
        return False


class ClientLogSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = ClientLog
        fields = [
            "path",
            "host",
            "request_method",
            "user_agent",
            "created_at"
        ]


class SupportCategorySerializer(serializers.ModelSerializer):
    class meta:
        model = SupportCategory
        field = [
            "title"
        ]


class SupportSubCategorySerilizer(serializers.ModelSerializer):
    category = SupportCategorySerializer()

    class meta:
        model: SupportSubCategory
        field = [
            "category",
            " title"
        ]


class SupportSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    subcategory = SupportSubCategorySerilizer()
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = ClientLog
        fields = [
            "user",
            "subcategory",
            "message",
            "file",
            "created_at"
        ]


class SupportReplySerializer(serializers.ModelSerializer):
    support = SupportSerializer()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = ClientLog
        fields = [
            "user",
            "subcategory",
            "message",
            "file",
            "created_at"
        ]
