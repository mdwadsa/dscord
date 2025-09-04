import discord
from discord.ext import commands
import os
from datetime import datetime

# ========================
# إعدادات البوت
# ========================
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# روم تسجيل الدخول
LOGIN_CHANNEL_ID = 1413017306698874951
# روم عرض الحالة
STATUS_CHANNEL_ID = 1413017747394396191
# رتبة المتابعة
ROLE_ID = 1413017853338189895
# مالك البوت
OWNER_ID = 948531215252742184

# قاعدة بيانات مؤقتة
logins = {}

# ========================
# أحداث
# ========================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ========================
# أوامر تسجيل الدخول
# ========================
@bot.command()
async def login(ctx):
    if ctx.channel.id != LOGIN_CHANNEL_ID:
        return
    if str(ctx.author.status) != "online":
        await ctx.send("❌ لازم تكون اونلاين عشان تسجل دخول")
        return
    logins[ctx.author.id] = datetime.now()
    await ctx.send("✅ تم تسجيل الدخول")

@bot.command()
async def logout(ctx):
    if ctx.channel.id != LOGIN_CHANNEL_ID:
        return
    if ctx.author.id in logins:
        del logins[ctx.author.id]
    await ctx.send("✅ تم تسجيل الخروج")

@bot.command()
async def status(ctx):
    if ctx.channel.id != STATUS_CHANNEL_ID:
        return
    role = ctx.guild.get_role(ROLE_ID)
    msg = "📋 **حالة الأعضاء:**\n"
    for member in role.members:
        if member.id in logins:
            delta = datetime.now() - logins[member.id]
            minutes = delta.seconds // 60
            msg += f"🟢 {member.display_name} - مسجل منذ {minutes} دقيقة\n"
        else:
            msg += f"🔴 {member.display_name} - غير مسجل\n"
    await ctx.send(msg)

# ========================
# نظام التكت
# ========================
@bot.command()
async def setuppp(ctx):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ غير مسموح لك")

    embed = discord.Embed(
        title="🎫 نظام التذاكر",
        description="اضغط على الزر لإنشاء تذكرة.\n\n**قوانين التكت:**\n1- احترام الجميع.\n2- ممنوع السب.\n3- التزام بالقوانين العامة.\n",
        color=0x00ff00,
    )
    view = discord.ui.View()
    button = discord.ui.Button(label="🎟️ إنشاء تذكرة", style=discord.ButtonStyle.green)

    async def create_ticket(interaction: discord.Interaction):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True),
        }
        ticket_channel = await ctx.guild.create_text_channel(
            f"ticket-{interaction.user.name}", overwrites=overwrites
        )
        await ticket_channel.send(f"{interaction.user.mention} تم فتح تذكرتك 🎫")
        await interaction.response.send_message("✅ تم إنشاء التذكرة", ephemeral=True)

    button.callback = create_ticket
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

# ========================
# تشغيل البوت
# ========================
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("❌ ضع التوكن في ملف .env")
else:
    bot.run(TOKEN)
