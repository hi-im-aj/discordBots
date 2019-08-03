import discord,asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import requests as req
import bs4 as bs
import json as jso
from random import randint as raI
print("Initializing bot...")
zot_prefix = "z!"
zot_channellist = [
    ""]
zot_commandlist = [
    "z",
    "numtrivia",
    "cat",
    "quotes",
    "calc",
    "roll",
    "purge"]
def zot_commands():
    return str("Commands:\n" + ", ".join(zot_commandlist)) + "."
def zot_nulpermission():
    return "You do not have permission to use this command"
def zot_z():
    return ":regional_indicator_z:"
def zot_numtrivia():
    response = req.get("http://numbersapi.com/random/trivia")
    text = response.text
    if str(response) != "<Response [200]>":
        return "Oops, something went wrong..."
    else:
        return text
def zot_cat():
    xmlurl = "http://thecatapi.com/api/images/get?format=xml&results_per_page=1"
    response = req.get(xmlurl)
    responsetxt = response.text
    soup = bs.BeautifulSoup(responsetxt,"lxml")
    link = str(soup.find_all("url"))
    link = link.lstrip("[<url>")
    link = link.rstrip("</url>]")
    return link
def zot_quotes():
    url = "http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1"
    response = req.get(url)
    responsetxt = response.text
    dataDict = response.json()
    dataDict = dataDict[0]
    name = dataDict["title"]
    content = dataDict["content"]
    content = content.lstrip("<p>")
    content = content.rstrip("<\/p>\n")
    x = "{}:\n{}".format(name,content)
    x = x.replace("&#8217;","'")
    x = x.replace("&#8211;","-")
    return x
def zot_coinflip():
    pass
def zot_roll(MAID):
    x = raI(0,100)
    x = "<@{}> ".format(MAID) + str(x)
    return x
def zot_tictactoe():
    pass
Client = discord.Client()
client = commands.Bot(command_prefix = zot_prefix)
@client.event
async def on_ready():
    print("Done.")
@client.event
async def on_message(message):
    strMCha = str(message.channel.id)
    MCha = message.channel
    MCon = message.content
    if not strMCha in zot_channellist:
        if message.content.lower().startswith(zot_prefix + "help"):
            await client.send_message(message.channel,zot_commands())
        elif message.content.lower().startswith(zot_prefix + "z"):
            if "454281884780855297" in [role.id for q in message.author.roles]:
                await client.send_message(message.channel,zot_z())
            else:
                await client.send_message(message.channel,zot_nulpermission())
        elif message.content.lower().startswith(zot_prefix + "numt"):
            await client.send_message(message.channel,zot_numtrivia())
        elif message.content.lower().startswith(zot_prefix + "cat"):
            await client.send_message(message.channel,zot_cat())
        elif message.content.lower().startswith(zot_prefix + "quo"):
            await client.send_message(message.channel,zot_quotes())
        elif message.content.lower().startswith(zot_prefix + "calc"):
            await client.send_message(message.channel,eval(message.content.lstrip(zot_prefix + "calc")))
        elif message.content.lower().startswith(zot_prefix + "roll"):
            MAID = message.author.id
            await client.send_message(message.channel,zot_roll(MAID))
        elif message.content.lower().startswith(zot_prefix + "purge"):
            MContentInteger = [int(i) for i in MCon.split() if i.isdigit()]
            MContentInteger = MContentInteger[-1] + 1
            await client.purge_from(MCha, limit=MContentInteger, check=None, before=None, after=None, around=None)
    else:
        pass
client.run("")
