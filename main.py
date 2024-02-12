import discord
from discord.ext import commands
from discord import app_commands
import discordUtils
import config
import fistof5

invalidIdError = "The given string is not a valid identifier."
msgNotFoundError = "No message has the given identifier."

try:
    g_config = config.loadFromFile("config.json")
except Exception as e:
    print(f"Could not load configuration: {e}.\nStopping here.")
    exit(1)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.tree.sync()

@bot.command()
async def sync_commands(ctx: commands.Context):
    print("Commands sync requested... ", end="")
    if ctx.author.id == g_config.ownerId:
        await bot.tree.sync()
        print("Success.")
        await ctx.send('Command tree synced.')
    else:
        print("Aborted (user not allowed).")
        await ctx.send('You must be the owner to use this command!')

@bot.tree.command(name="fistof5count",
    description="Count reactions related to a Fist of Five poll.")
@app_commands.describe(msgid="Identifier of the target poll.")
async def fistof5count(interaction: discord.Interaction, msgid: str):
    print(f"Counting Fist of Five votes on message with ID {msgid}.")
    targetMsgId = discordUtils.parseIdentifier(msgid)
    if targetMsgId is None:
        await interaction.response.send_message(content=invalidIdError, ephemeral=True)
        return
    await interaction.response.defer(thinking=True, ephemeral=True)
    try:
        targetMsg = await interaction.channel.fetch_message(targetMsgId)
    except discord.NotFound:
        await interaction.followup.send(content=msgNotFoundError, ephemeral=True)
        return
    try:
        response = await fistof5.fistof5count(interaction, targetMsg)
        await interaction.followup.send(content=response, ephemeral=True)
    except discord.HTTPException as e:
        print(e)

@bot.tree.command(name="fistof5setup",
    description="Add Fist of Five reactions from this bot on the target message.")
@app_commands.describe(msgid="Identifier of the target message.")
async def fistof5setup(interaction: discord.Interaction, msgid: str):
    print(f"Setting up Fist of Five poll on message with ID {msgid}.")
    targetMsgId = discordUtils.parseIdentifier(msgid)
    if targetMsgId is None:
        await interaction.response.send_message(content=invalidIdError, ephemeral=True)
        return
    await interaction.response.defer(thinking=True, ephemeral=True)
    try:
        targetMsg = await interaction.channel.fetch_message(targetMsgId)
    except discord.NotFound:
        await interaction.followup.send(content=msgNotFoundError, ephemeral=True)
        return
    try:
        response = await fistof5.fistof5setup(interaction, targetMsg)
        await interaction.followup.send(content=response, ephemeral=True)
    except discord.HTTPException as e:
        print(e)

@bot.tree.context_menu(name="Fist of 5 - Set up")
async def fistof5countmenu(interaction: discord.Interaction, message: discord.Message):
    print(f"Setting up Fist of Five poll on message with ID {message.id}.")
    await interaction.response.defer(thinking=True, ephemeral=True)
    response = await fistof5.fistof5setup(interaction, message)
    await interaction.followup.send(content=response, ephemeral=True)
    
@bot.tree.context_menu(name="Fist of 5 - Count votes")
async def fistof5setupmenu(interaction: discord.Interaction, message: discord.Message):
    print(f"Counting Fist of Five votes on message with ID {message.id}.")
    await interaction.response.defer(thinking=True, ephemeral=True)
    response = await fistof5.fistof5count(interaction, message)
    await interaction.followup.send(content=response, ephemeral=True)
  
bot.run(g_config.botToken)
