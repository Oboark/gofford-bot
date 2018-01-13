#!/usr/bin/env python

"""
gofford-bot source code
"""

import discord
import asyncio
import goodnatt as gnatt
import random
import shlex
import sys
from utility import log

__author__ = "Oboark"
__version__ = "1.0.1"

client = discord.Client()

#Bot variables
presence = 'you yoo'
help_string = """
**ahh!! here is some help:

`!goodnatt [number of emojis]` - Sends a bunch of wholesome emojis :sparkling_heart:
`!sponge [text]` - i aM A fuCkinG dEGenErate :100:
`!purge [num of messages] [specified string]` - Deletes a bunch of messages (you gotta be authorized to use this) :no_good::skin-tone-2:
`gofford, [thing] or [other thing] or [other other thing]` - Make me decide!
`!8ball [query]` - summon the 8ball
**
"""
authorized_roles = ['399702651278983168', '399702073924517888']


@client.event
async def on_ready():
    """Do something on startup"""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    #Change the bot presence to 'presence'
    await client.change_presence(game=discord.Game(name=presence))


@client.event
async def on_message(message):
    """Do something on message"""

    #Handle commands
    if message.content.startswith('!help'):
        await help(message)
    elif message.content.startswith('!goodnatt'):
        await goodnatt(message)
    elif message.content.startswith('!sponge'):
        await sponge(message)
    elif message.content.startswith('!purge'):
        #Check if user is authorized
        auth = False
        for r in message.author.roles:
            if r.id in authorized_roles:
                auth = True
                
        if auth:
            #If so, do the procedure
            #add deleting 
            await client.send_message(message.channel, ":white_check_mark:")
            c = shlex.split(message.content)
            try:
                n = int(c[1])
                s = c[2]
                log(message.author.name, message.channel.name, "**Deleting {} messages containing '{}'...**".format(n, s))
                await purge(message, n, s)
            except IndexError:
                try:
                    n = int(c[1])
                    log(message.author.name, message.channel.name, "**Deleting {} messages...**".format(n))
                    await purge(message, n)
                except IndexError:
                    log(message.author.name, message.channel.name, "**Deleting {} messages...**".format(10))
                    await purge(message)
        else:
            #If not, send a message indicating they aren't authorized
            await client.send_message(message.channel, ":no_good::skin-tone-2:")
    elif message.content.startswith('wherest mein gofford'):
        await client.send_message(message.channel, ':sunflower:')
        await client.send_message(message.channel, 'i am here uwu')
    elif message.content.startswith('gofford, '):
        if ' or ' in message.content:
            #Made for the decision function
            await client.send_message(message.channel, await decide(message) + '?')
        elif ' lov' in message.content:
            #Made for something like "gofford, i love you!"
            await client.send_message(message.channel, "i lomv you too!!")
            await client.send_message(message.channel, ":sparkling_heart:")
    elif message.content == 'gofford':
        await client.send_message(message.channel, "heb?")
    elif message.content.startswith('!8ball'):
        p = ['It is certain', 'It is decidedly so', 'Without a doubt', 
                        'Yes definitely', 'You may rely on it', 'As I see it, yes',
                        'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 
                        'Reply hazy try again', 'Ask again later', 'Better not tell you now',
                        'Cannot predict now', 'Concentrate and ask again', 'Dont count on it',
                        'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
        
        await client.send_message(message.channel, ":8ball:")
        await client.send_message(message.channel, random.choice(p))

@client.event
async def on_member_join(member):
    """Do something when somebody joins the server"""
    #Assign normie role to new user
    role = discord.utils.get(member.server.roles, name='normie')
    await client.add_roles(member, role)
    log(member.name, 'general', "Assigned normie role to user {}".format(member.name))


async def help(message):
    """Sends help"""
    await client.send_message(message.channel, help_string)


async def goodnatt(message):
    """Sends a bunch of wholesome emojis"""
    try:
        #Try to get number of emojis specified
        n = int(shlex.split(message.content)[1])
        #Send message with n emojis
        await client.send_message(message.channel, gnatt.goodnatt(gnatt.emoji_list, n))
    except Exception:
        #Else, send a message anyways with 10 emojis (default)
        await client.send_message(message.channel, gnatt.goodnatt(gnatt.emoji_list, 10))


async def sponge(message):
    """gEnErATEs SpONge TeXt aND SEnds iT"""
    #Randomize message capitalization
    sponge_text = "".join(random.choice([k.upper(), k ]) for k in message.content[7:])
    #Send the messages
    if sponge_text: 
        await client.send_message(message.channel, sponge_text)
    await client.send_file(message.channel, 'assets\sponge.jpg')


async def purge(message, num_msgs=10, s=""):
    """Deletes a bulk of messages"""

    #Empty list to store the messages we will be deleting
    msgs = []
    #Collect messages
    async for x in client.logs_from(message.channel, limit = num_msgs):
        #Check if message contains specified string, if so, add to our soon-to-be-deleted-messages
        if s in x.content:
            msgs.append(x)
    
    await client.delete_messages(msgs)


async def decide(message):
    """Decides randomly based on user's query"""
    
    a = message.content.split()
    b = []
    for i in a:
        if not i in ['gofford,', 'or']:
            i = i.strip('?')
            b.append(i)
        
    return random.choice(b)


if __name__ == '__main__':
    token = sys.argv[1] if len(sys.argv) > 1 else sys.exit(0)
    client.run(str(token))
