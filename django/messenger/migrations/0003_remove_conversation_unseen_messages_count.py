# Generated by Django 2.2 on 2021-08-25 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_auto_20210825_0134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='unseen_messages_count',
        ),
    ]
