# Generated by Django 2.2 on 2019-12-13 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0008_auto_20191212_0202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermessage',
            name='has_read',
        ),
    ]