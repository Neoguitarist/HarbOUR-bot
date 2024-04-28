import datetime
import discord
import config

try:
    appConfig = config.loadFromFile("config.json")
except Exception as e:
    print(f"Could not load configuration: {e}.\nStopping here.")
    exit(1)

messageMaxLength = 2000
emoji0 = "0️⃣"
emoji1 = "1️⃣"
emoji2 = "2️⃣"
emoji3 = "3️⃣"
emoji4 = "4️⃣"
emoji5 = "5️⃣"
emojiCheck = "✅"
voteEmojis = [emoji0, emoji1, emoji2, emoji3, emoji4, emoji5]
watchedRoleId = 1162008885725511790
propositionHistoryDaySpan = datetime.timedelta(days=30)

def buildEmojiCountStr(emoji, usernames):
    res = emoji + " (" + str(len(usernames)) + "): "
    res += ", ".join(usernames) if any(usernames) else "_no one_"
    return res

async def fistof5count(interaction: discord.Interaction, message: discord.Message):
    watchedUsers = list(interaction.guild.get_role(watchedRoleId).members)
    watchedUserIds = set([u.id for u in watchedUsers])
    watchedUsers.sort(key=lambda u: u.display_name)
    noReactionUserIds = set([u.id for u in watchedUsers])
    reactionsUsernames = dict.fromkeys(voteEmojis, [])
    for reaction in message.reactions:
        if (reaction.emoji in voteEmojis):
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
    for emoji in voteEmojis:
        await message.add_reaction(emoji)
    return "Done."

async def fistof5missingme(interaction: discord.Interaction):
    outputMsg = None
    lookupStartDate = datetime.datetime.today()-propositionHistoryDaySpan
    messagesMissingVote = list[discord.Message]()
    async for message in interaction.channel.history(after=lookupStartDate):
        isProposition = False
        voteFound = False
        for reaction in message.reactions:
            # Consider messages with a check mark as voted,
            # since the possible proposition is already accepted.
            if (reaction.emoji == emojiCheck):
                voteFound = True
                break
            if (reaction.emoji in voteEmojis):
                reactionUsers = set([u.id async for u in reaction.users()])
                if (appConfig.appId in reactionUsers):
                    isProposition = True
                if (interaction.user.id in reactionUsers):
                    voteFound = True
                    break
        if (isProposition and not voteFound):
            messagesMissingVote.append(message)
    if any(messagesMissingVote):
        outputMsg = "Your vote is missing on the following propositions:\n"\
            + "\n".join([message.jump_url for message in messagesMissingVote])\
            + "\n"
    else:
        outputMsg = "There are no proposition waiting for your vote."
    return outputMsg[:messageMaxLength]
