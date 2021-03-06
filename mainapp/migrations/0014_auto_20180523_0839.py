# Generated by Django 2.0.5 on 2018-05-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.BooleanField(default=True, verbose_name='用户状态'),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='userphoto',
            field=models.ImageField(null=True, upload_to='userphoto'),
        ),
    ]
