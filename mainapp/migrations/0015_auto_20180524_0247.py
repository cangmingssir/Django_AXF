# Generated by Django 2.0.5 on 2018-05-24 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20180523_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userpasswd',
            field=models.CharField(max_length=100),
        ),
    ]
