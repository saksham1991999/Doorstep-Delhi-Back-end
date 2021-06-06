from rest_framework import serializers
from wallet.models import Wallet, Transaction

class WalletSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Wallet
        fields = [
            "id",
            "user",
            "redeemable",
            "non_redeemable"
        ]

class TransactionSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    
    class Meta:
        model = Transaction
        fields = [
            "id",
            "wallet",
            "receiver",
            "creator",
            "type",
            "category",
            "value",
            "running_balance",
            "created_at",
            "is_complete"
        ]

class TransactionListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = [
            "id",
            "type",
            "value",
            "created_at",
            "is_complete",
        ]