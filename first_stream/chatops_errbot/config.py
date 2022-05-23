import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = 'Slack'
# BACKEND = 'Text'  # Errbot will start in text mode (console only mode) and will answer commands from there.

BOT_DATA_DIR = r'/home/beantorong/PycharmProjects/chatops_p4o/data'
BOT_EXTRA_PLUGIN_DIR = r'/home/beantorong/PycharmProjects/chatops_p4o/plugins'

BOT_LOG_FILE = r'/home/beantorong/PycharmProjects/chatops_p4o/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_ALT_PREFIXES = ('Err', '/', '@chatops')
BOT_ALT_PREFIX_SEPARATORS = (',', ';')

BOT_IDENTITY = {
    'token': 'FILL_ME!',
}

BOT_ADMINS = ('@CHANGE_ME', )  # !! Don't leave that to "@CHANGE_ME" if you connect your errbot to a chat system !!
