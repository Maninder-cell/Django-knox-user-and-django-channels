# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def fetch_message(self,data):
        messages = Message.last_10_message()
        content = {
            "command" : "messages",
            "messages" : self.convert_to_all_json(messages)
        }
        self.send_fetch_messages(content)

    def convert_to_all_json(self,data):
        result = []
        for i in data:
            result.append(self.convert_to_json(i))
        return result

    def convert_to_json(self,data):
        return {
            "user" : data.user.username,
            "content" : data.content,
            "created" : str(data.created)
        }

    def new_message(self,data):
        msg = Message.objects.create(user = User.objects.get(pk=3), content = data["message"])
        content = {
            "command" : "new_message",
            "message" : self.convert_to_json(msg)
        }
        
        self.send_message(content)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = self.commands[text_data_json["commands"]](self,text_data_json)


    def send_message(self,messages):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': messages
            }
        )

    def send_fetch_messages(self,messages):
        self.send(text_data=json.dumps(messages))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
       
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
    
    commands = {
        "fetch_msg" : fetch_message,
        "new_message" : new_message
    }