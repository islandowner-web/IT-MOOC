# Generated by Django 2.2 on 2019-10-17 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20191017_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notice',
            field=models.CharField(default='', max_length=300, verbose_name='课程公告'),
        ),
    ]
