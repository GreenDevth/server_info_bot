import discord
from discord import DMChannel
from discord.ext import commands


class JoinMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(866926077246832680)
        welcome = guild.get_channel(914080006429360149)
        role = discord.utils.get(guild.roles, name="joiner")
        await member.add_roles(role)

        await welcome.send(f"{member.mention} : {member.name} ได้เข้าร่วมเซิร์ฟของเราแล้ว")
        await DMChannel.send(
            member,
            "**⚔ ChangThai℠ Really survival**\n\n" +
            "\n- เซิร์ฟสิงคโปร์ ปิงเริ่มต้นที่ 30 " +
            "\n- อัตราการดรอปของเท่ากับ 1 เท่า ซอมบี้ดาเมจ 1 เท่า" +
            "\n- ไม่มีกฎ ผู้เล่นสามารถทำอะไรได้เท่าที่เซิร์ฟตั้งค่าไว้" +
            "\n- ยานพาหนะไม่มีดรอป ทำภารกิจเพื่อรับรถ หรือใช้เหรียญที่มีแลกซื้อได้" +
            "\n- แอดมินจะช่วยเหลือเท่าที่สามารถทำได้ เฉพาะเวลาที่ออนไลน์เท่านั้น" +
            "\n- จำกัด ผู้เล่นละ 1 ธงเท่านั้น ครอบครองยานภาหนะได้ไม่จำกัด" +
            "\n- ไม่แสดงแผนที่ เพิ่มความเสียหายช๊อตไฟฟ้า 50 เท่า" +
            "\n- ไม่สามารถวางกับดักได้ ไม่มีการแสดงรายชื่อผู้ถูกสังหารและผู้สังหาร" +
            "\n- สร้างบ้านได้ทุกที่ แต่ห้ามใช้บัคของเกมส์ในการก่อสร้าง ทุกชนิด" +
            "\n- ไอพีเซิร์ฟ : **143.244.33.48:7102** รหัสผ่าน **28702**"
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(866926077246832680)
        leave = guild.get_channel(937573869361979422)
        await leave.send(f"{member.mention} : {member.name} ได้ออกจากเซิร์ฟของเราแล้ว")


def setup(bot):
    bot.add_cog(JoinMember(bot))

