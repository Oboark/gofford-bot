"""
Contains utility functions for moderation
"""

from datetime import datetime

def log(user='nAn', channel='nAn', server='nAn', content='nAn'):
    """Print logs with username, channel and content"""
    date = str(datetime.now())
    print('[{} by {} in {} from {}] {}'.format(date, user, channel, server, content))
