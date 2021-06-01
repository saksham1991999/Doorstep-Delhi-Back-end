from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    redeemable = models.PositiveIntegerField(default=0)
    non_redeemable = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "User Wallet"


transaction_category_choices = (
    ('Transfer', 'Transferred'),
    ('Order', 'Ordered'),
    ('Earned', 'Earned'),
    ('Redeemed', 'Redeemed'),
    ('Cashback', 'Cashback'),
)


class Transaction(models.Model):
    wallet = models.ForeignKey("wallet.Wallet", on_delete=models.PROTECT)
    receiver = models.ForeignKey('accounts.User', related_name='receiver', on_delete=models.PROTECT, default='')
    creator = models.ForeignKey("accounts.User", related_name='creator', on_delete=models.PROTECT, default='')
    type = models.BooleanField()
    category = models.CharField(max_length=15, choices=transaction_category_choices)
    value = models.FloatField()
    running_balance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)

