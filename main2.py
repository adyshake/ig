import sys
import os
import csv
import time
from threading import Thread
import sys

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import API
from instabot import Bot



bot = Bot()
bot.login()

#Printing Inbox
def print_inbox():
    inbox = bot.getv2Inbox()
    inbox_json = bot.getLastJSON()
    unseen_count = inbox_json["inbox"]["unseen_count"]
    message_threads = inbox_json["inbox"]["threads"]
    print("Unseen Messages: " + str(unseen_count))
    for user in message_threads:
        print(user["thread_title"] + "\t" + user["thread_id"])
        if((user["items"][0]["item_type"]).encode("utf-8") == "text"):
            print((user["items"][0]["text"]).encode("utf-8"))
        elif((user["items"][0]["item_type"]).encode("utf-8") == "media_share"):
            print("Post by " + (user["items"][0]["media_share"]["user"]["username"]))
        print("")


last_chat_var = "placeholder"

#Printing Margesha's chat
def query_chat_log():
    #time.sleep(3)
    margesha_thread = 340282366841710300949128170938113262944
    personal_thread = bot.SendRequest('direct_v2/threads/{0}'.format(margesha_thread))
    personal_thread = bot.getLastJSON()
    global last_chat_var
    if last_chat_var == bot.getLastJSON():
        print("no change in response")
        pass
    else:
        #Returns a dict
        last_chat_var = bot.getLastJSON()
        personal_thread = personal_thread["thread"]
        other_person_name = personal_thread["users"][0]["username"]
        other_person_id = personal_thread["users"][0]["pk"]

        for message in reversed(personal_thread["items"]):
            if message["user_id"] == other_person_id:
                print(other_person_name)
            else:
                print("Shake!")
            if message["item_type"] == "text":
                print(message["text"])
            elif message["item_type"] == "media":
                print("personal media sent")
            elif message["item_type"] == "link":
                print(message["link"]["text"])
            elif message["item_type"] == "placeholder":
                print(message["placeholder"]["message"])
            elif message["item_type"] == "media_share":
                media_type = "Post"
                if message["media_share"]["media_type"] == 1:
                    media_type = "Photo"
                elif message["media_share"]["media_type"] == 2:
                    media_type = "Video"
                caption = message["media_share"]["caption"]
                try:
                    caption = caption["text"].encode("utf-8")
                except:
                    caption = "null"
                print(media_type + " by " + message["media_share"]["user"]["username"])
                print("Caption: " + caption)
            print("")
        pass


def send_message():
    chat_to_send = str(raw_input("Enter your text"))
    ig_user=["margesha_devlekar"]
    message_to_send=[]
    message_to_send.append(chat_to_send)
    bot.send_messages(message_to_send, ig_user)

while True:
    print("1. check log")
    print("2. send message")
    choice = int(raw_input(""))
    if(choice == 1):
        query_chat_log()
    elif(choice == 2):
        send_message()
