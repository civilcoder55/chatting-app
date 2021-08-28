import socketio
import json
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Conversation,Participation,Message
from django.db.models import Q
from users.models import User
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.urls import reverse
from helpers import helpers
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache





 


socket_host = os.environ.get("SOCKET_HOST",'http://127.0.0.1:3000')
sio = socketio.Client()
sio.connect(socket_host,socketio_path='socket',namespaces=["/internal"])


@login_required
def home(request,exception=False):
    conversations = request.user.get_conversations()
    contacts = request.user.get_contacts()
    return render(request,'messenger.html',{'title':'messenger','conversations':conversations,'contacts':contacts})





class PrivateView(LoginRequiredMixin,View):
    def get(self,request,id):
        chat_with = User.objects.filter(id=id).first()
        if chat_with and chat_with.id != request.user.id :
            participation = Participation.objects.getOrCreate(user=request.user,with_user=chat_with)
            conversation = participation.conversation
            conversations = request.user.get_conversations()
            contacts = request.user.get_contacts()
            unseen_messages_count = cache.get(f'_count_{participation.id}') or 0
            messages = list(conversation.messages.all())[-20:] if unseen_messages_count < 20 else conversation.messages.filter(Q(id__gt=participation.last_message_seen_id - 5))
            messagesList = helpers.structure_messages(messages)
            return render(request,'private.html',{'title':'messenger','conversations':conversations,'contacts':contacts,'conversationID':conversation.id,'chatWith':chat_with.jinfo,'messages':messagesList,
            })
        else:
            return HttpResponseRedirect(reverse('messengerHome'))

    def post(self, request,id):
        chat_with = User.objects.filter(id=id).first()
        if chat_with:
            participation = Participation.objects.getOrCreate(user=request.user,with_user=chat_with)
            conversation = participation.conversation
            data = json.loads(request.body.decode('utf-8'))
            if data['text'] :
                obj = Message(conversation= conversation , sender = request.user , text = data['text'])
                obj.save()
                Conversation.objects.filter(id=conversation.id).update(last_message=obj.text,last_message_time=obj.time)
                sio.emit('broadcastMessage', {'id':obj.pk,'conversationID':conversation.id,'text':obj.text , 'from':request.user.info, 'to' : chat_with.info,"time":obj.getStrTime(),'timeStamp':obj.getTimestamp()}, namespace='/internal')
                return JsonResponse({})
        return HttpResponse(404)


@login_required        
def history(request,id):
    chat_with = User.objects.filter(id=id).first()
    if chat_with and chat_with != request.user :
        participation = Participation.objects.getOrCreate(user=request.user,with_user=chat_with)
        conversation = participation.conversation
        data = json.loads(request.body.decode('utf-8'))
        try:
            messageId = int(data['beforeID'])
        except Exception :
            return HttpResponse(404)

        if messageId :
            old_messages = conversation.messages.all().filter(Q(id__lt=messageId))
            if old_messages.count() > 20 :
                old_messages = list(old_messages)[-20:]
                pagination = 'true'
            else:
                pagination = 'false'
            return JsonResponse({'pagination':pagination ,'messages':helpers.structure_messages(old_messages)})
        
    return HttpResponse(404)
        




