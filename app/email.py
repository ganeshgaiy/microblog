"""Encapsulates an email message.

    :param subject: email subject header
    :param recipients: list of email addresses
    :param body: plain text message
    :param html: HTML message
    :param sender: email sender address, or **MAIL_DEFAULT_SENDER** by default
    :param cc: CC list
    :param bcc: BCC list
    :param attachments: list of Attachment instances
    :param reply_to: reply-to address
    :param date: send date
    :param charset: message character set
    :param extra_headers: A dictionary of additional headers for the message
    :param mail_options: A list of ESMTP options to be used in MAIL FROM command
    :param rcpt_options:  A list of ESMTP options to be used in RCPT commands
"""
from app import app,mail
from flask_mail import Message
from flask import render_template
from threading import Thread

def send_async_email(app,message):
    with app.app_context():
        mail.send(message)


def send_pass_request_email(user):
	#send the email with the token
	token = user.get_reset_password_token()
	message = Message(subject='Flask Blog Password reset',recipients=[user.email],sender=app.config['MAIL_DEFAULT_SENDER'])
	message.body = render_template('email/reset_password.txt',user=user,token=token)
	message.html = render_template('email/reset_password.html',user=user,token=token)
	Thread(target=send_async_email,args=(app,message)).start()
