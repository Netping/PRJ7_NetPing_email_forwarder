from config import VERSION, get_parser


if __name__ == '__main__':
    config = get_parser(f'NetPIng Email forwarder v.{VERSION}, Tasks.',
                        ('user_db', 'admin_db', 'smtp2go')).parse_args()
