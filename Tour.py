import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import has_permissions
import asyncio
from itertools import cycle
import time
import youtube_dl
import random
import aiohttp
import json
from discord import Game

my_token = 'NTQ5MDM4NTIyMDQwODQ0MzA5.D3zJ-w.dWEZpgrRD_RBFPlrewC0STQAc-M'

client = commands.Bot(command_prefix = '>')

client.remove_command('help')
status = ['>help for commands', 'Code By Tourbilion', "Creator: ꧁☬༒๏บℝbιlι๏🅽༒☬꧂#1585"]

players = {}


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name =current_status))
        await asyncio.sleep(10)


@client.event
async def on_ready():
    print('The bot is online and is connected to discord')

@client.event
async def on_message(message):
    
    await client.process_commands(message)
    if message.content.startswith('>help'):
        userID = message.author.id
        await client.send_message(message.channel, '<@%s> ***Check DM For Information!*** :mailbox_with_mail: ' % (userID))

@client.command(pass_context =True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(Colour = discord.Colour.orange())
    embed.set_author(name = '***Help Commands***')
    embed.add_field(name ='>say', value ='***Returns what the user says.***', inline=False)
    embed.add_field(name ='>clear', value ='***Deletes certain amount of messages, default amount is 10***', inline=False)
    embed.add_field(name ='>join', value ='***The bot joins the current voice channel, the user must be in a voice channel to use this command***', inline=False)
    embed.add_field(name ='>leave', value ='***The bot leaves the current voice channel.***', inline=False)
    embed.add_field(name ='>play', value ='***Plays the audio from a youtube url***', inline=False)
    embed.add_field(name ='>serverinfo', value ='***Gives the server information on the selected user example: >serverinfo (Name User)***', inline=False)
    embed.add_field(name ='>ban', value ='***Ban A User from Discord Group***', inline=False)
    embed.add_field(name ='>kick', value ='***Kick A User from Discord Group***', inline=False)
    embed.add_field(name ='>website', value ='***Discord Website***', inline=False)
    embed.add_field(name ='>mute', value ='***Gives the member muted***', inline=False)
    embed.add_field(name ='>unmute', value ='***Gives the member unmuted***', inline=False)
    embed.add_field(name ='>spin', value ='***you get random number***', inline=False)
    embed.add_field(name ='>howgay', value ='***see you gay or not***', inline=False)
    embed.add_field(name ='>dm', value ='***bot will dm select user and put you say***', inline=False)
    embed.add_field(name ='>mdm', value ='***bot will dm you***', inline=False)
    embed.add_field(name ='>avatar', value ='***select user and see he avatar***', inline=False)
    embed.add_field(name ='>findworld', value ='***Find A World From Growtopia!***', inline=False)
    embed.add_field(name ='>servercount', value ='***see bot in the howmuch playing server***', inline=False)
    embed.add_field(name ='>servericon', value ='***see the server icon***', inline=False)
    embed.add_field(name ='>serverid', value ='***see the server id***', inline=False)
    embed.add_field(name ='Sup dude', value ='***Subcribe : Tourbilion Gtprivate link*** : https://www.youtube.com/channel/UCRlNfKIVy2G0ibX830L-5IQ', inline=False)


    await client.send_message(author, embed=embed)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount = 10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) +1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount) + ' messages were deleted so ya! ')






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
@commands.has_permissions(administrator_members=True)
async def unban(ctx, userName: discord.User):
    """Unban A User from server"""
    await client.unban(userName)
    await client.say("__**Successfully User Has Been Unbanned**__")

@client.command(pass_context = True)
async def findworld(ctx, type):
    await client.say('Successfully!!')
    await client.say('https://growtopiagame.com/worlds/'f'{type}.png')

@client.command(pass_context=True)
async def mute(ctx,target:discord.Member):
      role=discord.utils.get(ctx.message.server.roles,name='Muted')
 
      await client.add_roles(target,role)
      await client.say('**He Get Mute!**')
      await client.send_message(target,'**You Get Mute!**')
        
@client.command(pass_context=True)
async def unmute(ctx,target:discord.Member):
      role=discord.utils.get(ctx.message.server.roles,name='Muted')
 
      await client.remove_roles(target,role)
      await client.send_message(target,'**You Got Unmute!**')
      await client.say('**He Get Unmute!**')

@client.command(pass_context = True)
async def website():
    await client.say("Discord : https://discord.gg/VPA5vJ")
    await client.say("Successfully You Use This Command Sending Logs")
    await client.say("Done!")

@client.command(pass_context = True)
async def jointim(ctx, *, member: discord.Member):
    await client.say('{0} joined on {0.joined_at}')

@client.command(pass_context = True)
async def nuke(ctx, type):
    await client.say('***>> 'f'{type} was nuked from orbit , it the only way to be sure . play nice everybody!***')

@client.command(pass_context = True)
async def secretban(ctx, userName: discord.User):
    await client.ban(userName)
    await client.say("Secret Successfully")

@client.command()
async def say(*args):
        output = ''
        for word in args:
            output += word
            output += ' '
        await client.say(output)


@client.command(pass_context=True)
async def serverinfo(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="***Found A User***", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.add_field(name='Dont Abuse',value = 'Dont Abuse This Command Because This Command is not stable', inline= False)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)

@client.command()
async def spin():
	spin = random.choice(['33','32','31','30','29','28','27',',26','25','24','23','23','22','21','20','19','18','17','16','15','14','13','12','11','10','9','8','7','6','5','4','3','2','1'])
	await client.say(spin)
	
@client.command()
async def howgay():
	howgay = random.choice(['1%','2%','3%','4%','5%','6%','7%','8%','9%','10%','11%','12%','13%','14%','15%','16%','17%','18%','19%','20%','21%','22%','23%','24%','25%','26%','27%','28%','29%','30%','40%','41%','42%','43%','44%','45%','46%','47%','48%','49%','50%','51%','52%','53%','53%','54%','55%','56%','57%','58%','59%','60%','61%','62%','63%','64%','65%','66%','67%','68%','69%','70%','71%','72%','73%','74%','75%','76%','77%','78%','79%','80%','81%','82%','83%','84%','85%','86%','87%','88%','89%','90%','91%','92%','93%','94%','95%','96%','97%','98%','99%','100'])
	await client.say(howgay)
	
@client.command(pass_context = True)
async def dm(ctx, member : discord.Member, *, content: str):
    await client.send_message(member, content)
    await client.say('**He Get Send Message!**')

@client.command(pass_context=True)
async def mdm(ctx,target:discord.Member):
    await client.send_message(target,'***You Has Been Moved To Group***: https://discord.gg/BGfE3Q')
    await client.send_message(target,'***You Has Been Moved To Group***: https://discord.gg/BGfE3Q')
    await client.say('**He Get Send Message!**')

@client.command(pass_context=True, no_pm=True)
async def avatar(ctx, member: discord.Member):
    """User Avatar"""
    await client.reply("{}".format(member.avatar_url))

@client.command(pass_context=True)
async def ping(ctx):
    t = await client.say('Pong')
    ms = (t.timestamp-ctx.message.timestamp).total_seconds() * 1000
    await client.edit_message(t, new_content='Got:` {}ms`'.format(int(ms)))
    
@client.command()
async def servercount():
  	"""Bot Guild Count"""
  	await client.say("**I'm in {} Servers!**".format(len(client.servers)))

@client.command(pass_context=True, no_pm=True)
async def servericon(ctx):
    """Guild Icon"""
    await client.reply("{}".format(ctx.message.server.icon_url))

@client.command(pass_context=True)
async def serverid(ctx):
	  """Guild ID"""
	  await client.say("`{}`".format(ctx.message.server.id))

client.loop.create_task(change_status())
client.run('NTQ5MDM4NTIyMDQwODQ0MzA5.D3zJ-w.dWEZpgrRD_RBFPlrewC0STQAc-M')
