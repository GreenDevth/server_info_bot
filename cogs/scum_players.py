import asyncio
from discord.ext import commands
from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config
from db.bank_db import bank_balance

db = read_db_config()


def players_info(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT * FROM scum_players WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res
    except Error as e:
        print(e)


def remove_players(discord_id):
    conn = None
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cur = conn.cursor()
        cur.execute('SELECT steam_id FROM scum_players WHERE discord_id = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            data = list(row)
            steam_id = data[0]
            cur.execute('DELETE FROM scum_players WHERE discord_id = %s', (discord_id,))
            conn.commit()
            cur.close()
            msg = "ระบบได้ทำการลบข้อมูล สตรีมหมายเลข {} เป็นที่เรียบร้อยแล้ว".format(steam_id)
            return msg.strip()
    except Error as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


class ScumPlayers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith("my_steam"):
            if message.channel.id == 925559937323659274:
                steam_id = players_info(message.author.id)
                await message.reply(
                    f"Your steam id : {steam_id[3]}", mention_author=False, delete_after=5
                )
                await asyncio.sleep(6)
                await message.delete()
            if message.author.guild_permissions.administrator:
                steam_id = players_info(message.author.id)
                await message.reply(
                    f"Your steam id : {steam_id[3]}", mention_author=False, delete_after=5
                )
                await asyncio.sleep(6)
                await message.delete()
            else:
                await message.reply('ให้ใช้งานคำสั่งที่ห้อง <#925559937323659274> เท่านั้น', mention_author=False)
                await asyncio.sleep(3)

    @commands.command(name="players_id")
    @commands.has_role('Admin')
    async def get_player_id(self, ctx, discord_id):
        # await ctx.message.delete()
        role = ctx.guild.get_role(893004701518417921)
        member = ctx.author
        status = players_info(discord_id)
        name = status[1]
        discord_id = status[2]
        steam_id = status[3]
        bank_id = status[4]
        coins = status[5]
        level = status[6]
        if role in member.roles:
            await ctx.reply(
                f"```css\nDiscord information of {name}\n"
                + "========================================="
                + f"\nNAME : '{name}'"
                + f"\nID : {discord_id}"
                + f"\nSTEAM ID : {steam_id}"
                + f"\nBANK ID : {bank_id}"
                + f"\nCOINS : {coins}"
                + f"\nLEVEL : {level}\n```",
                mention_author=False
            )
            await asyncio.sleep(5)
            await ctx.message.delete()

    @commands.command(name="steam_out")
    async def steam_out(self, ctx, *, number):
        discord_id = number
        await ctx.message.delete()
        remove = remove_players(discord_id)
        await ctx.channel.send('{}'.format(remove), delete_after=5)

    @commands.command(name='status')
    async def setatus_command(self, ctx):

        bank = bank_balance(ctx.author.id)
        coin = "${:,d}".format(bank[5])
        if ctx.channel.id == 925559937323659274:

            await ctx.reply(
                content=f'Discord Name : {bank[1]}'
                        f'\nBank ID : {bank[4]}'
                        f'\nCoins : {coin}'
                        f'\nLevel : {bank[6]}'
                        f'\nExp : {bank[8]}',
                mention_author=False
            )
        else:
            await ctx.reply(content='กรุณาพิมพ์คำสั่งที่ห้อง <#925559937323659274>', mention_author=False,
                            delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(ScumPlayers(bot))
