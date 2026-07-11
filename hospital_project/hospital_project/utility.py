

import string

import random

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from decouple import config

def generate_otp():

    otp = ''.join(random.choices(string.digits,k=4))

    return otp



def send_email(recipient,template,subject,context):

    sender = config('EMAIL_HOST_USER')

    content = render_to_string(template,context)

    msg = EmailMultiAlternatives(from_email=sender,to=[recipient],subject=subject)

    msg.attach_alternative(content,'text/html')

    msg.send()