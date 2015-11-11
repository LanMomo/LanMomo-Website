DEBUG = True
WEB_ROOT = 'http://localhost:5000/#'
DATABASE_URI = 'sqlite:////tmp/lanmomo-test.db'
SECRET_KEY = 'secret'
SERVER_TOKEN = 'SECRET'  # Used for notifier

# Mailgun
MAILGUN_USER = 'no-reply@lanmomo.org'
MAILGUN_DOMAIN = 'lanmomo.org'

# Lanmomo
TYPE_IDS = {'pc': 0, 'console': 1}
TICKETS_MAX = {TYPE_IDS['pc']: 96, TYPE_IDS['console']: 32}
PRICING = {TYPE_IDS['pc']: 20, TYPE_IDS['console']: 10}
DISCOUNT_MOMO = 5
LOG_PATH = 'test.log'
