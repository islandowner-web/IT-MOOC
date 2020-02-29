# Generated by Django 2.2 on 2019-12-07 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_order_add_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '课程订单', 'verbose_name_plural': '课程订单'},
        ),
        migrations.AlterField(
            model_name='order',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程名'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=64, verbose_name='订单号'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(choices=[(0, '未支付'), (1, '已支付')], default=0, verbose_name='支付状态'),
        ),
        migrations.AlterField(
            model_name='order',
            name='userid',
            field=models.CharField(max_length=60, verbose_name='用户编号'),
        ),
    ]