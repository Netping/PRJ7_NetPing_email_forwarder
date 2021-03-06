"""
SMTP Proxy-server module

Receiving mails and store in DB for processing.
"""

import base64
import logging
import typing
import smtpd
import traceback
from datetime import datetime
import email

from email_forwarder.mails.mailbox import MailBox


def decode_b64(data):
    """Wrapper for b64decode, without having to struggle with bytestrings."""
    byte_string = data.encode('utf-8')
    decoded = base64.b64decode(byte_string)
    return decoded.decode('utf-8')


def encode_b64(data):
    """Wrapper for b64encode, without having to struggle with bytestrings."""
    byte_string = data.encode('utf-8')
    encoded = base64.b64encode(byte_string)
    return encoded.decode('utf-8')


class AuthChannel(smtpd.SMTPChannel):
    def __init__(self, authdata: typing.Tuple[str, str],
                 log: logging.Logger, errors: logging.Logger,
                 server: smtpd.SMTPServer, conn: typing.Tuple[str, int],
                 addr: typing.Optional[typing.Tuple[str, int]],
                 *args, **kwargs):
        super().__init__(server, conn, addr, *args, **kwargs)
        self.username = authdata[0]
        self.password = authdata[1]
        self.authenticated = False
        self.authenticating = False
        self.credential_instance = None
        self.logs = log
        self.errors = errors

    def validate_credential(self, username: str, password: str):
        """
        Validate user

        Args:
            - username -- user login
            - password -- user password
        """
        return (self.username == username and self.password == password)

    def smtp_AUTH(self, arg):
        """
        Handler for AUTH action

        Args:
            - arg -- base64-encoded string AUTH PLAIN\0username\0password
        """
        self.logs.info('Получен запрос AUTH %s', arg)
        if 'PLAIN' in arg:
            split_args = arg.split(' ')
            # second arg is Base64-encoded string of blah\0username\0password
            authbits = decode_b64(split_args[1]).split('\0')
            if self.validate_credential(authbits[1], authbits[2]):
                self.authenticated = True
                self.push('235 Authentication successful.')
            else:
                self.push('454 Temporary authentication failure.')
                self.close_when_done()
        else:
            self.authenticating = False
            self.push('454 Temporary authentication failure.')
            self.close_when_done()

    def smtp_EHLO(self, arg):
        """
        Handler for EHLO action

        Args:
            - arg -- hostname
        """
        self.logs.info('Получен запрос EHLO %s', arg)
        if not arg:
            self.push('501 Syntax: EHLO hostname')
            return
        if self.seen_greeting:
            self.push('503 Duplicate HELO/EHLO')
            return
        self._set_rset_state()
        self.seen_greeting = arg
        self.extended_smtp = True
        self.push('250-%s' % self.fqdn)
        self.push('250-AUTH PLAIN')
        if self.data_size_limit:
            self.push('250-SIZE %s' % self.data_size_limit)
            self.command_size_limits['MAIL'] += 26
        if not self._decode_data:
            self.push('250-8BITMIME')
        if self.enable_SMTPUTF8:
            self.push('250-SMTPUTF8')
            self.command_size_limits['MAIL'] += 10

        self.push('250 HELP')

    # SMTP and ESMTP commands
    def smtp_HELO(self, arg):
        """
        Handler for HELO action

        Args:
            - arg -- hostname
        """
        self.logs.info('Получен запрос HELO %s', arg)
        if not arg:
            self.push('501 Syntax: HELO hostname')
            return
        if self.seen_greeting:
            self.push('503 Duplicate HELO/EHLO')
            return
        self._set_rset_state()
        self.seen_greeting = arg
        self.push('250 %s' % self.fqdn)

    @property
    def allow_args_before_auth(self):
        """
        Available actions before AUTH
        """
        return ['AUTH', 'EHLO', 'HELO', 'NOOP', 'RSET', 'QUIT']


class ProxySMTPServer(smtpd.SMTPServer):
    """
    Proxy SMTP-server
    Receive mails and store them in DB.

    Args:
        - localaddr -- address to bind to.
                       Tuple of host and port.
                       Example, ('127.0.0.1', 8525).
        - authdata -- data authentification users.
                      Tuple of username and password.
                      Example, ('username', 'password').
        - mailbox -- Mailbox object for store mail info in DB.
        - log -- Logger object for logging info and debug messages.
        - errors - - Logger object for logging error messages.
    """
    def __init__(self,
                 localaddr: typing.Tuple[str, int],
                 authdata: typing.Tuple[str, str],
                 mailbox: MailBox,
                 log: logging.Logger,
                 errors: logging.Logger):
        super(ProxySMTPServer, self).__init__(localaddr, None)
        self.channel_class = lambda *args, **kwargs: AuthChannel(
            authdata, log, errors, *args, **kwargs)
        self.mailbox = mailbox
        self.log = log
        self.errors = errors

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        """
        Processing received message.

        Args:
            - peer - the remote host’s address
            - mailfrom -- sender, envelope originator
            - rcpttos -- envelope recipient(s)
            - data -- string containing the contents of the e-mail
        """
        self.log.info('Получено письмо от %s:', peer)
        self.log.info('Отправитель: %s', mailfrom)
        self.log.info('Получатель(-и): %s', rcpttos)
        self.log.info('Сообщение: %s', data.decode())
        meta = dict(kwargs)
        if 'From' not in meta:
            meta['From'] = mailfrom
        if 'To' not in meta:
            meta['To'] = rcpttos
        try:
            msg = email.message_from_string(data.decode(),
                                            policy=email.policy.default)
            for item in msg.items():
                if item[0] not in meta:
                    meta[item[0]] = item[1]
            self.mailbox.new_mail(mailfrom, datetime.now(), meta,
                                  msg.get_content())
        except Exception as e:
            try:
                self.mailbox.new_mail(mailfrom, datetime.now(), meta,
                                      data.decode())
            except Exception:
                pass
            self.errors.error('Ошибка сохранения нового письма: %s', str(e))
            self.errors.error(traceback.format_exc())
