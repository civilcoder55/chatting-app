# Generated by Django 2.2 on 2021-08-26 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0003_remove_conversation_unseen_messages_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='last_message_seen_id',
            field=models.IntegerField(default=0),
        ),
    ]