import discord
import asyncio
import time

from specs import SECRETS
from specs import FORMAL
from specs import common

client = discord.Client()

# sobald der bot online ist
@client.event
async def on_ready():
    print("Ready to rock!")
    game = discord.Game("-BEEP- I'm a human enjoying human stuff like breathing and eating -BOOP-")
    await client.change_presence(activity=game)

    client.loop.create_task(user_spam())


# sobald jemand joined
@client.event
async def on_member_join(member):

    # schickt private nachricht an member
    nachricht = discord.Embed(

        title=f"Heeey *{member.name}*, wilkommen auf unserem Discord :)",
        description="Common-Sense hat noch nie jemandem geschadet :P",
        color=discord.Color.blue()

    )
    kanal = client.get_user(member.id)
    await kanal.send(embed=nachricht)



    nachricht = discord.Embed(

        title=f"Heeey *{member.name}*, wilkommen auf unserem Discord :)",
        description="Stell dich doch bitte kurz vor ^^",
        color=discord.Color.blue()

    )

    kanal = client.get_channel(489783973271175168)
    await kanal.send(embed=nachricht)

    # weist member rolle zu
    role = discord.utils.get(member.guild.roles, name="member")
    await member.add_roles(role, atomic=True)


# liest nachrichten
@client.event
async def on_message(message):

    f = open("specs\\chatlog.txt", "a")
    f.write(f"{message.channel}\t{time.asctime()}\t{message.author}\t:\t{message.content}\n")
    f.close()

    # befehlsabfrage
    if message.content.startswith(FORMAL.PREFIX):

        # fragt whitelist ab
        if not common.WHITELIST.channels.__contains__(str(message.channel)) or not common.WHITELIST.member.__contains__(message.author.id):
            return

        
        invoke = message.content[1:]
        command = invoke.split(" ")[0]
        try:
            arg = invoke.split(" ")[1:][0]
        except IndexError:
            arg = ""

        # durchsucht befehlsliste nach befehl UND fuehrt befehl aus
        if common.cmd_dict.cmd_list.__contains__(command.upper()):
            await common.cmd_dict.cmd_list.get(command.upper()).ex(message, client, arg)
            """ common --> cmd_dict --> cmd_list --> nimmt dann das gegenstueck zu "PING" --> fuehrt dann "ex" aus"""

            f = open("specs\\log.txt", "a")
            f.write(f"{time.asctime()}\t{message.author}\t{message.author.id} \t {invoke}  \n")
            f.close()

        else:
            nachricht = discord.Embed(

                description=f"*{command}* - is not a valid command",
                color=discord.Color.blue()

            )
            await message.channel.send(embed=nachricht)

	# testcommands werden hier geprueft		
    elif message.content == "$":

        nachricht = discord.Embed(

            title="Hallo"

        )

        await message.channel.send(embed=nachricht)


#  Spambot
async def user_spam():

    while client.is_ready():
        # 586167546420658177 --> skyaaas empire
        channel = client.get_channel(586167546420658177)
        for member in channel.members:
            kanal = client.get_user(member.id)

            nachricht = discord.Embed(

                title="Heyyy, This is Skyaaa!",
                description="And I will spam you as long as you are in my channel >:D",
                color=discord.Color.blue()

            )
            await kanal.send(embed=nachricht)

        await asyncio.sleep(2)













client.run(SECRETS.TOKEN)
