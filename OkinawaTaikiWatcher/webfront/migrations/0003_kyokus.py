# Generated by Django 4.2.6 on 2023-12-10 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webfront', '0002_settings_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kyokus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', max_length=20)),
                ('alert_flg', models.BooleanField(default=True)),
                ('registed_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
