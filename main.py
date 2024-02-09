import os
import discord
from discord.ext import commands

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

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def count_votes(ctx, targetMsgId):
    print("Received ID "+targetMsgId)
    watchedUsers = list(ctx.guild.get_role(watchedRoleId).members)
    watchedUsers.sort(key=lambda u: u.display_name)
    noReactionUserIds = set([u.id for u in watchedUsers])
    try:
        reactionsUsernames = dict.fromkeys(watchedEmojis, [])
        targetMsg = await ctx.channel.fetch_message(targetMsgId)
        for reaction in targetMsg.reactions:
            if (reaction.emoji in watchedEmojis):
                reactionUsers = [u async for u in reaction.users()]
                reactionsUsernames[reaction.emoji] = [u.display_name for u in reactionUsers]
                noReactionUserIds -= set([u.id for u in reactionUsers])
        outputMsg =\
            "\n".join([\
                (emoji + " (" + str(len(usernames)) + "): " + ", ".join(usernames))\
                    for (emoji, usernames) in reactionsUsernames.items()])\
            + "\n"
        if any(noReactionUserIds):
            outputMsg += "**Missing votes:** " + ", ".join([u.display_name for u in watchedUsers if u.id in noReactionUserIds])
        else:
            outputMsg += "**Everyone has voted!**"
        await ctx.channel.send(outputMsg)
    except discord.NotFound:
        pass

bot.run(os.getenv("TOKEN"))
