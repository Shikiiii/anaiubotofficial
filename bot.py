import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from itertools import cycle
import aiohttp
import random
import os
import json
import time
from discord.voice_client import VoiceClient

cooldowns = {}

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

players = []

def switch(argument):
    switcher = {
        "blackyy": "3",
        "₮hegamesbg": "2",
        "teaboi": "1"
    }
    return switcher.get(argument, "Invalid user")

voice_client = None

async def try_create_user(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1
        users[user.id]['credits'] = 0

async def add_experience(users, user, channel, exp):
    users[user.id]["experience"] += exp
    await level_up(users, user, channel)

async def level_up(users, user, channel):
    experience = users[user.id]["experience"]
    lvl_start = users[user.id]["level"]
    lvl_end = int(experience ** (1/6))

    if lvl_start < lvl_end:
        embed = discord.Embed(title="Congratulations! You leveled up. You are now {} level.".format(lvl_end))
        embed.set_author(name="{}".format(user.name), icon_url=user.avatar_url)
        await bot.send_message(channel, "", embed=embed)
        await bot.send_message(channel, "{} leveled up to level {}!".format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end

        if lvl_end == 5:
            reward5 = discord.utils.get(user.server.roles, name="5Level")
            await bot.send_message(channel,
                                   ":star: | **{}** reached a milestone! Reward: **5Level Role**".format(user.name))
            await bot.add_roles(user, reward5)
            
@bot.command(pass_context=True)
async def hello(ctx):
    await bot.say("Hello! :smile:")
    print('Someone used command (ID: !hello). The command was successfully executed.')
    
@bot.command(pass_context=True)
async def t(ctx):
    await bot.say("**Online**! :white_check_mark:")

@bot.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount) +1):
        messages.append(message)
    await bot.delete_messages(messages)
    embed = discord.Embed(color=0x3adf00)
    embed.set_author(name='Deleted!', icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)
    print('Someone used command (ID: !clear). The command was successfully executed.')

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    
    embed = discord.Embed(title="Anaiu | Anime News Official Bot coded by @Thegamesbg#2392", color=0x3adf00)
    
    embed.add_field(name=":link: Anime News Invite Link: :link:", value=" https://discord.gg/Cb44gtf")
    embed.add_field(name=":coffee: Want to buy the developer a cup of coffee? :coffee:", value="View donation links with ``!donate``")
    embed.add_field(name=":scroll: Looking for commands list? :scroll:", value="https://bit.ly/anaiucommands")

    await bot.send_message(ctx.message.author, embed=embed)
    await bot.say('**Help message sended to {}. Please check your private messages to view the information.**'.format(ctx.message.author.name))
    print("{} used command (ID: !mute), the command was successfully executed.".format(ctx.message.author.name))

@bot.command(pass_context=True)
@commands.has_any_role("Admin", "Moderator")
async def mute(ctx, usr, *reason):
    if len(ctx.message.mentions) > 0:
        user = ctx.message.mentions[0]
        rsn = " ".join(reason)
        role = discord.utils.get(user.server.roles, name="AnimeNews-Muted")
        embed = discord.Embed(title="A member has been MUTED!", description="{0} has been muted by {1}!\nReason: {2}".format(user.name, ctx.message.author.name, rsn), color=0xff0000)
        embed.set_footer(text="this punishment will be reseted on sunday at whenever the owner gets his lazy ass off the chair to do it | report staff abuse by DMing Thegamesbg")
        embed.set_thumbnail(url=user.avatar_url)
        await bot.add_roles(user, role)
        await bot.say(embed=embed)
        print("{} used command (ID: !mute), the command was successfully executed.".format(ctx.message.author.name))
    else:
        await bot.say(":x: | You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !mute), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@mute.error
async def mute_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say(":x: | Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
        print("{} used command (ID: !mute), but declined for `no permissions`.".format(ctx.message.author.name))

@bot.command(pass_context=True)
@commands.has_any_role("Admin", "Moderator")
async def warn(ctx, usr, *reason):
    if len(ctx.message.mentions) > 0:
        user = ctx.message.mentions[0]
        rsn = " ".join(reason)
        role = discord.utils.get(user.server.roles, name="AnimeNews-Warned")
        embed = discord.Embed(title="A member has been WARNED!", description="{0} has been warned by {1}!\nReason: {2}".format(user.name, ctx.message.author.name, rsn), color=0xff0000)
        embed.set_footer(text="this punishment will be reseted on sunday at whenever the owner gets his lazy ass off the chair to do it | report staff abuse by DMing Thegamesbg")
        embed.set_thumbnail(url=user.avatar_url)
        await bot.add_roles(user, role)
        await bot.say(embed=embed)
        print("{} used command (ID: !warn), the command was successfully executed.".format(ctx.message.author.name))
    else:
        await bot.say(":x: | You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !warn), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@warn.error
async def warn_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say(":x: | Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
        print("{} used command (ID: !warn), but declined for `no permissions`.".format(ctx.message.author.name))

@bot.command(pass_context=True)
@commands.has_any_role("Admin", "Moderator")
async def kick(ctx, usr, *reason):
    if len(ctx.message.mentions) > 0:
        user = ctx.message.mentions[0]
        rsn = " ".join(reason)
        embed = discord.Embed(title="A member has been KICKED!", description="{0} has been kicked by {1}!\nReason: {2}".format(user.name, ctx.message.author.name, rsn), color=0xff0000)
        embed.set_footer(text="last warning, next is permanent ban! | report staff abuse by DMing Thegamesbg")
        embed.set_thumbnail(url=user.avatar_url)
        await bot.send_message(user, "This is your last warning. If you break 1 more rule, you will be permanent banned. Rejoin Anime News from here: https://discord.gg/yNHppj6 | If you've been kicked without a reason, please contact @Thegamesbg#2392.")
        await bot.kick(user)
        await bot.say(embed=embed)
        print("{} used command (ID: !kick), the command was successfully executed.".format(ctx.message.author.name))
    else:
        await bot.say(":x: | You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !kick), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@kick.error
async def kick_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say(":x: | Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
        print("{} used command (ID: !kick), but declined for `no permissions`.".format(ctx.message.author.name))

@bot.command(pass_context=True)
@commands.has_any_role("Admin", "Moderator")
async def ban(ctx, usr, *reason):
    if len(ctx.message.mentions) > 0:
        user = ctx.message.mentions[0]
        rsn = " ".join(reason)
        embed = discord.Embed(title="A member has been PERMANENT BANNED!", description="{0} has been permanent banned by {1}!\nReason: {2}".format(user.name, ctx.message.author.name, rsn), color=0xff0000)
        embed.set_footer(text="too bad he's/she's gone forever | report staff abuse by DMing Thegamesbg")
        embed.set_thumbnail(url=user.avatar_url)
        await bot.send_message(user, "You are now PERMANENT BANNED from Anime News! You can of course purchase unban by contacting @Thegamesbg#2392 via PayPal or SMS. By that way, you'll also get the donator rank (and all of it's percs)!")
        await bot.say(embed=embed)
        await bot.ban(user)
        print("{} used command (ID: !ban), the command was successfully executed.".format(ctx.message.author.name))
    else:
        await bot.say(":x: | You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !ban), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@ban.error
async def ban_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say(":x: | Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
        print("{} used command (ID: !ban), but declined for `no permissions`.".format(ctx.message.author.name))

@bot.command(pass_context=True)
async def pfp(ctx):
    if len(ctx.message.mentions) > 0:
        user = ctx.message.mentions[0]
        embed = discord.Embed(title="Profile picture of {}:".format(user.name), color=0x5882FA)
        embed.set_image(url=user.avatar_url)
        await bot.say(embed=embed)
        print("{} used command (ID: !pfp), the command was successfully executed.".format(ctx.message.author.name))
    else:
        await bot.say(":x: | You need to mention a user!")
        print("{} used a command (ID: !pfp), but got declined for `not mentioning a user`.")

@bot.command(pass_context=True)
@commands.has_any_role("Admin", "Moderator")
async def unban(ctx, *username):
    server = ctx.message.author.server
    banned = await bot.get_bans(server)
    user = discord.utils.get(banned, name=" ".join(username))
    embed = discord.Embed(title="A member has been UBNANNED!", description="{0} has been unbanned by {1}!".format(user.name, ctx.message.author.name), color=0x3adf00)
    embed.set_footer(text="hmph, guess you weren't gone forever like it said | report staff abuse by DMing Thegamesbg")
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)
    await bot.unban(server, user)
    print("{} used command (ID: !unban), the command was successfully executed.".format(ctx.message.author.name))

@unban.error
async def unban_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say(":x: | Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
        print("{} used command (ID: !unban), but declined for `no permissions`.".format(ctx.message.author.name))

@bot.command(pass_context=True)
@commands.has_any_role("Admin", "Moderator")
async def unmute(ctx, user):
    if len(ctx.message.mentions) > 0:
        user = ctx.message.mentions[0]
        role = discord.utils.get(user.server.roles, name="AnimeNews-Muted")
        embed = discord.Embed(title="A member has been UNMUTED!", description="{0} has been unmuted by {1}!".format(user.name, ctx.message.author.name), color=0x3adf00)
        embed.set_footer(text="you can chat, again | report staff abuse by DMing Thegamesbg")
        embed.set_thumbnail(url=user.avatar_url)
        await bot.send_message(ctx.message.channel, "", embed=embed)
        await bot.remove_roles(user, role)
        print("{} used command (ID: !unmute), the command was successfully executed.".format(ctx.message.author.name))
    else:
        await bot.say(":x: | You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !unmute), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@unmute.error
async def unmute_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say("Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
        print("{} used command (ID: !unmute), but declined for `no permissions`.".format(ctx.message.author.name))

@bot.command(pass_context=True)
@commands.has_any_role("Admin", "Moderator")
async def unwarn(ctx, user):
    if len(ctx.message.mentions) > 0:
        user = ctx.message.mentions[0]
        role = discord.utils.get(user.server.roles, name="AnimeNews-Warned")
        embed = discord.Embed(title="A member has been UNWARNED!", description="{0} has been unwarned by {1}!".format(user.name, ctx.message.author.name), color=0x3adf00)
        embed.set_footer(text="gratz :tada: | report staff abuse by DMing Thegamesbg")
        embed.set_thumbnail(url=user.avatar_url)
        await bot.send_message(ctx.message.channel, "", embed=embed)
        await bot.remove_roles(user, role)
        print("{} used command (ID: !unmute), the command was successfully executed.".format(ctx.message.author.name))
    else:
        await bot.say(":x: | You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !unwarn), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@unwarn.error
async def unwarn_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say("Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
        print("{} used command (ID: !unwarn), but declined for `no permissions`.".format(ctx.message.author.name))

@bot.command(pass_context=True)
async def magicball(ctx, *reason):
    rsn = " ".join(reason)
    msgs = [":crystal_ball: Yes.", ":crystal_ball: No.", ":crystal_ball: That's not true.", ":crystal_ball: They lied to you.", ":crystal_ball: You got it right.", ":crystal_ball: That's true.", ":crystal_ball: Yes, you are.", ":crystal_ball: No, you aren't."]
    rdm = random.choice(msgs) 
    embed = discord.Embed(title=rdm, description="Command executed by {} | Question: {}".format(ctx.message.author.name, rsn), color=0x5882FA)
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)
    print("{} used !magicball, question: {}".format(ctx.message.author.name, rsn))

@bot.command(pass_context=True)
async def join(ctx):
    await bot.say("✅ Successfully ``joined`` your voice channel!")
    channel = ctx.message.author.voice.voice_channel
    voice_client = await bot.join_voice_channel(channel)

@bot.command(pass_context=True)
async def leave(ctx):
    await bot.say("✅ Successfully ``disconnected`` your voice channel!")
    await voice_client.disconnect()
    voice_client = None

@bot.command(pass_context=True)
async def reminder(ctx):
    await bot.say(switch(ctx.message.author.name.lower()))

@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def kiss(ctx, username):
    if len(ctx.message.mentions) > 0:
      user = ctx.message.mentions[0]
      msgs = ["https://cdn.nekos.life/kiss/8585.gif", "https://images-ext-1.discordapp.net/external/Bzrtv_MYjG3fYIbCECRNgUcao1L_MUzpUASOwrtPiG0/https/cdn.nekos.life/kiss/2929.gif", "https://cdn.nekos.life/kiss/kiss13142.gif", "https://cdn.nekos.life/kiss/155155.gif", "https://images-ext-1.discordapp.net/external/zeO78IQa-yafl8XNzVtGFlqG8jHLw3fAKH-QU8e-5Xk/https/cdn.nekos.life/kiss/139139.gif", "https://cdn.nekos.life/kiss/C9C9.gif", "https://cdn.nekos.life/kiss/kiss10050.gif", "https://cdn.nekos.life/kiss/141141.gif", "https://cdn.nekos.life/kiss/kiss18553.gif", "https://cdn.nekos.life/kiss/C5C5.gif", "https://cdn.nekos.life/kiss/kiss1547.gif","https://cdn.nekos.life/kiss/D9D9.gif", "https://cdn.nekos.life/kiss/5555.gif", "https://cdn.nekos.life/kiss/9595.gif", "https://cdn.nekos.life/kiss/kiss16234.gif", "https://cdn.nekos.life/kiss/3535.gif","https://cdn.nekos.life/kiss/119119.gif"]
      rdm = random.choice(msgs)
      embed = discord.Embed(title="**{}** kisses **{}**. :heart:".format(ctx.message.author.name, user.name), color=0xfe2ef7)
      embed.set_image(url=rdm)
      await bot.say(embed=embed)
    else:
      await bot.say(":x: | You need to mention a user to kiss him/her!")    

@kiss.error
async def kiss_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say(":x: | Hey, **{}**! Sorry but this command has a cooldown of 10 seconds, please try again in **{}** seconds.".format(ctx.message.author.name, round(error.retry_after, 1)))
    
@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def hug(ctx, username):
    if len(ctx.message.mentions) > 0:
      user = ctx.message.mentions[0]
      msgs = ["https://cdn.nekos.life/hug/5D5D.gif", "https://cdn.nekos.life/hug/B1B1.gif", "https://cdn.nekos.life/hug/8989.gif", "https://cdn.nekos.life/hug/2929.gif", "https://cdn.nekos.life/hug/C1C1.gif", "https://cdn.nekos.life/hug/3939.gif", "https://cdn.nekos.life/hug/hug774.gif", "https://cdn.nekos.life/hug/hug13142.gif", "https://cdn.nekos.life/hug/A9A9.gif", "https://cdn.nekos.life/hug/8181.gif", "https://cdn.nekos.life/hug/hug8504.gif", "https://cdn.nekos.life/hug/hug3093.gif", "https://cdn.nekos.life/hug/3535.gif", "https://cdn.nekos.life/hug/2D2D.gif", "https://cdn.nekos.life/hug/4D4D.gif", "https://cdn.nekos.life/hug/hug6185.gif", "https://cdn.nekos.life/hug/9D9D.gif", "https://cdn.nekos.life/hug/hug2320.gif"]
      rdm = random.choice(msgs)
      embed = discord.Embed(title="**{}** hugs **{}**. :heart:".format(ctx.message.author.name, user.name), color=0xfe2ef7)
      embed.set_image(url=rdm)
      await bot.say(embed=embed)
    else:
      await bot.say(":x: | You need to mention a user to hug him/her!")
    
@hug.error
async def hug_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say(":x: | Hey, **{}**! Sorry but this command has a cooldown of 10 seconds, please try again in **{}** seconds.".format(ctx.message.author.name, round(error.retry_after, 1)))
    
@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def slap(ctx, username):
    if len(ctx.message.mentions) > 0:
      user = ctx.message.mentions[0]
      msgs = ["https://cdn.nekos.life/slap/slap17007.gif", "https://cdn.nekos.life/slap/slap6185.gif", "https://cdn.nekos.life/slap/slap74863696a58673d3d2d3332323535353132312e3134376463306136613061386265653434333036353633313437321547.gif", "https://cdn.nekos.life/slap/slap3866.gif", "https://cdn.nekos.life/slap/slap3093.gif", "https://cdn.nekos.life/slap/slap20099.gif", "https://cdn.nekos.life/slap/slap19326.gif", "https://cdn.nekos.life/slap/slap8504.gif", "https://cdn.nekos.life/slap/slap12369.gif", "https://cdn.nekos.life/slap/slap10823.gif"]
      rdm = random.choice(msgs)
      embed = discord.Embed(title="**{}** slaps **{}**.".format(ctx.message.author.name, user.name), color=0xfe2ef7)
      embed.set_image(url=rdm)
      embed.set_footer(text="Ouch, that hurts!")
      await bot.say(embed=embed)
    else:
      await bot.say(":x: | You need to mention a user to slap him/her!")
    
@slap.error
async def slap_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say(":x: | Hey, **{}**! Sorry but this command has a cooldown of 10 seconds, please try again in **{}** seconds.".format(ctx.message.author.name, round(error.retry_after, 1)))
    
@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def pat(ctx, username):
    if len(ctx.message.mentions) > 0:
      user = ctx.message.mentions[0]
      msgs = ["https://cdn.weeb.sh/images/rkSN7g91M.gif", "https://cdn.weeb.sh/images/rJMskkFvb.gif", "https://cdn.weeb.sh/images/Sy6Gektw-.gif", "https://cdn.weeb.sh/images/rJ4E1ep7f.gif", "https://cdn.weeb.sh/images/SJLaWWRSG.gif", "https://cdn.weeb.sh/images/HkJ2VknqG.gif", "https://cdn.weeb.sh/images/Bk4Ry1KD-.gif", "https://cdn.weeb.sh/images/r12R1kYPZ.gif", "https://cdn.weeb.sh/images/H1jgekFwZ.gif"]
      rdm = random.choice(msgs)
      embed = discord.Embed(title="**{}** pats **{}**. :3".format(ctx.message.author.name, user.name), color=0xfe2ef7)
      embed.set_image(url=rdm)
      await bot.say(embed=embed)
    else:
      await bot.say(":x: | You need to mention a user to pat him/her!")
    
@pat.error
async def pat_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say(":x: | Hey, **{}**! Sorry but this command has a cooldown of 10 seconds, please try again in **{}** seconds.".format(ctx.message.author.name, round(error.retry_after, 1)))
    
@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def bite(ctx, username):
    if len(ctx.message.mentions) > 0:
      user = ctx.message.mentions[0]
      msgs = ["https://cdn.discordapp.com/attachments/496005430254764042/497891785323053056/discord-avatar30092018.png", "https://cdn.discordapp.com/attachments/496005430254764042/497891785323053056/discord-avatar30092018.png"]
      rdm = random.choice(msgs)
      embed = discord.Embed(title="**{}** bites **{}**.".format(ctx.message.author.name, user.name), color=0xfe2ef7)
      embed.set_image(url=rdm)
      embed.set_footer(text="Ouch, that hurts!")
      await bot.say(embed=embed)
    else:
      await bot.say(":x: | You need to mention a user to bite him/her!")
    
@bite.error
async def bite_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say(":x: | Hey, **{}**! Sorry but this command has a cooldown of 10 seconds, please try again in **{}** seconds.".format(ctx.message.author.name, round(error.retry_after, 1)))

    
@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def tickle(ctx, username):
    if len(ctx.message.mentions) > 0:
      user = ctx.message.mentions[0]
      msgs = ["https://cdn.discordapp.com/attachments/496005430254764042/497891785323053056/discord-avatar30092018.png", "https://cdn.discordapp.com/attachments/496005430254764042/497891785323053056/discord-avatar30092018.png"]
      rdm = random.choice(msgs)
      embed = discord.Embed(title="**{}** tickles **{}**.".format(ctx.message.author.name, user.name), color=0xfe2ef7)
      embed.set_image(url=rdm)
      await bot.say(embed=embed)
    else:
      await bot.say(":x: | You need to mention a user to tickle him/her!")

@tickle.error
async def tickle_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say(":x: | Hey, **{}**! Sorry but this command has a cooldown of 10 seconds, please try again in **{}** seconds.".format(ctx.message.author.name, round(error.retry_after, 1)))
    
@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def cry(ctx):
    msgs = ["https://media.discordapp.net/attachments/435485699140091906/498047815126351882/Untitled-1.png?width=580&height=326", "https://media.discordapp.net/attachments/435485699140091906/498047830225715200/70864595_p0_master1200.jpg?width=230&height=326"]
    rdm = random.choice(msgs)
    embed = discord.Embed(title="**{}** is crying...".format(ctx.message.author.name), color=0xfe2ef7)
    embed.set_image(url=rdm)
    await bot.say(embed=embed)
    
@cry.error
async def cry_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say(":x: | Hey, **{}**! Sorry but this command has a cooldown of 10 seconds, please try again in **{}** seconds.".format(ctx.message.author.name, round(error.retry_after, 1)))
    
@bot.command(pass_context=True)
async def embedimg(ctx, *reason):
    rsn = " ".join(reason)
    embed = discord.Embed()
    embed.set_image(url="{}".format(rsn))
    await bot.say(embed=embed)
    
@bot.command(pass_context=True)
@commands.cooldown(1, 300, commands.BucketType.user)
async def roles(ctx):
    embed = discord.Embed(color=0x5882FA)
    embed.set_author(name="All server roles, listed here:", icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="Server leader: Thegamesbg#2392 | Command executed by {}".format(ctx.message.author.name))
    for role in ctx.message.server.roles:
        embed.add_field(name="Server roles:", value=role.name, inline=False)
    await bot.say(embed=embed)
    
@roles.error
async def roles_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say(":x: | Hey, **{}**! Sorry but this command has a cooldown of 300 seconds, please try again in **{}** seconds.".format(ctx.message.author.name, round(error.retry_after, 1)))
 
@bot.command(pass_context=True)
async def level(ctx):
    with open('users.json', 'r') as f:
        users = json.loads(f.read())

    lvl = users[ctx.message.author.id]["level"]
    await bot.send_message(ctx.message.channel, "**XP** | **{}**, you are at ``{}`` level. <a:ANHyped:501653444491214858>".format(ctx.message.author.name, lvl))

@bot.command(pass_context=True)
async def report(ctx, user, reason, *message):
    if len(ctx.message.mentions) > 0:
        user = ctx.message.mentions[0]
        await bot.send_message(ctx.message.channel, "Type ``confirm`` to report this member. Please note that reports that are NOT TRUE will transfer the punishment to YOU, so please don't abuse this command.")
        msg = await bot.wait_for_message(timeout=30, author=ctx.message.author, content='hello')
        
        if msg is None:
            await bot.send_message(ctx.message.channel, "{}, you ran out of time! (You didn't confirmed the !report)".format(ctx.message.author))
            return

        reporting_channel = discord.utils.get(ctx.message.author.server.channels, name="report-logs")
        reporting = discord.Embed(color=0xff0000)
        reporting.set_author(name="A new report has appeared:", icon_url=bot.user.avatar_url)
        reporting.add_field(name="Member:", value="{}".format(user.mention), inline=False)
        reporting.add_field(name="Reported by:", value="{}".format(ctx.message.author.mention), inline=False)
        reporting.add_field(name="Rule number broken:", value="{}".format(" ".join(reason)), inline=False)
        reporting.add_field(name="Channel broken in:", value="{}".format(ctx.message.channel.mention), inline=False)
        reporting.add_field(name="More information (optimal):", value="{}".format(" ".join(message)), inline=False)
        await bot.send_message(reporting_channel, "", embed=reporting)
        reply = discord.Embed(title="Thank you! Your report has been sended to our staff team for a review.", description="Please note that reports that are NOT TRUE will transfer the punishment to YOU!", color=0x3adf00)
        await bot.send_message(ctx.message.channel, "", embed=reply)

    else:
        await bot.send_message(ctx.message.channel, ":x: | Nu, baka! Correct usage: ``!report @someone rule_broken optimal_information``. Example: ``!report @Thegamesbg#2392 3 He is spamming and doesn't want to stop!``")

@bot.command(pass_context=True)
async def rps(ctx, message):
    channel = ctx.message.channel
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
    memberchoice = " ".join(message)
    if rock == memberchoice:
        rockchoice = ["paper", "scissors", "rock"]
        randomrock = random.choose(rockchoice)
        if randomrock == rock:
            embedROCKDRAW = discord.Embed(color=0xf3f781)
            embedROCKDRAW.set_author(name="I choose ROCK! - We are draw.", icon_url=ctx.message.author.avatar_url)
            embedROCKDRAW.set_footer(text="GG, {}!".format(ctx.message.author.name))
            await bot.send_message(ctx.message.channel, "", embed=embedROCKDRAW)
            return

        if randomrock == paper:
            embedROCKWIN = discord.Embed(color=0xff0000)
            embedROCKWIN.set_author(name="I choose PAPER! - I win.", icon_url=ctx.message.author.avatar_url)
            embedROCKWIN.set_footer(text="GG, {}!".format(ctx.message.author.name))
            await bot.say(embed=embedROCKWIN)
            return

        if randomrock == scissors:
            embedROCKLOSE = discord.Embed(color=0x40ff00)
            embedROCKLOSE.set_author(name="I choose SCISSORS! - I lose.", icon_url=ctx.message.author.avatar_url)
            embedROCKLOSE.set_footer(text="GG, {}!".format(ctx.message.author.name))
            await bot.say(embed=embedROCKLOSE)
            return

    if paper == memberchoice:
        paperchoice = ["rock", "scissors", "paper"]
        randompaper = random.choose(paperchoice)
        if randompaper == rock:
            embedPAPERLOSE = discord.Embed(color=0xff0000)
            embedPAPERLOSE.set_author(name="I choose ROCK! - I lose.", icon_url=ctx.message.author.avatar_url)
            embedPAPERLOSE.set_footer(text="GG, {}!".format(ctx.message.author.name))
            await bot.say(embed=embedPAPERLOSE)
            return

        if randompaper == paper:
            embedPAPERDRAW = discord.Embed(color=0xf3f781)
            embedPAPERDRAW.set_author(name="I choose PAPER! - We are draw.", icon_url=ctx.message.author.avatar_url)
            embedPAPERDRAW.set_footer(text="GG, {}!".format(ctx.message.author.name))
            await bot.say(embed=embedPAPERDRAW)
            return

        if randompaper == scissors:
            embedPAPERWIN = discord.Embed(color=0x40ff00)
            embedPAPERWIN.set_author(name="I choose SCISSORS! - I win.", icon_url=ctx.message.author.avatar_url)
            embedPAPERWIN.set_footer(text="GG, {}!".format(ctx.message.author.name))
            await bot.say(embed=embedPAPERWIN)
            return

    if scissors == memberchoice:
        scissorschoice = ["paper", "rock", "scissors"]
        randomscissors = random.choose(scissorschoice)
        if randomscissors == rock:
            embedSCISSORSWIN = discord.Embed(color=0x40ff00)
            embedSCISSORSWIN.set_author(name="I choose ROCK! - I win.", icon_url=ctx.message.author.avatar_url)
            embedSCISSORSWIN.set_footer(text="GG, {}!".format(ctx.message.author.name))
            await bot.say(embed=embedSCISSORSWIN)
            return

        if randomscissors == paper:
            embedSCISSORSLOSE = discord.Embed(color=0xff0000)
            embedSCISSORSLOSE.set_author(name="I choose PAPER! - I lose.", icon_url=ctx.message.author.avatar_url)
            embedSCISSORSLOSE.set_footer(text="GG, {}!".format(ctx.message.author.name))
            await bot.say(embed=embedSCISSORSLOSE)
            return

        if randomscissors == scissors:
            embedSCISSORSDRAW = discord.Embed(color=0xf3f781)
            embedSCISSORSDRAW.set_author(name="I choose SCISSORS! - We are draw.", icon_url=ctx.message.author.avatar_url)
            embedSCISSORSDRAW.set_footer(text="GG, {}!".format(ctx.message.author.name))
            await bot.say(embed=embedSCISSORSDRAW)
            return
        
@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='!help | Made by Thegamesbg#2392 with love.'))
    print('Starting up...')
  
@bot.event
async def on_member_join(member):
    welcomeChannel = discord.utils.get(member.server.channels, name="welcome-n-goodbye")
    role = discord.utils.get(member.server.roles, name="User")
    channel = discord.utils.get(member.server.channels, name="rules")
    await bot.add_roles(member, role)
    await bot.send_message(welcomeChannel, "Welcome **{}**! Thank you for joining Anime News ○ Network! Please read {} before you start using the server, so you don't have to face punishments while doing things. Enjoy your stay at Anime News! :heart:".format(member.name, channel.mention))
    with open('users.json', 'r') as f:
        users = json.loads(f.read())

    await try_create_user(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@bot.event
async def on_member_remove(member):
    welcomeChannel = discord.utils.get(member.server.channels, name="welcome-n-goodbye")
    await bot.send_message(welcomeChannel, "Goodbye, **{}**! We thank you for using our server, but you left :C We are sorry if we did something to you. Come back if you want! :smile:".format(member.name))

@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.author.id in cooldowns:
            if (time.time() - cooldowns[message.author.id]) < 60:
                await bot.process_commands(message)
                return

        cooldowns[message.author.id] = time.time()

        with open('users.json', 'r') as f:
            users = json.loads(f.read())

        await try_create_user(users, message.author)
        await add_experience(users, message.author, message.channel, 5)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await bot.process_commands(message)
       
bot.run(os.environ.get("token"))
