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
from utility import log, read_settings, write_settings
from emoji import to_emoji

__author__ = "Oboark"
__version__ = "1.0.3"

client = discord.Client()

#Bot variables
authorized_users = ["340140981586493442", "398191324685402112"] #Developer users who can change global settings/use global commands
presence = 'you woo'
help_string = """
**ahh!! here is some help:

`gofford, [thing] or [other thing] or [other other thing]` - Make me decide!
`!goodnatt [number of emojis]` - Sends a bunch of wholesome emojis :sparkling_heart:
`!sponge [text]` - i aM A fuCkinG dEGenErate :100:
`!8ball [query]` - summon the 8ball :8ball:
`!emojify [text]` :regional_indicator_e: :regional_indicator_m: :regional_indicator_o: :regional_indicator_j: :regional_indicator_i: :regional_indicator_f: :regional_indicator_y:     :regional_indicator_t: :regional_indicator_e: :regional_indicator_x: :regional_indicator_t:

moderator stuff: (you gotta be authorized to use this) :no_good::skin-tone-2:
`!purge [num of messages] [specified string]` - Deletes a bunch of messages
`!defaultrole [default role]` - Sets the default role of the server (Be CaSe SenSiTiVe!)

developer stuff: (you gotta be SUPER authorized to use this) :no_entry_sign: :no_good::skin-tone-4: :no_entry_sign:
`!presence [presence]` - Sets the 'Playing....' thing

my inner workings:
https://github.com/Oboark/gofford-bot
v{}
**
""".format(__version__)

@client.event
async def on_ready():
    """Do something on startup"""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(__version__)
    print('------')

    #Change the bot presence to 'presence'
    await client.change_presence(game=discord.Game(name=presence))


@client.event
async def on_member_join(member):
    """Do something when somebody joins the server"""

    #Assign normie role to new user
    role_name = read_settings(member.server.id, id='default_role')
    role = discord.utils.get(member.server.roles, name=role_name)
    await client.add_roles(member, role)
    log(member.name, 'joined', member.server, "Assigned {} role".format(role_name))


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
            if r.permissions.administrator:
                auth = True

        if auth:
            #If so, do the procedure
            #add deleting 
            await client.send_message(message.channel, ":white_check_mark:")
            c = shlex.split(message.content)
            try:
                n = int(c[1])
                s = c[2]
                log(message.author.name, message.channel.name, message.server, "**Deleting {} messages containing '{}'...**".format(n, s))
                await purge(message, n, s)
            except IndexError:
                try:
                    n = int(c[1])
                    log(message.author.name, message.channel.name, message.server, "**Deleting {} messages...**".format(n))
                    await purge(message, n)
                except IndexError:
                    log(message.author.name, message.channel.name, message.server, "**Deleting {} messages...**".format(10))
                    await purge(message)
        else:
            #If not, send a message indicating they aren't authorized
            await client.send_message(message.channel, ":no_good::skin-tone-2:")
    elif message.content.lower().startswith('wherest mein gofford'):
        await client.send_message(message.channel, ':sunflower:')
        await client.send_message(message.channel, 'i am here uwu')
    elif message.content.lower().startswith('gofford, '):
        if ' or ' in message.content:
            #Made for the decision function
            await client.send_message(message.channel, await decide(message) + '?')
        elif ' lov' in message.content:
            #Made for something like "gofford, i love you!"
            await client.send_message(message.channel, "i lomv you too!!")
            await client.send_message(message.channel, ":sparkling_heart:")
        elif any(s in message.content for s in [' how', ' why', ' what']):
            #Made for something like "gofford, how do i fix this?"
            p = ["¯\_(ツ)_/¯", "https://www.google.com/", "42"]
            await client.send_message(message.channel, random.choice(p))
    elif message.content.lower() == 'gofford':
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
    elif 'hetero' in message.content:
        await client.send_message(message.channel, ':no_good::skin-tone-2: grrrRRR :no_good::skin-tone-3:')
    elif message.content.startswith('!emojify'):
        s = message.content[8:]
        await client.send_message(message.channel, to_emoji(s))
    elif message.content.startswith('!presence'):
        """THIS IS A GLOBAL FUNCTION"""

        #Check if user is authorized
        auth = False
        if message.author.id in authorized_users:
            auth = True

        if auth:
            #If so, do the procedure
            await client.send_message(message.channel, ":white_check_mark:")
            presence = message.content[10:]
            await client.change_presence(game=discord.Game(name=presence))
            await client.send_message(message.channel, "Set!")
            log(message.author.name, message.channel.name, message.server, "Presence is set to '{}'".format(presence))
        else:
            #If not, send a message indicating they aren't authorized
            await client.send_message(message.channel, ":no_good::skin-tone-2:")
    elif message.content.startswith('!defaultrole'):
        await set_default_role(message)


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
    await client.send_file(message.channel, 'assets/sponge.jpg')


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
    
    a = message.content.lower().split(' or ')
    b = []
    for i in a:
        for banned in ['?', 'gofford, ']:
            i = i.strip(banned)
        b.append(i)
        
    return random.choice(b)


async def set_default_role(message):
    #Check if user is authorized
    auth = False
    for r in message.author.roles:
        if r.permissions.administrator:
            auth = True

    if auth:
        role_name = message.content[13:]
        await client.send_message(message.channel, "Setting default server role to '{}'...".format(role_name))
        log(message.author.name, message.channel, message.server, "Setting default server role to '{}'...".format(role_name))
        write_settings(message.server, default_role=role_name)
        await client.send_message(message.channel, ":white_check_mark:")
    else:
        await client.send_message(message.channel, ':no_good::skin-tone-2:')


if __name__ == '__main__':
    token = sys.argv[1] if len(sys.argv) > 1 else sys.exit(0)
    client.run(str(token))
