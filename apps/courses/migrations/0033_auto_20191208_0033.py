# Generated by Django 2.2 on 2019-12-08 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0032_auto_20191208_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursehomeworkdetail',
            name='name',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='courses.CourseHomework', verbose_name='所属作业'),
        ),
    ]
