# Generated by Django 2.0.5 on 2018-05-21 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_topmenu_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='mustbuy',
            fields=[
                ('trackid', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('img', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'axf_mustbuy',
            },
        ),
    ]