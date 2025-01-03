from .models import FAQ, Notification

def faq_count(request):
    if request.user.is_authenticated:
        count = (
            FAQ.objects.filter(answer__exact="").exclude(answer__isnull=True).count()
        )
    else:
        count = 0
    return {"faq_count": count}



def current_login(request):
    if request.user and request.user.is_authenticated:
        if request.user.user_type == "4":
            user = request.user
            agent_id = user.agent.id
            notification = Notification.objects.filter(
                agent=agent_id, is_seen__in=[False]
            ).order_by("-id")
            notification_Count = Notification.objects.filter(
                agent=agent_id, is_seen__in=[False]
            ).count()

            return {
                "agent_id": agent_id,
                "notification": notification,
                "notification_Count": notification_Count,
            }
        elif request.user.user_type == "5":
            user = request.user
            agent_id = user.outsourcingagent.id
            notification = Notification.objects.filter(
                outsourceagent=agent_id, is_seen__in=[False]
            ).order_by("-id")
            notification_Count = Notification.objects.filter(
                outsourceagent=agent_id, is_seen__in=[False]
            ).count()

            return {
                "agent_id": agent_id,
                "notification": notification,
                "notification_Count": notification_Count,
            }
        elif request.user.user_type == "3":
            user = request.user
            emp_idd = user.employee.id
            notification = Notification.objects.filter(employee=emp_idd,is_seen=False,is_admin=False).order_by("-id")
            # notification = Notification.objects.filter(
            #     employee=emp_idd, is_seen__in=[False]
            # ).order_by("-id")
            notification_Count = Notification.objects.filter(
                employee=user.employee, is_seen=False,is_admin=False
            ).count()
            print("NO...............",notification)

            return {
                "emp_idd": emp_idd,
                "notification": notification,
                "notification_Count": notification_Count,
            }

        elif request.user.user_type == "2":
            
            user = request.user

            
            notification = Notification.objects.filter(is_seen=False,is_admin=True).order_by("-id")
            
            notification_Count = Notification.objects.filter(is_seen=False,is_admin=True).count()
            print("notificationsss counts::",notification_Count)
            return {
                "notification": notification,
                "notification_Count": notification_Count,
            }

           
            
    return {}
    
