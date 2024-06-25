from . import consumers
from django.urls import path, re_path

websocket_urlpatterns = [
    path('ws/chat/single/<int:other_user_id>/', consumers.SingleChatConsumer.as_asgi()),
    path("ws/chat/<str:group_id>/", consumers.ChatConsumer.as_asgi()),
    path(
        "ws/notifications/<str:employee_id>/", consumers.NotificationConsumer.as_asgi()
    ),
    path(
        "ws/Agent/notifications/<str:agent_id>/",
        consumers.NotificationAgentConsumer.as_asgi(),
    ),
    path(
        "ws/Admin/notifications/",
        consumers.NotificationAdminConsumer.as_asgi(),
    ),
]
