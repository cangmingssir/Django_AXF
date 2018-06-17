# Generated by Django 2.0.5 on 2018-05-25 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_auto_20180525_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderState',
            field=models.IntegerField(choices=[(0, '待派送'), (1, '已派送'), (2, '已送达'), (3, '已签售'), (4, '拒收'), (5, '未到达')], default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='payState',
            field=models.IntegerField(choices=[(0, '待支付'), (1, '已支付'), (2, '正在支付中'), (3, '已退款')], default=0),
        ),
    ]