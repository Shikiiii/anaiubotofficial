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
async def leave(ctx):
    await bot.say("✅ Successfuly ``disconnected`` your voice channel!")
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
    
class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = ' {0.title} uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()
class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @bot.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        else:
            await self.bot.say('Ready to play audio in **' + channel.name)

    @bot.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('Are you sure your in a channel?')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @bot.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            await self.bot.say("Loading the song please be patient..")
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)

    @bot.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))
    @bot.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @bot.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            await self.bot.say("Cleared the queue and disconnected from voice channel ")
        except:
            pass

    @bot.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @bot.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))

bot.run(os.environ.get("token"))
