# Generated by Django 2.2 on 2019-11-20 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20191019_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否广告位'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图'),
        ),
    ]
