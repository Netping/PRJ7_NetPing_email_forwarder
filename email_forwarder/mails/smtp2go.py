"""
Module for send mails via https://www.smtp2go.com
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .sender import Sender

class SMTP2GO(Sender):
    """
    Class for send email via https://www.smtp2go.com

    Args:
        - host -- server address, usually mail.smtp2go.com
        - port -- server port, usually 25, 587, 2525 or 8025
        - username -- username for connect to smtp2go
        - password -- password for connect to smtp2go
        - logs -- logger for info/debug messages
        - errors -- logger for errors
    """
    def __init__(self, host: str, port: int, username: str, password: str,
                 logs: logging.Logger, errors: logging.Logger):
        super(SMTP2GO, self).__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logs = logs
        self.errors = errors

    def send(self, sender: str, recipient: str, subject: str, body: str):
        """
        Send message to recipient

        Args:
            - sender -- sender email
            - recipient -- recipiet email
            - subject -- subject text
            - body -- mail content in html
        """
        msg = MIMEMultipart('mixed')

        html_message = MIMEText(body, 'html')

        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        if isinstance(recipient, list):
            msg['To'] = ','.join(recipient)
        else:
            msg['To'] = recipient
        msg.attach(html_message)

        mailServer = smtplib.SMTP(self.host, self.port)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.username, self.password)
        mailServer.sendmail(sender, recipient, msg.as_string())
        mailServer.close()
        return msg.items()
