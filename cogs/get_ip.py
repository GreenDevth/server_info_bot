from discord.ext import commands
from discord_components import Button, ButtonStyle
import discord


class GetPass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        get_ip = interaction.component.custom_id
        if get_ip == 'get_ip_pwd':
            await interaction.respond(
                content='ระบบกำลังจัดส่งไอพีเซิร์ฟและรหัสผ่านไปยังข้อความส่วนตัวของคุณ```ไอพีเซิร์ฟ : 143.244.33.48:7102  รหัสผ่าน : 28702```')
            await discord.DMChannel.send(member, 'ไอพีเซิร์ฟ : **143.244.33.48:7102**  รหัสผ่าน : **28702**')

    @commands.command(name="get_pass")
    async def get_pass_command(self, ctx):
        await ctx.channel.send(
            "**⚔ ChangThai℠ Really survival**\n" +
            "\n- เซิร์ฟสิงคโปร์ ปิงเริ่มต้นที่ 30 " +
            "\n- อัตราการดรอปของเท่ากับ 1 เท่า ซอมบี้ดาเมจ 1 เท่า" +
            "\n- ไม่มีกฎ ผู้เล่นสามารถทำอะไรได้เท่าที่เซิร์ฟตั้งค่าไว้" +
            "\n- ยานพาหนะไม่มีดรอป ทำภารกิจเพื่อรับรถ หรือใช้เหรียญที่มีแลกซื้อได้" +
            "\n- แอดมินจะช่วยเหลือเท่าที่สามารถทำได้ เฉพาะเวลาที่ออนไลน์เท่านั้น" +
            "\n- จำกัด ผู้เล่นละ 1 ธงเท่านั้น จะทำการตรวจสอบธงทุกวันหากมีธงแต่ไม่มีสิ่งปลูกสร้างจะทำลายทิ้งทันที" +
            "\n- ไม่แสดงแผนที่ เพิ่มความเสียหายช๊อตไฟฟ้า 50 เท่า" +
            "\n- ไม่สามารถวางกับดักได้ ไม่มีการแสดงรายชื่อผู้ถูกสังหารและผู้สังหาร" +
            "\n- สร้างบ้านได้ทุกที่ แต่ห้ามใช้บัคของเกมส์ในการก่อสร้าง เช่น รั้ว และตัวบ้าน" +
            "\n\nกดรับ ไอพีและรหัสได้จากปุ่มด้านล่าง",
            components=[Button(style=ButtonStyle.gray, label='Get IP/PWD', emoji='💻', custom_id='get_ip_pwd')]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(GetPass(bot))
