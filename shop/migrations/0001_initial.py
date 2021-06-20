# Generated by Django 3.1.7 on 2021-06-20 15:33

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_auto_20210620_2103'),
        ('accounts', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=16, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('last_used_on', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('initial_balance_amount', models.DecimalField(decimal_places=3, max_digits=12)),
                ('current_balance_amount', models.DecimalField(decimal_places=3, max_digits=12)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gift_cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('unconfirmed', 'Unconfirmed'), ('unfulfilled', 'Unfulfilled'), ('partially_fulfilled', 'Partially fulfilled'), ('partially_returned', 'Partially returned'), ('returned', 'Returned'), ('fulfilled', 'Fulfilled'), ('canceled', 'Canceled')], default='unfulfilled', max_length=32)),
                ('tracking_client_id', models.CharField(blank=True, editable=False, max_length=36)),
                ('shipping_price', models.DecimalField(decimal_places=3, default=0, editable=False, max_digits=12)),
                ('total_net_amount', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('undiscounted_total_net_amount', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('display_gross_prices', models.BooleanField(default=True)),
                ('customer_note', models.TextField(blank=True, default='')),
                ('billing_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='accounts.address')),
                ('gift_cards', models.ManyToManyField(blank=True, related_name='orders', to='shop.GiftCard')),
                ('pickup_point', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='store.pickuppoint')),
                ('shipping_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='accounts.address')),
                ('shipping_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='store.shippingmethod')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('entire_order', 'Entire order'), ('shipping', 'Shipping'), ('specific_product', 'Specific products, collections and categories')], default='entire_order', max_length=20)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.PositiveSmallIntegerField(null=True)),
                ('code', models.CharField(db_index=True, max_length=12, unique=True)),
                ('usage_limit', models.PositiveIntegerField(blank=True, null=True)),
                ('used', models.PositiveIntegerField(default=0, editable=False)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('apply_once_per_order', models.BooleanField(default=False)),
                ('apply_once_per_customer', models.BooleanField(default=False)),
                ('discount_value_type', models.CharField(choices=[('fixed', 'fixed'), ('percentage', '%')], default='fixed', max_length=10)),
                ('min_checkout_items_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, to='product.Category')),
                ('collections', models.ManyToManyField(blank=True, to='product.Collection')),
                ('products', models.ManyToManyField(blank=True, to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('fixed', 'fixed'), ('percentage', '%')], default='fixed', max_length=10)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, to='product.Category')),
                ('collections', models.ManyToManyField(blank=True, to='product.Collection')),
                ('products', models.ManyToManyField(blank=True, to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('quantity_fulfilled', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('order', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='shop.order')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_lines', to='product.productvariant')),
                ('wholesale_variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_lines', to='product.wholesaleproductvariant')),
            ],
        ),
        migrations.CreateModel(
            name='OrderEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('type', models.CharField(choices=[('DRAFT_CREATED', 'draft_created'), ('DRAFT_CREATED_FROM_REPLACE', 'draft_created_from_replace'), ('DRAFT_ADDED_PRODUCTS', 'draft_added_products'), ('DRAFT_REMOVED_PRODUCTS', 'draft_removed_products'), ('PLACED', 'placed'), ('PLACED_FROM_DRAFT', 'placed_from_draft'), ('OVERSOLD_ITEMS', 'oversold_items'), ('CANCELED', 'canceled'), ('ORDER_MARKED_AS_PAID', 'order_marked_as_paid'), ('ORDER_FULLY_PAID', 'order_fully_paid'), ('ORDER_REPLACEMENT_CREATED', 'order_replacement_created'), ('ORDER_DISCOUNT_ADDED', 'order_discount_added'), ('ORDER_DISCOUNT_AUTOMATICALLY_UPDATED', 'order_discount_automatically_updated'), ('ORDER_DISCOUNT_UPDATED', 'order_discount_updated'), ('ORDER_DISCOUNT_DELETED', 'order_discount_deleted'), ('ORDER_LINE_DISCOUNT_UPDATED', 'order_line_discount_updated'), ('ORDER_LINE_DISCOUNT_REMOVED', 'order_line_discount_removed'), ('UPDATED_ADDRESS', 'updated_address'), ('EMAIL_SENT', 'email_sent'), ('CONFIRMED', 'confirmed'), ('PAYMENT_AUTHORIZED', 'payment_authorized'), ('PAYMENT_CAPTURED', 'payment_captured'), ('EXTERNAL_SERVICE_NOTIFICATION', 'external_service_notification'), ('PAYMENT_REFUNDED', 'payment_refunded'), ('PAYMENT_VOIDED', 'payment_voided'), ('PAYMENT_FAILED', 'payment_failed'), ('INVOICE_REQUESTED', 'invoice_requested'), ('INVOICE_GENERATED', 'invoice_generated'), ('INVOICE_UPDATED', 'invoice_updated'), ('INVOICE_SENT', 'invoice_sent'), ('FULFILLMENT_CANCELED', 'fulfillment_canceled'), ('FULFILLMENT_RESTOCKED_ITEMS', 'fulfillment_restocked_items'), ('FULFILLMENT_FULFILLED_ITEMS', 'fulfillment_fulfilled_items'), ('FULFILLMENT_REFUNDED', 'fulfillment_refunded'), ('FULFILLMENT_RETURNED', 'fulfillment_returned'), ('FULFILLMENT_REPLACED', 'fulfillment_replaced'), ('TRACKING_UPDATED', 'tracking_updated'), ('NOTE_ADDED', 'note_added'), ('REACHING_PICKUP_POINT', 'reaching_pickup_point'), ('REACHED_PICKUP_POINT', 'reached_pickup_point'), ('PICKED_UP_FROM_PICKUP_POINT', 'picked_up_from_pickup_point'), ('OTHER', 'other')], max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='shop.order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='voucher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='shop.voucher'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(null=True)),
                ('external_url', models.URLField(max_length=2048, null=True)),
                ('invoice_file', models.FileField(upload_to='invoices')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='shop.order')),
            ],
        ),
    ]
