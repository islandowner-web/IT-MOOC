# Generated by Django 2.2 on 2019-12-09 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_auto_20191203_1744'),
        ('courses', '0035_auto_20191209_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Teacher', verbose_name='讲师'),
        ),
    ]
