from django.db import models
from users.models import User
from datetime import datetime
from django.core.cache import cache
#===========================for dockerizing reason =====================#
from django.core.management.base import BaseCommand
BaseCommand.requires_system_checks = False
#=======================================================#

class ParticipationManager(models.Manager):
    def getOrCreate(self,user,with_user):
        participation = cache.get_or_set(f'_participation_{user.id}_{with_user.id}',self.filter(user=user,with_user=with_user).select_related('conversation').first)
        if not participation :
            conversation = Conversation.objects.create()
            participation = self.create(user=user,with_user=with_user,conversation=conversation)
            self.create(user=with_user,with_user=user,conversation=conversation)
        return participation








class Conversation(models.Model):
    last_message = models.TextField()
    last_message_time = models.DateTimeField()


    def last_message_StrTime(self):
        if self.last_message_time.date() == datetime.today().date():
            return self.last_message_time.strftime("%I:%M %p")
        else:
            return self.last_message_time.strftime("%Y/%m/%d %I:%M %p")


    def last_message_timestamp(self):
        return self.last_message_time.timestamp() 


class Participation(models.Model):
    user = models.ForeignKey(User,related_name="participations",on_delete=models.CASCADE)
    with_user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE)
    last_message_seen_id = models.IntegerField(default=0)
    objects = ParticipationManager()


    
    


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    text = models.TextField()
    seen = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)


    def getTimestamp(self):
        return self.time.timestamp()


    def getStrTime(self):
        return self.time.strftime("%I:%M %p")

    


