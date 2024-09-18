from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import ChatGroup, ChatMessage, Employee
from asgiref.sync import sync_to_async
from .models import CustomUser
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
import base64
# ------------------------- Single chat added -------------------

from django.utils import timezone

class SingleChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["user"].id
       
        self.user = self.scope["user"]
        
        self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
        self.other_user = await sync_to_async(CustomUser.objects.get)(id=self.other_user_id)
        
        self.room_name = f'{min(self.user_id, self.other_user_id)}_{max(self.user_id, self.other_user_id)}'
        self.room_group_name = f'chat_{self.room_name}'
  

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
            
        )

        

        await self.accept()
       
        print("websocket connected.....")


        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("websocket disconnected",close_code)

   
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        message = text_data_json.get('message', None)
        attachment = text_data_json.get('attachment', None)

        if message:
            chat_message = await database_sync_to_async(ChatMessage.objects.create)(
                message_by=self.user,
                receive_by=self.other_user,
                message=message,
                is_seen=False  # Initially, the message is not seen
            )
        attachment_id = ""   
        attachemt_img=""
        if attachment:
            attachment_data = base64.b64decode(attachment['data'].split(',')[1])  # Decode base64 data
            attachment_file = ContentFile(attachment_data, attachment['filename'])
            
            # Save the attachment to your model (assume you have a field for attachments)
            chat_message = await database_sync_to_async(ChatMessage.objects.create)(
                message_by=self.user,
                receive_by=self.other_user,
                attachment=attachment_file,
                is_seen=False
            )

            attachment_id=chat_message.id
            attachemt_img = chat_message.attachment.url
            
        

        
        
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_by': self.user_id,
                'is_seen': False,  # This will be false until the recipient sees it
                'attachment': attachment ,
                'attachment_id':attachment_id,
                'attachemt_img':attachemt_img,
               
            }
        )



    async def chat_message(self, event):
        message = event['message']
        msg_by = event['message_by']
        attachment = event['attachment']
        is_seen = event.get('is_seen', False)
        msg_id = event['attachment_id']
        attachemt_img = event['attachemt_img']
        print("msg id",msg_id)
        print("attachment image",attachemt_img)
        
        
        await self.send(text_data=json.dumps({
            'message': message,
            'msg_by': msg_by,
            'is_seen': is_seen,
            'attachment': attachment,
            'msg_id': msg_id,
            'attachemt_img': attachemt_img,
        }))
        
    
    async def mark_messages_as_seen(self):
        """Mark unseen messages as seen when the user connects"""
        # Mark messages as seen
        await sync_to_async(ChatMessage.objects.filter(
            message_by=self.other_user,
            receive_by=self.user,
            is_seen=False
        ).update)(is_seen=True)

        # Notify the other user that their messages have been seen
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': '',  # Optional: Only send if needed to trigger an update
                'message_by': self.user_id,
                'is_seen': True,  # Mark the messages as seen
            }
        )


# class SingleChatConsumer(AsyncWebsocketConsumer):
    
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json.get('message', None)
#         attachment = text_data_json.get('attachment', None)

#         # Handle message
#         if message:
#             chat_message = await database_sync_to_async(ChatMessage.objects.create)(
#                 message_by=self.user,
#                 receive_by=self.other_user,
#                 message=message,
#                 is_seen=False  # Initially, the message is not seen
#             )

#         # Handle attachment
#         if attachment:
#             attachment_data = base64.b64decode(attachment['data'].split(',')[1])  # Decode base64 data
#             attachment_file = ContentFile(attachment_data, attachment['filename'])
            
#             # Save the attachment to your model (assume you have a field for attachments)
#             chat_message = await database_sync_to_async(ChatMessage.objects.create)(
#                 message_by=self.user,
#                 receive_by=self.other_user,
#                 attachment=attachment_file,
#                 is_seen=False
#             )

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'message_by': self.user_id,
#                 'is_seen': False,
#                 'attachment': attachment  # Pass attachment info to the group
#             }
#         )



# ------------------------------------- END SINGLE CHAT ------------------



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.group_name = self.scope["url_route"]["kwargs"]["group_id"]
        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print("Message receive from client", text_data)
        data = json.loads(text_data)
        
        if "msg" in data:
            message = data["msg"]
            username = self.user.first_name + " " + self.user.last_name
            group = ChatGroup.objects.get(id=self.group_name)
            chat = ChatMessage(
                message_content=data["msg"], group=group, message_by=self.user
            )
            chat.save()
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {"type": "chat.message", "message": message, "message_by": username},
            )
        elif "attachment" in data:
            # Handle attachments
            attachment = data["attachment"]
            filename = attachment.get("filename", "")
            file_data = attachment.get("data", "")

            # Save the attachment to the database
            group = ChatGroup.objects.get(id=self.group_name)
            chat = ChatMessage(
                group=group,
                message_by=self.user,
                filename=filename,
                attachment=file_data,
            )
            chat.save()

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chat.attachment",
                    "filename": filename,
                    "message_by": self.user.first_name + " " + self.user.last_name,
                    "data": file_data,
                },
            )

    def chat_message(self, event):
       
        self.send(
            text_data=json.dumps(
                {"msg": event["message"], "msg_by": event["message_by"]}
            )
        )

    def chat_attachment(self, event):
        
        self.send(
            text_data=json.dumps(
                {
                    "attachment": {
                        "filename": event["filename"],
                        "msg_by": event["message_by"],
                        "data": event["data"],
                    }
                }
            )
        )

    def disconnect(self, code):
        print("Websocket Disconnected.....", code)


#  --------------------------- Notification ----------------------


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Add the user to the "employees_group" group
        self.employee_id = self.scope["url_route"]["kwargs"]["employee_id"]
        print("helooooo connection...")
        await self.channel_layer.group_add(self.employee_id, self.channel_name)

    async def disconnect(self, close_code):
        # Remove the user from the "employees_group" group
        await self.channel_layer.group_discard(self.employee_id, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]

        # Send the received message to the client
        await self.send(text_data=json.dumps({"message": message}))

    # Custom method to handle notifications
    async def notify(self, event):
        message = event["message"]
        count = event["count"]

        # Send the notification to the client
        await self.send(text_data=json.dumps({"message": message, "count": count}))

    async def assign(self, event):
        message = event["message"]
        count = event["count"]
        notifications = Notification.objects.filter(is_seen=False,is_admin=False).order_by("-id")
        serialized_notifications = serialize('json', notifications)
        print("serailizzee",serialized_notifications)

        # Send the notification to the client
        await self.send(text_data=json.dumps({"message": message, "count": count,"notifications": serialized_notifications}))


class NotificationAgentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Add the user to the "employees_group" group
        self.agent_id = self.scope["url_route"]["kwargs"]["agent_id"]
        print("helooooo connection...")
        await self.channel_layer.group_add(self.agent_id, self.channel_name)

    async def disconnect(self, close_code):
        # Remove the user from the "employees_group" group
        await self.channel_layer.group_discard(self.agent_id, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("Message receive from client", text_data)
        message = text_data_json["message"]

        # Send the received message to the client
        await self.send(text_data=json.dumps({"message": message}))

    # Custom method to handle notifications
    async def notify(self, event):
        message = event["message"]
        count = event["count"]

        # Send the notification to the client
        await self.send(text_data=json.dumps({"message": message, "count": count}))

    async def assign(self, event):
        message = event["message"]
        count = event["count"]

        # Send the notification to the client
        await self.send(text_data=json.dumps({"message": message, "count": count}))

    async def assignop(self, event):
        message = event["message"]
        count = event["count"]

        # Send the notification to the client
        await self.send(text_data=json.dumps({"message": message, "count": count}))


# ------------------------------------------------------------------------

from .models import Notification

# class NotificationAdminConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         # Add the user to the "employees_group" group

#         print("helooooo admin connection...")
#         await self.channel_layer.group_add("admin_group", self.channel_name)

#     async def disconnect(self, close_code):
#         # Remove the user from the "employees_group" group
#         await self.channel_layer.group_discard("admin_group", self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         print("Message receive from client", text_data)
#         message = text_data_json["message"]
#         print("message receive form client",message)

#         # Send the received message to the client
#         await self.send(text_data=json.dumps({"message": message}))

#     # Custom method to handle notifications
#     async def notify_admin(self, event):
#         message = event["message"]
#         count = event["count"]
#         # notif = Notification.objects.get()
#         # print("ssssssssssssss",event["agent_id"])
#         agentID = event["agent_id"]
#         notif_id = ""
#         if agentID:
            
#             notif_id = Notification.objects.get(agent=agentID)
#             print("ooooooooooooo id",notif_id)
        

#         # Send the notification to the client
#         await self.send(text_data=json.dumps({"message": message, "count": count,"notif_id":notif_id}))

from django.core.serializers import serialize
class NotificationAdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("admin_group", self.channel_name)
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_group", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("Message received from client", text_data)
        message = text_data_json["message"]
        print("Message received from client:", message)
       
        await self.send(text_data=json.dumps({"message": message}))

    async def notify_admin(self, event):
        message = event["message"]
        count = event["count"]
        agentID = event["agent_id"]
        notifications = Notification.objects.filter(is_seen=False,is_admin=True).order_by("-id")
        serialized_notifications = serialize('json', notifications)
        print("serailizzee",serialized_notifications)
        

        # Assuming agentID is being used to filter or fetch the Notification object
        notif_id = None
        if agentID:
            try:
                notification = Notification.objects.get(agent=agentID)
                notif_id = notification.id  # Extract the ID only
                print("Notification ID:", notif_id)
            except Notification.DoesNotExist:
                print("Notification does not exist for the given agent.")

        # Send the notification to the client
        await self.send(text_data=json.dumps({
            "message": message,
            "count": count,
            "notifications": serialized_notifications  # Send the ID only
        }))
