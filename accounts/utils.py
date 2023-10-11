from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def send_verification_mail(request, user, mail_template, mail_subject):
    from_mail=settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(mail_template, {
                               'user': user,
                               'domain': current_site,
                               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                               'token': default_token_generator.make_token(user)
                               })
    to_mail = user.email
    mail = EmailMessage(mail_subject, message,from_mail, to=[to_mail])
    mail.send()
