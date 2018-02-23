"""
Contains utility functions for moderation and server settings
"""

from datetime import datetime
import json
import discord


def log(user='nAn', channel='nAn', server='nAn', content='nAn'):
    """Print logs with username, channel and content"""
    date = str(datetime.now())
    log = '[{} by {} in {} from {}] {}'.format(date, user, channel, server, content)
    
    #Print log
    print(log)

    #Append to log file
    with open("data/server.log", "a") as f:
        f.write(log + '\n')


def write_message(message):
    """Writes message data to file"""

    new_message = {}
    new_message[str(message.id)] = []
    new_message[str(message.id)].append({
        'u': message.author.name,
        'c': message.content,
        't': message.timestamp.strftime('%m/%d/%Y/%H/%M/%S')
    })

    with open('data/messages.json') as f:
        messages = json.load(f)

    messages.update(new_message)

    with open('data/messages.json', 'w') as f:
        json.dump(messages, f, indent=4)


def authorized(user):
    """Checks if a user is authorized"""
    auth = False
    for r in user.roles:
        if r.permissions.administrator:
            auth = True

    return auth
