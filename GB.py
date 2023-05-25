####################
# Importing all the important libraries
####################
import os
import discord
import asyncio
import random
from discord.ext import commands
#For Web-Scraping
from bs4 import BeautifulSoup
import requests
#API for HowLongToBeat
from howlongtobeatpy import HowLongToBeat

#VARIABLES
SCORES = {}
MUSIC_COMMANDS = ['game-bot play some music', 'gamebot play some music', 'game-bot play music', 'gamebot play music', 'game-bot music', 'gamebot music']
song = []

# Setting bot prefix and complying with Discord API standards
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '?', intents=intents)

####################
# Events/Keyword Triggers
####################

@bot.event
async def on_ready():
	print('Game-Bot is ready')
	await bot.change_presence(activity=discord.Game(name="Game Boy"))

#The on_message event lets the bot listen for certain key-words
@bot.event
async def on_message(message):
	# To ensure the bot can't respond to itself thus preventing command loops
	if message.author == bot.user:
		return
	if any(x in message.content.lower() for x in MUSIC_COMMANDS):
		####################
		# The Music Playing Feature
		####################
		await message.channel.send('Choose a game franchise from the following list:')
		file = open("text/music_list.txt")
		music_list = file.read().split('\n')
		file.close()
		music_list.remove("")
		await message.channel.send(music_list)
		#------------------------------------
		def game_music(arg): # Command searches for requested game text file and posts random link from it
			global song
			file = open("text/games/" + arg + ".txt")
			music = file.read().split('\n')
			file.close()
			music.remove("")
			song = random.choice(music)
			print(song)
		def is_correct(m):
			return m.author == message.author
		#------------------------------------
		# Stops bot from waiting forever
		try:
			entry = await bot.wait_for('message', check=is_correct, timeout=13.0)
		except asyncio.TimeoutError:
			return await ctx.send("Sorry you took too long")
		choice = entry.content.lower()
		# In this section, change the "choice == "GAME TITLE"" with the games you chose to have in the text/games folder
		# for "game_music(X)", make sure X matches your game list text files
		if choice == "fire emblem":
			game_music('fe')
			await message.channel.send(song)
		if choice == "persona":
			game_music('persona')
			await message.channel.send(song)
		if choice == "mario":
			game_music('mario')
			await message.channel.send(song)
		if choice == "zelda":
			game_music('zelda')
			await message.channel.send(song)
		if choice == "star fox":
			game_music('starfox')
			await message.channel.send(song)
		if choice == "ace attorney":
			game_music('aceattorney')
			await message.channel.send(song)
		if choice == "kingdom hearts":
			game_music('kingdomhearts')
			await message.channel.send(song)
		if choice == "assassins creed":
			game_music('seashanties')
			await message.channel.send(song)
		if choice == "katamari demacy":
			game_music('katamari')
			await message.channel.send(song)
		if choice == "splatoon":
			game_music('splatoon')
			await message.channel.send(song)
	#This line is necessary, otherwise it will play this event only when receiving messages and ignore the commands
	await bot.process_commands(message)

####################
# Commands
####################
#Asynchronous functions where the trigger word is the name of the function(ctx).
#Then the function sends message with the ctx.send()

#COMMANDS
@bot.command()
async def ping(ctx):
#I use an f string to issue a ping command
	await ctx.send(f" GAME-BOT LATENCY:: [{round(bot.latency * 1000)}ms]")

#--------------------------------------------------------------------------#
####################
# SCOREBOARD FUNCTIONALITY
####################
@bot.command()
#put the role in here that you want to give scoreboard access to
@commands.has_any_role('Admin')
async def score(ctx, arg):
	global SCORES
	user = arg.lower()
	if user in SCORES:
		if SCORES[user] == 4:
			await ctx.send(user + ' WINS! Scoreboard will reset now')
			SCORES = {}
		else:
			SCORES[user] += 1
			await ctx.send(user + ' +1 point')
	else:
		SCORES[user] = 1
		await ctx.send(user + ' Yay! Your first point!')

@bot.command()
#put the role in here that you want to give scoreboard access to
@commands.has_any_role('Admin')
async def remove_score(ctx, arg):
	global SCORES
	user = arg.lower()
	if user in SCORES:
		SCORES[user] -= 1
		await ctx.send(user + " -1 point")
	else:
		await ctx.send(user + " not on the scoreboard")
@bot.command()
#put the role in here that you want to give scoreboard access to
@commands.has_any_role('Admin')
async def clear_scores(ctx):
	global SCORES
	SCORES = {}
	await ctx.send("scoreboard cleared")

@bot.command()
async def scores(ctx):
	if SCORES == {}:
		await ctx.send('No one has any points yet')
	else:
		await ctx.send('Points are as follows {USER : POINTS}:')
		await ctx.send(SCORES)
#-------------------------------------------------------------------#
####################
# How Long To Beat: Game Time Lookups/Web-scraping
####################
@bot.command()
async def hltb(ctx, *args):
        # join the args into a single string for the HLTB API to parse
        title = ' '.join(str(i) for i in args)
        #print(title)
        def getURL(title):
                # Put the Title through the HLTB API and grab the best result. This was taken whole cloth from the examples
                results = HowLongToBeat().search(title, similarity_case_sensitive=False)
                if results is not None and len(results) > 0:
                        best_element = max(results, key=lambda element: element.similarity)
                        return best_element
                else:
                        print('something is wrong')
                        return None
        game = getURL(title)
        link = str(game.game_web_link)
        #print(link)
        # Now the web-scraping begins using BeautifulSoup we need to parse it first
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
        G_title = ' '.join(list(title))
        # GETTING THE GAME ICON
        game_images = soup.find_all("img")
        images = game_images[0]
        image = images['src']
                #-----------------------
        # CREATING THE EMBEDED ELEMENT
        embed=discord.Embed(title=G_title, url=link, description="", color=0x1300d9)
        embed.set_thumbnail(url=image)
        embed.add_field(name="Main Story", value=MainStory, inline=True)
        embed.add_field(name="Main Story Plus", value=MainPlus, inline=True)
        embed.add_field(name="Completionist", value=Completionist, inline=True)
        embed.add_field(name="All Styles", value=AllStyles, inline=True)
        embed.set_footer(text="howlongtobeat.com")
        await ctx.send(embed=embed)

#Runs the bot and authorizes the bot with it's unique token
bot.run('BOT TOKEN')
