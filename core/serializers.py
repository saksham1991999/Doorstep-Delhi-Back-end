from rest_framework import serializers
from .models import ClientLog,Support,SupportCategory,SupportReply,SupportSubCategory

from .models import ClientLog,Support,SupportCategory,SupportReply,SupportSubCategory

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
          model= SupportCategory
          field=[
              "title"
          ]
class SupportSubCategorySerilizer(serializers.ModelSerializer):
     category=SupportCategorySerializer()
     class meta:
         model: SupportSubCategory
         field=[
             "category",
             " title"
         ]
class SupportSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    subcategory= SupportSubCategorySerilizer()
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
    support=SupportSerializer()
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

   