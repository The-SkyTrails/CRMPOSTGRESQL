# notification_utils.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def create_notification(employee, message,lead_id=None):
    notification = Notification.objects.create(
        employee=employee,
        name=message,
        lead_id=lead_id,
        is_seen=False,
    )
    notification.save()


def create_notification_agent(agent_id, message):
    notification = Notification.objects.create(
        agent=agent_id,
        name=message,
        is_seen=False,
    )
    notification.save()


def create_notification_outsourceagent(outsourcepartner, message):
    notification = Notification.objects.create(
        outsourceagent=outsourcepartner,
        name=message,
        is_seen=False,
    )
    notification.save()


def send_notification(employee_id, message, current_count):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(employee_id),
        {"type": "notify", "message": message, "count": current_count},
    )


def assign_notification(agent_id, message, current_count):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(agent_id),
        {"type": "assign", "message": message, "count": current_count},
    )


def assignop_notification(agent_id, message, current_count):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(agent_id),
        {"type": "assignop", "message": message, "count": current_count},
    )


def create_admin_notification(message,lead_id=None, agent_id=None,outsourceagent_id=None):
    notification = Notification.objects.create(
        name=message,
        is_seen=False,
        lead_id=lead_id,
        agent_id=agent_id,
        outsourceagent_id=outsourceagent_id,
    )
    notification.save()


def send_notification_admin(message, current_count,agent_id=None):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "admin_group",
        {"type": "notify_admin", "message": message, "count": current_count,"agent_id":agent_id},
    )
