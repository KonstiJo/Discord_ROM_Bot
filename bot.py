# Importiert aller notwendigen Module
import discord
import os
import json

# Importiert aller notwendigen Module für Slash Commands
from discord import app_commands
from discord import Embed, Interaction
from discord import File
from discord.ui import View, Button
from datetime import datetime
from dotenv import load_dotenv
from keep_alive import keep_alive

# Lädt die .env Datei
load_dotenv()

# Starte Timer der Uptime
start_time = datetime.now()

# Discord Server ID für Slash Commands
GUILD_ID = 1338866926952120412
firmwares_channel = "https://discord.com/channels/1338866926952120412/1338866928818585606"
request_channel = "https://discord.com/channels/1338866926952120412/1338866928487366752"
support_channel = "https://discord.com/channels/1338866926952120412/1338866928818585607"
keys_channel = "https://discord.com/channels/1338866926952120412/1338866928818585605"

# Definition der Pfade für Logs und Zähler
LOG_PATH = "logs/command_log.txt"
COUNT_PATH = "counters/usage_count.json"

# Erstellt die Verzeichnisse für Logs und Zähler, falls sie nicht existieren
os.makedirs("logs", exist_ok=True)
os.makedirs("counters", exist_ok=True)


# Bot-Klasse erstellen
class MyBot(discord.Client):
    # Bot initialisieren
    def __init__(self):
        super().__init__(
            intents=discord.Intents.default())  # Intents definieren
        self.tree = app_commands.CommandTree(self)  # Slash Commands aktivieren

    async def setup_hook(self):
        # Slash Commands nur für ROMS/PIRACY 3 synchronisieren
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print("✅ Slash-Commands synchronisiert!")


# Bot-Instanz erstellen
bot = MyBot()


# Bot ist online
@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

# /dm Befehl
@bot.tree.command(name="dm", description="Sends you a private message.")
async def dm(interaction: discord.Interaction):
    log_command(interaction.user.name, "dm")
    count_command("dm")
    try:
        await interaction.user.send(
            "📬\nHi! The test was succesfull.\nYou can use the roms command now! :D"
        )
        await interaction.response.send_message("✅ DM was sent!",
                                                ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ I couldn't send you a DM.\nPlease check your settings - DMs deactivated?",
            ephemeral=True)


# Button für Rom-Liste
class AgreeView(View):

    def __init__(self, user: discord.User):
        super().__init__(timeout=60)  # 60 Sekunden zum Reagieren
        self.user = user

    @discord.ui.button(label="✅ I agree", style=discord.ButtonStyle.success)
    async def agree_button(self, interaction: discord.Interaction,
                           button: Button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(
                "❌ Request discarded.", ephemeral=True) 
            return

        file_path = "roms.txt"

        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("There was an issue with the ROM-List.\nPlease contact an Admin.")

        with open(file_path, "rb") as f:
            file = discord.File(f, filename="roms.txt")
            try:
                await self.user.send(
                    content=
                    "📥\nHere is the current list of available ROMs.\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️",
                    file=file)
                await interaction.response.edit_message(
                    content="✅ ROM-List was sent per DM.", view=None)
            except discord.Forbidden:
                await interaction.response.edit_message(
                    content="❌ DMs deactivated. I couldn't text you anything.",
                    view=None)

    @discord.ui.button(label="❌ I disagree", style=discord.ButtonStyle.danger)
    async def disagree_button(self, interaction: discord.Interaction,
                              button: Button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(
                "❌ Request discarded.", ephemeral=True)
            return

        await interaction.response.edit_message(content="❌ Request discarded.",
                                                view=None)


# /rom-list Befehl
@bot.tree.command(
    name="rom-list",
    description="Sendet dir eine ROM-Liste per DM (nach Zustimmung)")
async def romlist(interaction: discord.Interaction):
    log_command(interaction.user.name, "rom-list")
    count_command("rom-list")

    view = AgreeView(interaction.user)

    await interaction.response.send_message(content=(
        "⚠️**Disclaimer:**⚠️\n\n"
        "By clicking **I agree**, you confirm that you already own a legal, physical copy of the original hardware and software.\n "
        "These files are provided strictly for personal backup and preservation purposes only.\n\n"
        "We do not condone or promote piracy, and we cannot be held responsible for the actions of our users.\n"
        "If you do not own the original hardware/software, you must delete the files immediately.\n\n"
        "By proceeding, you acknowledge that you access this ROM list at your own risk, and we are not liable for any legal issues that may arise."
    ),
                                            view=view,
                                            ephemeral=True)


# /time Befehl
@bot.tree.command(name="time",
                  description="Get the time you are on the server")
async def time(interaction: discord.Interaction):
    log_command(interaction.user.name, "time")
    count_command("time")
    await interaction.response.send_message(
        f"You joined the Server on this Date:**\n {interaction.user.joined_at.strftime('%d.%m.%Y')}**  -  **{interaction.user.joined_at.strftime('%H:%M:%S')}**",
        ephemeral=False)


# /info Befehl
@bot.tree.command(name="info",
                  description="An overview of the most important dates and events.")
async def info(interaction: Interaction):
    log_command(interaction.user.name, "info")
    count_command("info")

    embed = Embed(
        title="📊 Server History & Bot-Info",
        description=
        "An overview of the most important dates and events.\n",
        color=0x7000ff  # Violette Farbe
    )

    # 1st Server Infos
    embed.add_field(name="\n🕒 1st Server",
                    value=("Name: **Yuzu/Ryujinx ROMs Piracy Server**\n"
                           "➡️ Created: **15.12.2022**\n"
                           "➡️ Banned: **22.11.2023**"),
                    inline=False)

    # 2nd Server Infos
    embed.add_field(
        name="\n🕒 2nd Server (Backup)",
        value=(
            "Name: **ROMS/PIRACY 2**\n"
            "➡️ Created: **14.05.2023**\n"
            "➡️ Status: **still alive**\n"
            "🚨 **Raided on: 31.01.2024** *(Bot Token got in the wrong hands)*\n\n"
        ),
        inline=False)

    # 3rd Server Infos
    embed.add_field(name="\n✅ 3rd Server",
                    value=("**Name:** ROMS/PIRACY 3\n"
                           "✅ Läuft noch\n"),
                    inline=False)

    # Bot Laufzeit & Entwickler
    embed.add_field(
        name="⏱️ Bot-Uptime",
        value=(f"🟢 **Uptime:** {get_uptime()}\nVersion: **1.0.0**\n"),
        inline=True)
    embed.add_field(name="👨‍💻 Developer", value="`__hazegod`", inline=True)

    # Footer, Thumbnail & Author
    embed.set_footer(text="Fuck Nintendo btw 💔")
    embed.set_thumbnail(url="https://i.imgur.com/vN6kT8t.png")
    embed.set_author(name="Bot Info",
                     icon_url="https://i.imgur.com/abc123.png")

    await interaction.response.send_message(embed=embed)


# Loggt jeden Befehl mit Uhrzeit & User
def log_command(user, command_name):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {user} used /{command_name}\n")


# Zählt pro Command die Verwendung
def count_command(command_name):
    if not os.path.exists(COUNT_PATH):
        with open(COUNT_PATH, "w") as f:
            json.dump({}, f)

    with open(COUNT_PATH, "r") as f:
        counts = json.load(f)

    counts[command_name] = counts.get(command_name, 0) + 1

    with open(COUNT_PATH, "w") as f:
        json.dump(counts, f, indent=4)


# Uptime des Bots
def get_uptime():
    now = datetime.now()
    uptime = now - start_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{days} Tag{'e' if days > 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} Std")
    if minutes > 0:
        parts.append(f"{minutes} Min")
    if seconds > 0:
        parts.append(f"{seconds} Sek")

    return ", ".join(parts)


# 🔐 Bot starten
TOKEN = os.environ["TOKEN"]
if not TOKEN:
    print("❌ Kein Token gefunden.")
else:
    keep_alive()
    bot.run(TOKEN)
