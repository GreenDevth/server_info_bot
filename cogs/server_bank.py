import asyncio
import discord
from discord.ext import commands
from db.bank_db import *

class DiscordBank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bank is online')

    
    @commands.command(name='bank')
    async def bank_balance(self, ctx):
        bank = bank_balance(ctx.author.id)
        coin = "${:,d}".format(bank[5])
        if ctx.channel.id == 925559937323659274:
                await ctx.reply(
                    content=
                    f"```css\nName : '{bank[1]}' , Bank ID : {bank[4]}, Total : {coin}\n```"
                    "ใช้คำสั่ง `` !dmbank `` สำหรับส่งข้อมูลแบบส่วนตัว",
                    mention_author=False)
        
        elif ctx.author.guild_permissions.administrator == True:
                await ctx.reply(
                    content=
                    f"```css\nName : '{bank[1]}' , Bank ID : {bank[4]}, Total : {coin}\n```"
                    "ใช้คำสั่ง `` !dmbank `` สำหรับส่งข้อมูลแบบส่วนตัว",
                    mention_author=False)
        
        else:
            await ctx.reply(content='กรุณาพิมพ์คำสั่งที่ห้อง <#925559937323659274>', mention_author=False,
                                delete_after=5)
            await asyncio.sleep(5)
            await ctx.delete()
    
    @commands.command(name='dmbank')
    async def dbbank_command(self, ctx):
        member = ctx.author
        bank = bank_balance(ctx.author.id)
        coin = "${:,d}".format(bank[5])
        if ctx.channel.id == 925559937323659274:
                await ctx.reply(
                    content=
                    "ระบบกำลังส่งข้อความแบบส่วนตัวให้คุณ",
                    mention_author=False)
                await discord.DMChannel.send(member,  f"Bank ID : {bank[4]}, Total : {coin}")
        elif ctx.author.guild_permissions.administrator == True:
                await ctx.reply(
                    content=
                    "ระบบกำลังส่งข้อความแบบส่วนตัวให้คุณ",
                    mention_author=False)
                await discord.DMChannel.send(member,  f"Bank ID : {bank[4]}, Total : {coin}")
        else:
            await ctx.reply(content='กรุณาพิมพ์คำสั่งที่ห้อง <#925559937323659274>', mention_author=False,
                                delete_after=5)
            await asyncio.sleep(5)
            await ctx.delete()


    @commands.command(name='transfer')
    async def transfer_command(self, ctx, amount: int, bank_id: str):
        if ctx.channel.id == 925559937323659274:
            discord_id = ctx.author.id
            transfer = transfer_coin(discord_id,amount,bank_id)
            print(type(bank_id))
            await ctx.reply(f'{transfer}', mention_author=False)
        else:
            await ctx.reply(content='กรุณาพิมพ์คำสั่งที่ห้อง <#925559937323659274>', mention_author=False)


    @commands.command(name='addcoins')
    async def addcoins_command(self, ctx, amount, discord_id):
        if ctx.channel.id == 925559937323659274:
            add = add_coins(amount, discord_id)
            await ctx.reply(f'{add}', mention_author=False)
        elif ctx.author.guild_permissions.administrator == True:
            add = add_coins(amount, discord_id)
            await ctx.reply(f'{add}', mention_author=False)
        elif ctx.author.guild_permissions.administrator == False:
            await ctx.reply(content='คำสั่งนี้ใช้งานได้แค่แอดมินเท่านั้น', mention_author=False)
        else:
            await ctx.reply(content='กรุณาพิมพ์คำสั่งที่ห้อง <#925559937323659274>', mention_author=False)

    @commands.command(name='removecoins')
    async def removecoins_command(self, ctx, amount, discord_id):
        if ctx.channel.id == 925559937323659274:
            remove = remove_coins(amount, discord_id)
            await ctx.reply(f'{remove}', mention_author=False)
        elif ctx.author.guild_permissions.administrator == True:
            remove = remove_coins(amount, discord_id)
            await ctx.reply(f'{remove}', mention_author=False)
        elif ctx.author.guild_permissions.administrator == False:
            await ctx.reply(content='คำสั่งนี้ใช้งานได้แค่แอดมินเท่านั้น', mention_author=False)
        else:
            await ctx.reply(content='กรุณาพิมพ์คำสั่งที่ห้อง <#925559937323659274>', mention_author=False)


def setup(bot):
    bot.add_cog(DiscordBank(bot))

