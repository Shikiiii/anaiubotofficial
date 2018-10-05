import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from itertools import cycle
import aiohttp
import random
import os

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

players = []

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='!help | Made by Thegamesbg#2392 with love.'))
    print('Starting up...')

@bot.event
async def on_member_join(member):
    welcomeChannel = discord.utils.get(member.server.channels, name="welcome-n-goodbye")
    role = discord.utils.get(member.server.roles, name="User")
    await bot.add_roles(member, role)
    await bot.send_message(welcomeChannel, "Hello **{}**! Thank you for joining Anime News ○ Network! Please read #rules before you start using the server, so you don't have to face punishments while doing things. Enjoy your stay at Anime News! :heart:".format(member.name))

@bot.event
async def on_member_remove(member):
    welcomeChannel = discord.utils.get(member.server.channels, name="welcome-n-goodbye")
    await bot.send_message(welcomeChannel, "Goodbye, **{}**! We thank you for using our server, but you left :C We are sorry if we did something to you. Come back if you want! :smile:".format(member.name))

@bot.command(pass_context=True)
async def hello(ctx):
    await bot.say("Hello! :smile:")
    print('Someone used command (ID: !hello). The command was successfully executed.')

@bot.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount) +1):
        messages.append(message)
    await bot.delete_messages(messages)
    embed = discord.Embed(title="Messages successfully deleted.", color=0x3adf00)
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
        await bot.say("You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !mute), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@mute.error
async def mute_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say("Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
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
        await bot.say("You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !warn), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@warn.error
async def warn_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say("Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
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
        await bot.say("You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !kick), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@kick.error
async def kick_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say("Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
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
        await bot.say("You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !ban), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@ban.error
async def ban_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say("Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
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
        await bot.say("You need to mention a user!")
        print("{} used a command (ID: !pfp), but got declined for `not mentioning a user`.")

@bot.command(pass_context=True)
@commands.has_any_role("Admin", "Moderator")
async def unban(ctx, *username):
    server = ctx.message.author.server
    banned = await bot.get_bans(server)
    usr = discord.utils.get(banned, name=" ".join(username))
    embed = discord.Embed(title="A member has been UBNANNED!", description="{0} has been unbanned by {1}!".format(usr.name, ctx.message.author.name), color=0x3adf00)
    embed.set_footer(text="hmph, guess you weren't gone forever like it said | report staff abuse by DMing Thegamesbg")
    embed.set_thumbnail(url=usr.avatar_url)
    await bot.say(embed=embed)
    await bot.unban(server, usr)
    print("{} used command (ID: !unban), the command was successfully executed.".format(ctx.message.author.name))

@unban.error
async def unban_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say("Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
        print("{} used command (ID: !unban), but declined for `no permissions`.".format(ctx.message.author.name))

@bot.command(pass_context=True)
@commands.has_any_role("Admin", "Moderator")
async def unmute(ctx, usr):
    if len(ctx.message.mentions) > 0:
        user = ctx.message.mentions[0]
        role = discord.utils.get(user.server.roles, name="AnimeNews-Muted")
        embed = discord.Embed(title="A member has been UNMUTED!", description="{0} has been unmuted by {1}!".format(user.name, ctx.message.author.name), color=0x3adf00)
        embed.set_footer(text="you can chat, again | report staff abuse by DMing Thegamesbg")
        embed.set_thumbnail(url=user.avatar_url)
        await bot.say(embed=embed)
        await bot.remove_roles(usr, role)
        print("{} used command (ID: !unmute), the command was successfully executed.".format(ctx.message.author.name))
    else:
        await bot.say("You need to mention a user!".format(ctx.message.author.name))
        print("{} used command (ID: !unmute), but declined for `not mentioning a user`.".format(ctx.message.author.name))

@unmute.error
async def unmute_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await ctx.bot.say("Hey, {}! Don't try to use me when I don't want to, baka. **(You don't have permission to use this command!**)".format(ctx.message.author.name))
        print("{} used command (ID: !unmute), but declined for `no permissions`.".format(ctx.message.author.name))

@bot.command(pass_context=True)
async def magicball(ctx, *reason):
    rsn = " ".join(reason)
    msgs = ["Yes.", "No.", "That's not true.", "They lied to you.", "You got it right.", "That's true.", "Yes, you are.", "No, you aren't."]
    rdm = random.choice(msgs) 
    embed = discord.Embed(title=rdm, description="Command executed by {} | Question: {}".format(ctx.message.author.name, rsn), color=0x5882FA)
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)
    print("{} used !magicball, question: {}".format(ctx.message.author.name, rsn))

voice_client = None
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

def switch(argument):
    switcher = {
        "blackyy": "3",
        "₮hegamesbg": "2",
        "teaboi": "1"
    }
    return switcher.get(argument, "Invalid user")


@bot.command(pass_context=True)
async def reminder(ctx):
    await bot.say(switch(ctx.message.author.name.lower()))

@bot.command(pass_context=True)
async def kiss(ctx, username, *reason):
        reason = " ".join(reason)
        imgList = os.listdir(".picsngifs/kiss")
        imgString = random.choice(imgList)
        path = ".picsngifs/kiss/" + imgString
        embed = discord.embed()
        embed.set_author("**{}** has been kissed by **{}** for **{}**!".format(username, ctx.message.author.name, reason))
        await bot.say(embed=embed, path)

bot.run(os.environ.get("token"))
