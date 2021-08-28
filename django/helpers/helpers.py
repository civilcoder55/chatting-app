from json import dumps
from datetime import datetime


def getTime(date):
    if date.date() == datetime.today().date():
        return date.strftime("%H:%M %p")
    else:
        return date.strftime("%Y/%m/%d %H:%M %p")


def getTimestamp(date):
    return date.timestamp()


def getStrTime(date):
    return date.strftime("%H:%M %p")


def structure_messages(messages):
    messagesList = []
    for message in messages:
        messagesList.append({"id": message.id, "sender_id": message.sender_id , "text": message.text, "time": getStrTime(message.time), "seen": message.seen})
    return dumps(messagesList)

