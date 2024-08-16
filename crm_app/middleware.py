# crm_app/middleware.py
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from .models import CustomUser

class SessionExpireMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Middleware processing
        if request.user.is_authenticated:
            session_key = request.session.session_key
           
            if session_key:
                try:
                    session = Session.objects.get(pk=session_key)
                    if session.expire_date < timezone.now():
                        user_id = session.get_decoded().get("_auth_user_id")
                        if user_id:
                            try:
                                user = CustomUser.objects.get(id=user_id)
                                user.is_logged_in = False
                                user.save()
                            except CustomUser.DoesNotExist:
                                pass
                        logout(request)
                except Session.DoesNotExist:
                    pass

        response = self.get_response(request)
        return response
