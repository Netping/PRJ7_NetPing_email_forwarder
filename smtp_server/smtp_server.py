from smtpd import SMTPChannel, SMTPServer


class ProxySMTPServer(SMTPServer):
    def __init__(self, authdata, localaddr, remoteaddr):
        super(PureProxy, self).__init__(*args, **kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data):
        pass
