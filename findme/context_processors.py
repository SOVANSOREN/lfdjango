from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        unread = Notification.objects.filter(
            receiver=request.user,
            is_read=False
        )
        return {
            "notifications": unread[:5],  # latest 5
            "unread_notifications_count": unread.count()
        }
    return {}
