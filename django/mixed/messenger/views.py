from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Dialog,Message
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.middleware.csrf import rotate_token
import socketio
from django.urls import reverse
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger


def getTime(date):
    if date.date() == datetime.today().date() :
        return date.strftime("%H:%M %p")
    else :
        return date.strftime("%Y/%m/%d %H:%M %p")


def getTimestamp(date):
    return date.timestamp()


def getUserChats(user):
    chats = []
    dialogs = Dialog.objects.filter(Q(first=user) | Q(second=user)) #get dialogs which current user is part of it
    for dialog in dialogs :
        lastMessage = dialog.messages.order_by('-time').first()       #get last message data to handle front_end sidebar 
        if lastMessage :
            lastMessageText = lastMessage.text
            lastMessageTime = getTime(lastMessage.time)
            unreadCount = dialog.messages.filter(Q(read=False) & ~Q(sender=user)).count()
            chats.append({dialog : [lastMessageText,lastMessageTime,unreadCount,getTimestamp(lastMessage.time)]}) #it must be that way to handle template render 
    if len(chats) > 0 :
        chats = sorted(chats,key=lambda x: list(x.values())[0][3],reverse=True) # order all last messages from all dialogs by time 
    
    return chats











sio = socketio.Client()
sio.connect('http://chat.backenddev.co',socketio_path='/socket',namespaces=['/django'])

@login_required
def home(request):
    #get user chats 
    chats = getUserChats(request.user)

    #get contacts (in this case all regirsted users )
    contactsList = User.objects.all().exclude(id=request.user.id)
    return render(request,'messenger.html',{'title':'messenger','chats':chats,'contactsList':contactsList})







@login_required
def private(request,id):
    chatWith = User.objects.filter(id=id).first() # the user who the current user chat with 
    if chatWith :
        if request.is_ajax():
            if request.method == 'POST':
                # get the right dialog between current user and who chatting with 
                dialog = Dialog.objects.filter(Q(first=request.user) & Q(second=chatWith)).first()
                if not dialog :
                    dialog = Dialog.objects.filter(Q(first=chatWith) & Q(second=request.user)).first()

                text = request.POST.get('text', None) 
                if text :
                    obj = Message(dialog= dialog , sender = request.user , text = text )
                    obj.save() #save the message to db and emit to nodejs server to emit to online user 
                    sio.emit('new', {'text':text , 'from':request.user.username , 'to' :chatWith.username ,'fromId':request.user.id , 'mid':obj.pk,'fromImage':request.user.profile_pic.pic.url}, namespace='/django')
                    return HttpResponse(200)
                    



        #get users chats as in home view
        chats = getUserChats(request.user)
        




    
        # get contacts as in home view 
        contactsList = User.objects.all().exclude(id=request.user.id)


        # get current chat messages
        if chatWith!= request.user :
            # check if there is a dialog or create
            if Dialog.objects.filter(Q(first=request.user) & Q(second=chatWith)).count() == 0 and Dialog.objects.filter(Q(first=chatWith) & Q(second=request.user)).count() == 0 :
                Dialog(first=request.user,second=chatWith).save()



            # get the right dialog 
            dialog = Dialog.objects.filter(Q(first=request.user) & Q(second=chatWith)).first()
            if not dialog :
                dialog = Dialog.objects.filter(Q(first=chatWith) & Q(second=request.user)).first()


            # we will deliver all unread messages in first patch if they are more than 20 or will will deliver just the first 20 if they less than 20 messages
            unreadMessages = dialog.messages.filter(Q(read=False) & Q(sender=chatWith)).order_by('time')
            allMessages = dialog.messages.all().order_by('time')
            if unreadMessages.count() < 20  :
                messages = list(allMessages)[-20:]
            else:
                messages = unreadMessages
            

            #this is an ajax call to work as pagination to get history messages 
            if request.is_ajax():
                messageId = request.GET.get('mid', None)
                try:
                    int(messageId)
                except Exception :
                    return HttpResponse(404)

                if messageId :
                    history = allMessages.filter(Q(id__lt=messageId))
                    if history.count() > 20 :
                        history = list(history)[-20:]
                        return render(request,'history.html',{'THERE':'true' ,'messages':reversed(history),'chatWithUser':chatWith})
                    else:
                        return render(request,'history.html',{'THERE':'' ,'messages':reversed(history),'chatWithUser':chatWith})
                else:
                     return HttpResponse(404)
                
            if allMessages.count() > 20 :
                THERE = 'true'
            else:
                THERE = 'false'
            return render(request,'private.html',{'title':'messenger','chats':chats,'chatWith':chatWith.username,'THERE':THERE,'messages':messages,'chatWithUser':chatWith,'contactsList':contactsList})
        else:
            return HttpResponseRedirect(reverse('messengerHome'))

    else :
        return HttpResponseRedirect(reverse('messengerHome'))
        




