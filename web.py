from config import VERSION, get_parser


if __name__ == '__main__':
    config = get_parser(f'NetPIng Email forwarder v.{VERSION}, WEB.',
                        ('user_db', 'admin_db', 'web')).parse_args()
