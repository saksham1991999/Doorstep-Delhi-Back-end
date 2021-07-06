# Generated by Django 3.2.4 on 2021-07-06 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='description_hi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='title_hi',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]