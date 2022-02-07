import discord
from discord.ext import commands
from config import get_token, config_cogs
from discord_components import DiscordComponents

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
DiscordComponents(bot)
token = get_token(6)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID : {bot.user.id})')
    members = 0
    for guild in bot.guilds:
        members += guild.member_count -1
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name=f'ผู้ใช้งาน {members} คน')
        )


@bot.event
async def on_command_error(ctx, error):
    pass


config_cogs(bot)
bot.run(token)