# Generated by Django 2.2.16 on 2021-12-02 06:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_auto_20211201_1148'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Following',
            new_name='Follow',
        ),
    ]
