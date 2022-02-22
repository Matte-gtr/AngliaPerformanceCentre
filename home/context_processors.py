from contact.models import Callback, Message
from testimonials.models import Review


def get_notifications_to_context(request):
    """ returns the total number of unread messages,
    callback requests and reviews """
    ur_callbacks = Callback.objects.filter(read=False).count()
    ur_messages = Message.objects.filter(read=False).count()
    ur_reviews = Review.objects.filter(read=False).count()
    total_ur_count = ur_callbacks + ur_messages + ur_reviews
    return {'total_ur_count': total_ur_count}
