from mohan.celery import app
import datetime
from .models import purchase_orders

from django.core.mail import send_mail
from django.conf import settings

@app.task(name='send_notification')
def send_notification():
    try:
        time_thresold = datetime.now() - datetime.timedelta(days=30)

        pr_objs = purchase_orders.objects.filter(remaining__gt=1, date__gte=time_thresold)

        rem = []
        for pr_obj in pr_objs:
            rem.append(pr_obj.PR_no)
            return rem
            
        subject = 'PR with more than 30 days'
        message = rem
        email_from = settings.EMAIL_HOST_USER
        recipient_list = 'tibarek90@gmail.com'
        send_mail(subject, message, email_from, recipient_list)

    except Exception as e:
        print(e)


