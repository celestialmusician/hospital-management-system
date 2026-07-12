

import string

import random

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from decouple import config

def send_email(subject, otp, recipient):

    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                padding: 30px;
            }}

            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 5px 20px rgba(0,0,0,.1);
            }}

            .header {{
                background: #0d6efd;
                color: white;
                padding: 20px;
                text-align: center;
            }}

            .content {{
                padding: 30px;
            }}

            .otp {{
                font-size: 32px;
                font-weight: bold;
                text-align: center;
                background: #eef5ff;
                color: #0d6efd;
                padding: 20px;
                border-radius: 10px;
                letter-spacing: 6px;
                margin: 20px 0;
            }}

            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 14px;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <div class="header">

                <h2>🏥 HealthCare Hospital</h2>

            </div>

            <div class="content">

                <h3>Hello,</h3>

                <p>

                    Your One-Time Password (OTP) for login is:

                </p>

                <div class="otp">

                    {otp}

                </div>

                <p>

                    This OTP is valid for 5 minutes.

                </p>

                <p>

                    If you didn't request this OTP,
                    simply ignore this email.

                </p>

            </div>

            <div class="footer">

                © 2026 HealthCare Hospital

            </div>

        </div>

    </body>

    </html>
    """

    message = EmailMultiAlternatives(
        subject,
        f"Your OTP is {otp}",
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
    )

    message.attach_alternative(html_message, "text/html")

    message.send()