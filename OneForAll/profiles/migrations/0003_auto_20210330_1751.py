# Generated by Django 3.1.2 on 2021-03-30 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_relationship'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profiles',
            old_name='username',
            new_name='user',
        ),
    ]
