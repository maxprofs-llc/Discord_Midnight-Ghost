#!/usr/bin/python3
# coding: utf-8
# this script has to be run with a log channel id and a bot token as two arguments, like:
# python3 ./discord-midnight-ghost.py channelid token
import asyncio
import discord
import random
import re
from datetime import datetime as dt
from sys import argv

client = discord.Client()
botchannelid, token = argv[1:3]

def highlightedname(member, bold=True):
    boldchar = '**'
    if not bold:
        boldchar = ''
    if member.nick is not None:
        return '{3}{0}{3} ({1}#{2})'.format(member.nick, member.name,
                member.discriminator, boldchar)
    else:
        return '{2}{0}{2}#{1}'.format(member.name, member.discriminator,
                boldchar)

@client.event
async def on_message(message):
    utcnow = dt.utcnow()
    if not hasattr(on_message, "lastspam"):
        on_message.lastspam = utcnow
    if not hasattr(on_message, "lastmsg"):
        on_message.lastmsg = utcnow

    if message.author == client.user:
        return

    #msg = None
    #if message.content.lower().find('takbir') >= 0:
    #    msg = 'Allahu Akbar!          !الله أكبر'
    #if msg is not None:
    #    if (utcnow - on_message.lastspam).total_seconds() >= 20:
    #        await client.send_message(message.channel, msg)
    #    on_message.lastspam = utcnow

    if on_message.lastmsg.hour != utcnow.hour and utcnow.minute < 10:
        on_message.lastmsg = utcnow
        dieroll = random.randint(1, 72)
        if dieroll <= 3:
            for c in client.get_all_channels():
                if 'chat' in c.name:
                    await client.send_typing(c)
        if dieroll == 1:
            msgs = ['👻', '👻👻👻👻', '***boo!***', '👻 ***ooo ooooo oo***',
                    '***rattles chains***', '💀🎺 doot', '🎷💀 doot',
                    '👽🚬 ayy lmao', '.سلام 👳☝']
            msg = await client.send_message(message.channel,
                    random.choice(msgs))
            if random.randint(1, 6) == 1:
                await client.delete_message(msg)
            else:
                await asyncio.sleep(10)
                offset = -utcnow.hour + 24*(utcnow.hour>12)
                if utcnow.hour == 0:
                    midnightmsg = "(It's UTC midnight.)"
                elif utcnow.hour == 12:
                    midnightmsg = "(It's UTC-12 and UTC+12 midnight. " \
                            "*A double midnight!*)"
                else:
                    midnightmsg = "(It's UTC{:+d} midnight.)".format(offset)
                await client.edit_message(msg, msg.content + ' '*10 \
                        + midnightmsg)

    if '!cunt' in message.content.lower():
        await client.delete_message(message)

    #if message.content.startswith('!count'):
    #    msg = await client.send_message(message.channel, '1')
    #    for i in range(2, 11):
    #        await asyncio.sleep(1)
    #        msg = await client.edit_message(msg, msg.content \
    #                + ', {:d}'.format(i))
    #
    #if re.search(r'(^|\W)[dx]*xd+[xd]*(\W|$)', message.content.lower()):
    #    await asyncio.sleep(random.uniform(0, 5))
    #    msg = await client.send_message(message.channel,
    #            message.author.mention + ' x' \
    #                    + 'D'*int(1 + random.expovariate(0.04)))
    #
    #if message.content.startswith('!flash'):
    #    candybag = ['http://i.imgur.com/Zf1x4VW.png', '🍆', '🍆', '🍆', '🍆', '🍆']
    #    msg = await client.send_message(message.channel,
    #            random.choice(candybag))
    #    await asyncio.sleep(0.1)
    #    await client.delete_message(msg)
    #    await client.delete_message(message)

    on_message.lastmsg = utcnow

@client.event
async def on_ready():
    #print('{} Logged in as {}'.format(dt.utcnow(), client.user.name))
    await client.send_message(client.get_channel(botchannelid),
            '{} 👌 *bot (re)started and ready for action!*'.format(
            dt.utcnow().strftime("`%H:%M:%S UTC`")))

@client.event
async def on_member_join(member):
    boldname = highlightedname(member)
    msg = '{} 💯💯👔 {} **joined the server!** 💞💯🎉'.format(
            dt.utcnow().strftime("`%H:%M:%S UTC`"), boldname)
    await client.send_message(client.get_channel(botchannelid), msg)

@client.event
async def on_member_remove(member):
    boldname = highlightedname(member)
    msg = '{} 🙇💔🙅 {} **left the server!** 🛬🏢🏢💥'.format(
            dt.utcnow().strftime("`%H:%M:%S UTC`"), boldname)
    await client.send_message(client.get_channel(botchannelid), msg)

@client.event
async def on_voice_state_update(before, after):
    if 'offline' in [str(before.status), str(after.status)]:
        return
    if before.voice_channel != after.voice_channel:
        boldname = highlightedname(before)
        time = dt.utcnow().strftime("`%H:%M:%S UTC`")
        if before.voice_channel is None:
            msg = '{2} 🍻 {0} **joined {1.voice_channel}**'.format(boldname,
                    after, time)
        elif after.voice_channel is None:
            msg = '{2} 💀 {0} **left {1.voice_channel}**'.format(boldname,
                    before, time)
        else:
            msg = '{3} ↔ {0} **switched to {2.voice_channel}** from {1.voice_channel}'.format(boldname, before, after, time)
        await client.send_message(client.get_channel(botchannelid), msg)

@client.event
async def on_member_update(before, after):
    if before.status != after.status:
        time = dt.utcnow().strftime("`%H:%M:%S UTC`")
        boldname = highlightedname(before)
        msg = None
        if str(before.status) == 'offline':
            if after.voice_channel is None:
                msg = '{} 🍏 {} **went online**'.format(time, boldname)
            else:
                msg = '{} 🍻 {} **went 🍏 online and joined {}**'.format(time, boldname,
                        after.voice_channel)
        elif str(after.status) == 'offline':
            if before.voice_channel is None:
                msg = '{} 🍎 {} **went offline**'.format(time, boldname)
            else:
                msg = '{} 💀 {} **left {} and went 🍎 offline**'.format(time, boldname,
                        before.voice_channel)
        if msg is not None:
            await client.send_message(client.get_channel(botchannelid), msg)

client.run(token)
