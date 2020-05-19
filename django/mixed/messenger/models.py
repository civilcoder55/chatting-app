from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from encrypted_model_fields.fields import EncryptedTextField

class Dialog(models.Model):
    first = models.ForeignKey(User, related_name="Dialogs",on_delete=models.DO_NOTHING)
    second = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return _("Chat ") + self.first.username +_(" & ") + self.second.username





class Message(models.Model):
    dialog = models.ForeignKey(Dialog,related_name="messages", on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(User, verbose_name=_("Author"), related_name="messages",on_delete=models.DO_NOTHING)
    text = EncryptedTextField()
    read = models.BooleanField(verbose_name=_("Read"), default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + "in "+ self.dialog + "(" + str(self.time) + ") - '" + self.text + "'"

