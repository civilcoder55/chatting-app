from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from json import dumps
from django.db.models import Q
from django.core.cache import cache

class User(AbstractUser):
    avatar = models.ImageField(default='avatars/default.jpg',upload_to='avatars')

    

    def __str__(self):
        return self.user.username

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar :
            img = Image.open(self.avatar.path)
            if img.height > 100 or img.width > 100:
                output_size = (100, 100)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    @property
    def info(self):
        return {"id" : self.id ,"username":self.username,"avatar" : f"/users{self.avatar.url}"}
    
    @property
    def jinfo(self):
        return dumps(self.info)
        

    def get_conversations(self):
        conversations = []
        participations = self.participations.all().select_related('conversation').select_related('with_user')
        for participation in participations :
            conversation = participation.conversation
            lastMessage = conversation.last_message
            if len(lastMessage) > 0 :
                lastMessageTime = conversation.last_message_StrTime()
                lastMessageTimeStamp = conversation.last_message_timestamp()
                unseen_messages_count = conversation.messages.filter(Q(seen=False) & Q(sender=participation.with_user) & Q(id__gt=participation.last_message_seen_id)).count()
                cache.set(f'_count_{participation.id}',unseen_messages_count)
                conversations.append({"id":conversation.id,"with" : participation.with_user.info ,"lastMessageText":lastMessage,"lastMessageTime":lastMessageTime,
                "unreadCount":unseen_messages_count,"lastMessageTimeStamp":lastMessageTimeStamp})
        if len(conversations) > 0 :
            conversations = sorted(conversations,key=lambda x: x["lastMessageTimeStamp"],reverse=True)
        
        return dumps(conversations)

    
    def get_contacts(self):
        contacts = User.objects.all().exclude(id=self.id)
        contactsList = []
        for contact in contacts:
            contactsList.append(contact.info)
        return dumps(contactsList)