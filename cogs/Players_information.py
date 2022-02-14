import discord
import random
import asyncio
import requests
import json
from config import get_token
from discord.ext.commands import Cog
from discord.ext.commands import command

token = get_token(2)
url = get_token(3)
auth = f'{token}'
head = {'Authorization': 'Brarer' + auth}


def get_players():
    res = requests.get(url, headers=head)
    players = res.json()['data']['attributes']['players']
    return players


class PlayersInformation(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print('Battlemetric is online')
        while True:
            status_type = random.randint(0, 1)
            if status_type == 0:
                players = get_players()
                print(players)
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name=f"ผู้รอดชีวิต {players}/20 คน"))
            else:
                players = get_players()
                print(players)
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name=f'ผู้รอดชีวิต {players}/20 คน'))
            await asyncio.sleep(45)

    @command(name='server')
    async def get_server(self, ctx):
        if ctx.channel.id == 925559937323659274:
            response = requests.get("https://api.battlemetrics.com/servers/13458708", headers=head)
            res_text = response.text
            json.loads(res_text)
            json_obj = response.json()
            scum_server = json_obj['data']['attributes']['name']
            scum_ip = json_obj['data']['attributes']['ip']
            scum_port = json_obj['data']['attributes']['port']
            scum_player = json_obj['data']['attributes']['players']
            scum_player_max = json_obj['data']['attributes']['maxPlayers']
            scum_rank = json_obj['data']['attributes']['rank']
            scum_status = json_obj['data']['attributes']['status']
            scum_time = json_obj['data']['attributes']['details']['time']
            scum_version = json_obj['data']['attributes']['details']['version']
            print(json_obj['data']['attributes']['players'])
            await ctx.reply(
                f"```\nServer: {scum_server}" +
                "\n======================================" +
                f"\nIP: {scum_ip}:{scum_port}" +
                f"\nStatus: {scum_status}" +
                f"\nTime in Game: {scum_time}" +
                f"\nPlayers: {scum_player}/{scum_player_max}" +
                f"\nRanking: #{scum_rank}" +
                f"\nGame version: {scum_version}\n" +
                f"\nServer Restarts Every 6 hours" +
                f"\nDay 3.8 hours, Night 1 hours" +
                "\n======================================"
                "\nby ChangThai℠ Really Survival```",
                mention_author=False
            )
        if ctx.channel.id != 925559937323659274:
            await ctx.reply('**กรุณาใช้คำสั่งนี้ที่ห้อง** <#925559937323659274>', mention_author=False, delete_after=2)
            await asyncio.sleep(2.5)
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(PlayersInformation(bot))
