# Generated by Django 4.0.3 on 2022-03-26 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_departure'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='arrival',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='departure',
            field=models.CharField(max_length=50, null=True),
        ),
    ]