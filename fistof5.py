import discord

emoji0 = "0️⃣"
emoji1 = "1️⃣"
emoji2 = "2️⃣"
emoji3 = "3️⃣"
emoji4 = "4️⃣"
emoji5 = "5️⃣"
watchedEmojis = [emoji0, emoji1, emoji2, emoji3, emoji4, emoji5]
watchedRoleId = 1162008885725511790

def buildEmojiCountStr(emoji, usernames):
    res = emoji + " (" + str(len(usernames)) + "): "
    res += ", ".join(usernames) if any(usernames) else "_no one_"
    return res

async def fistof5count(interaction: discord.Interaction, message: discord.Message):
    watchedUsers = list(interaction.guild.get_role(watchedRoleId).members)
    watchedUserIds = set([u.id for u in watchedUsers])
    watchedUsers.sort(key=lambda u: u.display_name)
    noReactionUserIds = set([u.id for u in watchedUsers])
    reactionsUsernames = dict.fromkeys(watchedEmojis, [])
    for reaction in message.reactions:
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
    return outputMsg

async def fistof5setup(interaction: discord.Interaction, message: discord.Message):
    for emoji in watchedEmojis:
        await message.add_reaction(emoji)
    return "Done."
