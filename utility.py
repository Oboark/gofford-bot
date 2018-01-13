"""
Contains utility functions for moderation
"""

from datetime import datetime

def log(user='nAn', channel='nAn', content='nAn'):
    """Print logs with username, channel and content"""
    date = str(datetime.now())
    print('[{} by {} in {}] {}'.format(date, user, channel, content))
