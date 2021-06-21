from flask import render_template
from flask_mail import Message
from config import Config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail.mime_type import MimeType

from . import mail


def mail_message(subject, template, to, context):
    mailer = SendgridMailer()
    message = mailer.create_mail([to], subject,"email/welcome_user.html", context, template_type="text/html")
    mailer.send(message)

class SendgridMailer:

    def __init__(self,app=None):
        self.client= SendGridAPIClient(Config.SENDGRID_API_KEY)

    def create_mail(self,tos, subject, template,context, template_type="text/html",sender=None):
        if sender==None:
            sender = Config.DEFAULT_SENDGRID_SENDER
        html_content, text_content= None, None
        if template_type=="all":
            html_content = render_template(template, **context)
            text_content  =  render_template(template, **context)
        elif template_type=="text/html":
            html_content= render_template(template, **context)

        elif template_type=="text/plain":
            text_content = render_template(template, **context)
        else:
            raise ValueError("Invalid Content Type")
        message = Mail(
            from_email=sender, to_emails=tos, subject=subject,
        )

        if html_content:
            message.add_content(html_content, MimeType.html)
        if text_content:
            message.add_content(text_content, MimeType.text)
        return message

    def send(self, message):
        response = self.client.send(message)
        print(response.headers)


