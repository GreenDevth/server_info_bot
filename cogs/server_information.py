import discord
import asyncio
from discord import DMChannel
from discord.ext import commands
from discord_components import ButtonStyle, Button
from db.players_db import player_exists, new_scum_players


class RegistrationPlayers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """ Can't type any text in this channel """

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     a_string = str(message.content)
    #     length = len(a_string)
    #     if message.channel.id == 918381749833171005:
    #         if message.author == self.bot.user:
    #             return
    #         if message.content.isdigit() and length == 17:
    #             print('ok')
    #             await asyncio.sleep(5)
    #             await message.delete()
    #         else:
    #             await message.reply('🧐 SteamID64 เฉพาะตัวเลขเท่านั้น', mention_author=False, delete_after=5)
    #             await asyncio.sleep(5)
    #             await message.delete()

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn_id = interaction.component.custom_id

        if btn_id == 'reg_id':
            check = player_exists(member.id)

            if check == 1:
                await interaction.send(f'{member.mention} : 📢 คุณได้ลงทะเบียนสตรีมไอดีไว้แล้ว')
                verify = discord.utils.get(interaction.guild.roles, name='Verify Members')
                role = discord.utils.get(interaction.guild.roles, name='joiner')
                await member.add_roles(verify)
                await member.remove_roles(role)

            if check == 0:
                await interaction.send(f'{member.mention} : 📝 โปรดระบุ SteamID ของคุณเพื่อดำเนินการลงทะเบียน')
                while True:
                    try:
                        msg = await self.bot.wait_for(
                            'message',
                            check=lambda r: r.author == interaction.author and r.channel == interaction.channel,
                            timeout=300
                        )
                        if msg.content.isdigit():
                            a_string = str(msg.content)
                            length = len(a_string)

                            discord_name = str(member.name)
                            discord_id = str(member.id)
                            convert = discord_id[:5]
                            bank_id = str(convert)

                            if length == 17:
                                new = new_scum_players(discord_name, member.id, msg.content, bank_id)
                                if new == 1:
                                    await DMChannel.send(
                                        member,
                                        "🎉 ยินดีต้อนรับอย่างเป็นทางการสู่สังคม ChangThai℠ Really survival "
                                    )
                                    verify = discord.utils.get(interaction.guild.roles, name='Verify Members')
                                    role = discord.utils.get(interaction.guild.roles, name='joiner')
                                    await member.add_roles(verify)
                                    await member.remove_roles(role)
                                    await msg.delete()
                                    return

                        else:
                            await interaction.channel.send(
                                f'{member.mention} : 📢 รูปแบบสตรีมไอดีของคุณไม่ถูกต้องกรุณาลองใหม่อีกครั้ง',
                                delete_after=5)
                            await msg.delete()

                    except asyncio.TimeoutError:
                        await interaction.send(
                            f'{member.mention} : 📢 คุณใช้เวลาในการลงทะเบียนนานเกินไป กรุณาลงทะเบียนใหม่อีกครั้ง'
                        )

    @commands.command(name='get_rules')
    async def get_rules(self, ctx):
        await ctx.channel.send(file=discord.File('./img/banner1.png'))
        await ctx.channel.send(
            "⚔ **ChangThai℠ Really survival**" +
            "\n\nเซิร์ฟเวอร์ที่ออกแบบมาให้ระบบการเล่นมีความแตกต่างจากเซิร์ฟทั่วไป "
            "\nทีมงานได้ทำการปรับแต่งค่าต่าง ๆ ให้มีความเป็นเกมส์เอาตัวรอด 100 % "
            "\nปิดการแสดงแผนที่ เน้นความสมจริง ปิดตี้ (เพื่อปิดการแสดงชื่อผู้เล่น) "
            "\nปิดการใช้งานกับดักเพื่อป้องกันการวางกับดักตามสถานที่สำคัญ "
            "\nตามถนน เนื่องจากกฎการวางระเบิดมักมีผู้แหกกฎเป็นประจำ และทีมงาน "
            "\nมีความตั้งใจให้ AI ของเกมส์มีบทบาทและอันตรายมากกว่าผู้เล่นด้วยกัน ",
            file=discord.File('./img/line.png')
        )
        await ctx.send(
            "\n\n⚖ **เงื่อนไขและข้อตกลง**" +
            "\nผู้เล่นต้องยอมรับในกฎกติกาของเซิร์ฟอย่างเคร่งครัด" +
            "\n- การสร้างธงอนุญาตให้สร้างได้เพียง 1 ธงต่อคน\n- สามารถสร้างบ้านได้ทุกที่ แต่ห้ามใช้บัคของเกมส์ในการก่อสร้างทุกรูปแบบ\n- สามารถครอบครองยานพาหนะได้ไม่จำกัด" +
            "\n- เอาตัวรอด 24 ชั่วโมง ไม่มีกฏ เซิร์ฟเวอร์ปิดคำสั่งที่ไม่จำเป็นไว้หมดแล้ว" +
            "\n- ไม่มีการช่วยเหลือจากแอดมิน เว้นแต่เห็นสมควรตามเหตุการณ์และเวลา\n- การตัดสินใจของแอดมินถือเป็นที่สิ้นสุด" +
            "\n- การโกง การก่อกวน ถือเป็นการกระทำที่ผิดต่อกฎกติกา กรณีร้ายแรงเชิญออกทันที\n"

        )
        await ctx.message.delete()

    @commands.command(name='register_id')
    async def steamid_reg(self, ctx):
        await ctx.channel.send(file=discord.File('./img/banner1.png'))
        await ctx.channel.send(
            ":pencil: **ลงทะเบียนผู้เล่น**\n" +
            "\nเพื่อให้ผู้เล่นสามารถใช้งานคำสั่งต่าง ๆ ภายในเซิร์ฟและบอทส่งของได้"
            "\nผู้เล่นจำเป็นต้องเตรียม SteamID ไว้สำหรับลงทะเบียน เพื่อสิทธิ์และประโยชน์ในการใช้งานบอท\n" +
            "\nคลิกที่ปุ่มด้านล่างเพื่อทำการลงทะเบียน หรือเช็คข้อมูลการลงทะเบียนของตนเอง",
            components=[
                Button(style=ButtonStyle.gray, label="REGISTER STEAM ID", custom_id='reg_id', emoji="📝")
            ]
        )
        await ctx.message.delete()

    @commands.command(name='clear')
    @commands.has_role('Admin')
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Delete **{amount}** Message successfull.', delete_after=2)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(content='คุณไม่ได้กำหนดจำนวนหลังคำสั่ง !clear', mention_author=False)


def setup(bot):
    bot.add_cog(RegistrationPlayers(bot))
