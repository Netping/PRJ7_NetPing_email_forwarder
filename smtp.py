from config import VERSION, get_parser


if __name__ == '__main__':
    config = get_parser(f'NetPIng Email forwarder v.{VERSION}, SMTP-Proxy server.',
                        ('user_db', 'smtp')).parse_args()
