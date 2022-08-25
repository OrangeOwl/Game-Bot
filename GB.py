import os
import discord
import asyncio
#import requests
import random
from discord.ext import commands
#For Web-Scraping
from bs4 import BeautifulSoup
import requests
#A Google Search API
from duckduckgo_search import ddg

#VARIABLES
SCORES = {}
MUSIC_COMMANDS = ['game-bot play some music', 'gamebot play some music', 'game-bot play music', 'gamebot play music', 'game-bot music', 'gamebot music']
song = []
#COMMAND WORDS TO LISTEN FOR

intents = discord.Intents.default()
bot = commands.Bot(command_prefix = '?', intents=intents)

#EVENTS
#A terminal command that lets me know the bot is running in the terminal
@bot.event
async def on_ready():
	print('Game-Bot is ready')
	await bot.change_presence(activity=discord.Game(name="Game Boy"))

#The on_message event lets the bot listen for certain key-words
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if any(x in message.content.lower() for x in MUSIC_COMMANDS):
		await message.channel.send('Choose a game franchise from the following list:')
		file = open("text/music_list.txt")
		music_list = file.read().split('\n')
		file.close()
		music_list.remove("")
		await message.channel.send(music_list)
		#------------------------------------
		def game_music(arg):
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

#COMMANDS: Asynchronous functions where the trigger word is the name of the function(ctx).
#Then the function sends message with the ctx.send()

#COMMANDS
@bot.command()
async def ping(ctx):
#I use an f string to issue a ping command
	await ctx.send(f" GAME-BOT LATENCY:: [{round(bot.latency * 1000)}ms]")

#--------------------------------------------------------------------------#
# SCOREBOARD FUNCTIONALITY
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
@bot.command()
async def hltb(ctx, *args):
	# grab the first search result for the game (99% of the time is the proper HLTB website page you want)
	title = args
	query = "howlongtobeat.com" + str(title)
	raw_result = ddg(query, safesearch='Moderate', time=None, max_results=1, output=None)
	result = str(raw_result[0])
	result_list = result.split(',')
	raw_link = str(result_list[1])
	link_list = raw_link.split(':')
	link = "https:" + str(link_list[2])[:-1]
	# for link in search(query, num_results=1):
	# Now the web-scraping begins
	page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(page.content, 'html.parser')
	#----------------------
	# GETTING THE GAME INFO
	results = soup.find_all("div", {"class": "game_times"})
	info = results[0]
	INFO = info.get_text()
		#-----------------------
		# GETTING THE GAME TITLE
	game_title = soup.find("title")
	G_TITLE = game_title.get_text()
		#-----------------------
		# GETTING THE GAME ICON
	game_images = soup.find_all("img", {"alt": "Box Art"})
	images = game_images[0]
	image = images['src']
	print(image)
		#-----------------------
	embed=discord.Embed(title=G_TITLE, url=link, description="", color=0x1300d9)
	embed.set_thumbnail(url="https://howlongtobeat.com" + image)
	embed.add_field(name="Estimated Completion Time", value=INFO, inline=True)
	embed.set_footer(text="howlongtobeat.com")
	await ctx.send(embed=embed)

#Runs the bot and authorizes the bot with it's unique token
bot.run('ODA0OTM4MTg0Njk3NzA4NTY1.YBTnGg.8kqBNrzUu7ra3aM1kOdvHf2yOZ4')
