import discord
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = 1338866926952120412  

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Slash Commands nur für einen bestimmten Server synchronisieren
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print("✅ Slash-Commands synchronisiert!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

#  /ping
@bot.tree.command(name="info", description="Get all informations about the Server")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message("There are no informations yet!")

# /dm
@bot.tree.command(name="dm", description="Sends you a private message.")
@app_commands.describe(text="Der Text, den du per DM erhalten willst")
async def dm(interaction: discord.Interaction, text: str):
    try:
        await interaction.user.send(f"📬\nHi, this is your request:\n{text}")
        await interaction.response.send_message("✅ DM was send!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I couldn't send you a DM.\nDMs deactivated?", ephemeral=True)
        
# /rom-list
@bot.tree.command(name="rom-list", description="Get a list of available ROMs\nDatei.txt")
async def romlist(interaction: discord.Interaction):
    try:
        await interaction.user.send(f"\nHi, here is a list of all current available ROMs.\nIf the ROM you want is not on the list, you can request it here:\nhttps://discord.com/channels/1338866926952120412/1338866928487366752")
        await interaction.response.send_message("✅ Check DM", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I couldn't send you a DM.\nDMs deactivated?", ephemeral=True)
    
# 🔐 Bot starten
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("❌ Kein Token in .env gefunden.")
else:
    bot.run(TOKEN)