import discord
from discord.ext.commands import bot
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from itertools import cycle
import time
import youtube_dl
import random
from random import randint
import datetime
import os
import aiohttp
import sys
import traceback
import json
from discord.utils import get
from discord import Game

my_token = 'NTQ4MDU4MzYzODQ2NzIxNTM2.D0_18g.DWdGDgNGQ7OkdM3h7GjhgttRsUc'

client = commands.Bot(command_prefix = '^')

client.remove_command('help')
status = ('^help for commands', 'Updated V5', "Creator: Tron#2819", "In Server: {}".format(len(client.servers)))

players = {}


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name =current_status, type=1))
        await asyncio.sleep(10)


@client.event
async def on_ready():
    print('The bot is online and is connected to discord')

@client.event
async def on_message(message):
    
    await client.process_commands(message)
    if message.content.startswith('^help'):
        userID = message.author.id
        await client.send_message(message.channel, '<@%s> ***Check DM For Information!*** :mailbox_with_mail: ' % (userID))

@client.command(pass_context =True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(Colour = discord.Colour.orange())
    embed.set_author(name = '***Help Commands***')
    embed.add_field(name ='^say', value ='***Returns what the user says.***', inline=False)
    embed.add_field(name ='^clear', value ='***Deletes certain amount of messages, default amount is 10***', inline=False)
    embed.add_field(name ='^join', value ='***The bot joins the current voice channel, the user must be in a voice channel to use this command***', inline=False)
    embed.add_field(name ='^leave', value ='***The bot leaves the current voice channel.***', inline=False)
    embed.add_field(name ='^play', value ='***Plays the audio from a youtube url***', inline=False)
    embed.add_field(name ='^serverinfo', value ='***Gives the server information on the selected user example: ^serverinfo (Name User)***', inline=False)
    embed.add_field(name ='^ban', value ='***Ban A User from Discord Group***', inline=False)
    embed.add_field(name ='^kick', value ='***Kick A User from Discord Group***', inline=False)
    embed.add_field(name ='^website', value ='***Official Website***', inline=False)
    embed.add_field(name ='^findworld', value ='***Find A World From Growtopia!***', inline=False)
    embed.add_field(name='^mute', value ='***Mute A Player You Need Role Mute***', inline=False)
    embed.add_field(name='^unmute', value ='***Unmute Player Back***', inline=False)
    embed.add_field(name='^buildchannel', value ='***Create A Channel Example: ^buildchannel (dude-perfect)***', inline=False)
    embed.add_field(name='^servercount', value ='***This Will Be Show Who Invited This Bot!***', inline=False)
    embed.add_field(name='^invite', value ='***No Description!, The Description will be added in the next update***', inline=False)
    embed.add_field(name='^guildicon', value ='***This Will Be Show Discord Server Icon***', inline=False)
    embed.add_field(name='^avatar', value ='***This Will Be Show Users Avatar (target)***', inline=False)
    embed.add_field(name='^dm', value ='***This Like DM Users Example: ^dm (user) (message)***', inline=False)


    await client.send_message(author, embed=embed)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount = 10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) +1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount) + ' ***alright, i deleted the messages! so ya*** ')






@client.command(pass_context = True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    embed = discord.Embed(
        title = 'Voice channel',
        description = 'commands for the voice channel.',
        colour = discord.Colour.blue()
    )

    embed.add_field(name = '^play', value = 'play youtube audio with url', inline = False)
    embed.add_field(name = '^pause', value = 'pauses audio', inline = False)
    embed.add_field(name = '^resume', value = 'resumes audio', inline = False)
    embed.add_field(name = '^leave', value = 'leave voice channel', inline = False)

    await client.say(embed=embed)
    await client.join_voice_channel(channel)


@client.command(pass_context = True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


@client.command(pass_context = True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command(pass_context = True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context = True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context = True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, userName: discord.User):
    """Kick A User from server"""
    await client.say("@everyone")
    await client.say("***•Kick Notifications•***")
    time.sleep(1)
    await client.say("***•Name•:***")
    time.sleep(1)
    await client.say(userName)

    await client.kick(userName)

@client.command(pass_context = True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, userName: discord.User):
    """Ban A User from server"""
    await client.say("@everyone")
    await client.say("***•Banned Notifications•***")
    time.sleep(1)
    await client.say("***•Name•:***")
    time.sleep(1)
    await client.say(userName)
    await client.ban(userName, delete_message_days=7)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def buildchannel(ctx, type):
	await client.create_channel(ctx.message.server, ''f'{type}', type=discord.ChannelType.text)
	await client.say('Successfully I Created Channel Name: 'f'{type}')

@client.command(pass_context = True)
async def findworld(ctx, type):
    await client.say('Successfully!!')
    await client.say('https://growtopiagame.com/worlds/'f'{type}.png')
    time.sleep(1.0)
    await client.say('To Fix Bot Crash Now ^findworld Is Cooldown 10 Seconds')
    time.sleep(10.0)

@client.command(pass_context = True)
async def website():
    await client.say("https://anoforces.weebly.com")
    await client.say("Successfully You Use This Command Sending Logs")
    await client.say("Done!")

@client.command(pass_context = True)
async def jointim(ctx, *, member: discord.Member):
    await client.say('{0} joined on {0.joined_at}')

@client.command(pass_context = True)
async def nuke(ctx, type):
	await client.say('Nuking World...')
	time.sleep(5.0)
	await client.say('***>> 'f'{type} was nuked from orbit , it the only way to be sure. play nice everybody!***')
	time.sleep(1.0)
	await client.say('To Fix Bot Crash Now ^nuke Command Is Cooldown For 10 Seconds')
	time.sleep(10.0)
    

@client.command(pass_context = True)
async def secretban(ctx, userName: discord.User):
	if ctx.message.author.id==(tron):
		await client.ban(userName)
		await client.say("Roar!!! [No Commands Available]")

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def dm(ctx, member : discord.Member, *, content: str):
    await client.send_message(member, content)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx,target:discord.Member):
      role=discord.utils.get(ctx.message.server.roles,name='Muted')
 
      await client.add_roles(target,role)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unmute(ctx,target:discord.Member):
      role=discord.utils.get(ctx.message.server.roles,name='Muted')
 
      await client.remove_roles(target,role)


@client.command()
async def servercount():
  	"""Bot Guild Count"""
  	await client.say("**Im In {} Guilds!**".format(len(client.servers)))

@client.command(pass_context=True, no_pm=True)
async def avatar(ctx, member: discord.Member):
    """User Avatar"""
    await client.reply("{}".format(member.avatar_url))

@client.command(pass_context=True, no_pm=True)
async def guildicon(ctx):
    """Guild Icon"""
    await client.reply("{}".format(ctx.message.server.icon_url))

@client.command()
async def invite():
  	"""Bot Invite"""
  	await client.say("\U0001f44d")
  	await client.whisper("Add me with this link {}".format(discord.utils.oauth_url(client.user.id)))

	
@client.command()
async def say(*args):
        output = ''
        for word in args:
            output += word
            output += ' '
        await client.say(output)


@client.command(pass_context=True)
async def memberinfo(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="***Found A User***", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.add_field(name='NOTE',value = 'Toomany Users Spam This Command!, So This Features Has Added CoolDown 10 Seconds', inline= False)
    time.sleep(10)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)



client.loop.create_task(change_status())
client.run(my_token)
