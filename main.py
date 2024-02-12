import discord
from discord.ext import commands
from discord import app_commands
import config

try:
    config = config.loadFromFile("config.2json")
except Exception as e:
    print(f"Could not load configuration: {e}.\nStopping here.")
    exit(1)

msgNotFoundError = "No message has the given identifier."

emoji0 = "0️⃣"
emoji1 = "1️⃣"
emoji2 = "2️⃣"
emoji3 = "3️⃣"
emoji4 = "4️⃣"
emoji5 = "5️⃣"
watchedEmojis = [emoji0, emoji1, emoji2, emoji3, emoji4, emoji5]
watchedRoleId = 1162008885725511790

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def sync_commands(ctx: commands.Context):
    print("Commands sync requested... ", end="")
    if ctx.author.id == 654739217326276638:
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
    targetMsgId = int(msgid)
    watchedUsers = list(interaction.guild.get_role(watchedRoleId).members)
    watchedUserIds = set([u.id for u in watchedUsers])
    watchedUsers.sort(key=lambda u: u.display_name)
    noReactionUserIds = set([u.id for u in watchedUsers])
    try:
        await interaction.response.defer(thinking=True, ephemeral=True)
        reactionsUsernames = dict.fromkeys(watchedEmojis, [])
        targetMsg = await interaction.channel.fetch_message(targetMsgId)
        for reaction in targetMsg.reactions:
            if (reaction.emoji in watchedEmojis):
                reactionUsers = [u async for u in reaction.users() if u.id in watchedUserIds]
                reactionsUsernames[reaction.emoji] = [u.display_name for u in reactionUsers]
                noReactionUserIds -= set([u.id for u in reactionUsers])
        outputMsg =\
            "\n".join([\
                buildEmojiCountStr(emoji, usernames)\
                    for (emoji, usernames) in reactionsUsernames.items()])\
            + "\n"
        if any(noReactionUserIds):
            outputMsg += "**Missing votes:** " + ", ".join([u.display_name for u in watchedUsers if u.id in noReactionUserIds])
        else:
            outputMsg += "**Everyone has voted!**"
        await interaction.followup.send(content=outputMsg, ephemeral=True)
    except discord.NotFound:
        await interaction.followup.send(content=msgNotFoundError, ephemeral=True)
    except discord.HTTPException as e:
        print(e)

@bot.tree.command(name="fistof5setup",
    description="Add Fist of Five reactions from this bot on the target message.")
@app_commands.describe(msgid="Identifier of the target message.")
async def fistof5setup(interaction: discord.Interaction, msgid: str):
    print(f"Setting up Fist of Five poll on message with ID {msgid}.")
    targetMsgId = int(msgid)
    try:
        await interaction.response.defer(thinking=True, ephemeral=True)
        targetMsg = await interaction.channel.fetch_message(targetMsgId)
        for emoji in watchedEmojis:
            await targetMsg.add_reaction(emoji)
        await interaction.followup.send(content="Done.", ephemeral=True)
    except discord.NotFound:
        await interaction.followup.send(content=msgNotFoundError, ephemeral=True)
    except discord.HTTPException as e:
        print(e)

def buildEmojiCountStr(emoji, usernames):
    res = emoji + " (" + str(len(usernames)) + "): "
    res += ", ".join(usernames) if any(usernames) else "_no one_"
    return res

bot.run(config.botToken)
