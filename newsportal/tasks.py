from celery import shared_task
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@shared_task()
def send_weekly_mail():
    current_date = datetime.today()
    previous_date = current_date - timedelta(days=7)
    messages = []
    text_body = []
    users = User.objects.all()
    for user in users:
        posts = Post.objects.filter(category__in=user.category_set.all(), date__gte=previous_date,
                                    date__lte=current_date)
        for post in posts:
            message = {'header': post.header, 'text': post.text, 'id': post.id}
            messages.append(message)
            text_body.append(post.text[:50])

        html_content = render_to_string('weekly_mail.html',
                                        {'username': user.username, 'messages': messages})
        msg = EmailMultiAlternatives(
            subject='Новые статьи за неделю в твоих любимых разделах!',
            from_email='appointment@silicon-chronicles.ru',
            body='\n'.join(text_body),
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task()
def send_new_article_mail(post_id):
    mail_dict = {}
    instance = Post.objects.get(pk=post_id)
    categories = instance.category.all()
    for category in categories:
        for user in category.subscribers.all():
            mail_dict[user.username] = user.email

    for username, email in mail_dict.items():
        html_content = render_to_string('mail.html',
                                        {'header': instance.header, 'username': username, 'text': instance.text,
                                         'id': instance.id})
        msg = EmailMultiAlternatives(
            subject=instance.header,
            from_email='appointment@silicon-chronicles.ru',
            body=instance.text,
            to=[email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
