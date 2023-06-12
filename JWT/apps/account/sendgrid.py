from django.core.mail import EmailMessage
import os
from JWT import settings
import requests
import json


def send_sendgrid_mail(payload):
    r = requests.request(
        "POST",
        url=settings.SENDGRID_URL,
        data=json.dumps(payload),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
        },
    )
    print(r.status_code, type(r.status_code))
    if r.status_code in [200, 201, 202]:
        return r.status_code
    else:
        return r.json()


class SendGrid:
    def send_email_to_user_for_reset_password(self, email, reset_password_link):
        payload = {
            "from": {"email": settings.FROM_EMAIL},
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {
                        "forget_password_link": reset_password_link,
                    },
                },
            ],
            "template_id": settings.INVITE_USER_TEMPLATE_ID,
        }
        send_sendgrid_mail(payload=payload)

    def send_email_to_user_for_otp_login(self, email, otp):
        payload = {
            "from": {"email": settings.FROM_EMAIL},
            "personalizations": [
                {
                    "to": [{"email": email}],
                    "dynamic_template_data": {
                        "otp": otp,
                    },
                },
            ],
            "template_id": settings.SENT_OTP_USER_TEMPLATE_ID,
        }
        return send_sendgrid_mail(payload=payload)
