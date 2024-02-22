import os
import discord
import asyncio
import random
from discord.ext import commands
import typing
####################
#For Web-Scraping
from bs4 import BeautifulSoup
import requests
#API for HowLongToBeat
from howlongtobeatpy import HowLongToBeat
####################

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('Game-Bot is ready')
    await client.change_presence(activity=discord.Game(name="Game Boy"))

@client.event #Legacy
async def on_message(message):
    if message.author == client.user:
        return

@tree.command(name="ping", description="ping command")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f" GAME-BOT LATENCY:: [{round(client.latency * 1000)}ms]")

@tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == 'your discord user ID': #ensure to put your discord user ID here
        await tree.sync()
        print('Command tree synced.')
        await interaction.response.send_message('Commands Sync Complete. The sync may take up to an hour to complete') #This all depends on discords servers, as this is a global sync
    else:
        await interaction.response.send_message('You must be the owner to use this command!')

####################
# How Long To Beat: Game Time Lookups/Web-scraping
####################

@tree.command(name="hltb", description="Get info on how long a game is to beat")
async def hltb(interaction: discord.Interaction, game: str):
	# join the args into a single string for the HLTB API to parse
    title = ' '.join(str(i) for i in {game})
    #title = str({game})
    print(title)
	#print(title)
    def getURL(title):
		# Put the Title through the HLTB API and grab the best result. This was taken whole cloth from the examples
        results = HowLongToBeat().search(title, similarity_case_sensitive=False)
        if results is not None and len(results) > 0:
                best_element = max(results, key=lambda element: element.similarity)
                return best_element
        else:
                return None
    game = getURL(title)
    if game != None:
        link = str(game.game_web_link)
    else:
        await interaction.response.send_message("Game: '" + title + "' is not found")
        return
	# Now the web-scraping begins, using BeautifulSoup we need to parse it first
    page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'})
	# print(page)
    soup = BeautifulSoup(page.content, 'html.parser')
	#----------------------
	# GETTING THE GAME INFO
    results = soup.find_all("h5") #finding all h5 elements and setting them into variables
    MainStory = results[0].get_text()
    MainPlus = results[1].get_text()
    Completionist = results[2].get_text()
    AllStyles = results[3].get_text()
	# ---------------------
	# GETTING THE GAME TITLE
    #G_title = ' '.join(list(title))
	# GETTING THE GAME ICON
    game_images = soup.find_all("img")
    images = game_images[0]
    image = images['src']
		#-----------------------
	# CREATING THE EMBEDED ELEMENT
    embed=discord.Embed(title=title, url=link, description="", color=0x1300d9)
    embed.set_thumbnail(url=image)
    embed.add_field(name="Main Story", value=MainStory, inline=True)
    embed.add_field(name="Main Story Plus", value=MainPlus, inline=True)
    embed.add_field(name="Completionist", value=Completionist, inline=True)
    embed.add_field(name="All Styles", value=AllStyles, inline=True)
    embed.set_footer(text="howlongtobeat.com")
    await interaction.response.send_message(embed=embed)
####################

client.run('BOT TOKEN')
