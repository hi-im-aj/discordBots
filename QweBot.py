import discord,youtube_dl
from discord.ext import commands as cmds
import requests as req
import bs4 as bs
from random import randint as rai

TOKEN = ""
prefix = "q!"
client = cmds.Bot(command_prefix = prefix)

players = {}

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="{}help".format(prefix)))
    print("Ready")

@client.command()
async def cat():
    try:
        xmlurl = "http://thecatapi.com/api/images/get?format=xml&results_per_page=1"
        response = req.get(xmlurl)
        responsetxt = response.text
        soup = bs.BeautifulSoup(responsetxt,"lxml")
        link = str(soup.find_all("url"))
        link = link.lstrip("[<url>")
        link = link.rstrip("</url>]")
        await client.say(link)
    except:
        await client.say("Seems like the servers are down...")
@client.command(pass_context=True)
async def roll(ctx):
    author = ctx.message.author.id
    roll = rai(0,100)
    roll = "<@{}> {}".format(author,roll)
    await client.say(roll)
@client.command(pass_context=True)
async def calc(ctx):
    content = ctx.message.content
    calc = eval(content.lstrip(prefix+"calc"))
    await client.say(calc)
@client.command(pass_context=True)
async def purge(ctx,amount="1"):
    if amount.isdigit():
        await client.purge_from(ctx.message.channel,limit=int(amount)+1)
    else:
        await client.say("error")
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
@client.command(pass_context=True)
async def play(ctx,url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

client.run(TOKEN)
