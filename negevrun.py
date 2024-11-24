import os
import asyncio
import discord
from discord import app_commands, File
from typing import Optional
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.ui import Button, View
import random
from datetime import date
from dotenv import load_dotenv
from scrape_widget_1 import Scraper
from spanishdict import SpanishDictScraper
from pagination import PaginationView
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents().all()
bot = commands.Bot('++', intents=intents, self_bot = False)
@bot.event
async def on_ready():
    print("ready for action!")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=714216182508552293))
        print(f"Completed syncing {len(synced)} command(s)!")
    except Exception as e:
        print(f"Failure to sync: {e}")

#=========================================================
#Talking stuff ------------------------------------------
@bot.command(name='talk', help="Negev's lines!")
async def explode(ctx):
    explode = [
        'Combat specialist Negev reporting in!',
        'Commander, are you ready to accept my guidance?',
	'Good morning Commander. My expertise will keep you at ease anywhere.',
    "Ufufufu, sweeties, I'll give you guidance.",
    "I'll show you how the battle specialist fights!"
    ]
    response = random.choice(explode)
    await ctx.send(response)

@bot.command(name='greet', help='greets a person')
async def greet(ctx, user: discord.User):
    await ctx.send('Hello {}!'.format(user.mention))
@bot.command()
async def sun(ctx):
    for i in ctx.message.mentions:
        await i.create_dm()
        await i.dm_channel.send(file=discord.File("/home/naomi/DiscordBot/sun.jpeg"))
@bot.command()
async def author(ctx):
    await ctx.send(ctx.message.author.name)
@bot.command()
async def bang(ctx):
    for i in ctx.message.mentions:
        await ctx.message.channel.send(f"Oops! {i.name} exploded mysteriously")
#@bot.command(name='dm', help='sends a sneaky msg to @someone')
#async def dm(ctx):
#    dms = [
#	"boom boom want u in my room",
#	"watch out for a stabbing",
#	'watch out for the dynamite on your chair',
#	"Watch me bring the fire and set the night alight"
#    ]
#    response = random.choice(dms)
#    for i in ctx.message.mentions:
#        await i.create_dm()
#        await i.dm_channel.send(response)
#    await ctx.message.delete()

@bot.command(name="clear", help="delete the last n messages")
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int):
    await ctx.message.channel.send("On it Boss! Watch how a battle specialist clears the mission!")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit = amount+2)
@bot.event
async def on_message(m):
    await bot.process_commands(m)
#========================== HEBREW WOTD
@bot.tree.command(name="hello", guild=discord.Object(id=714216182508552293), description="testing slash command")
#@app_commands.describe(thing_to_say = "testing slash command")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Negev greets you, {interaction.user.mention}!")
@bot.tree.command(name="wotd", guild=discord.Object(id=714216182508552293))
@app_commands.describe(language = "Input language")
@app_commands.describe(day = "Input day")
async def paginate(interaction: discord.Interaction, day: Optional[str], language: str):
    if not day == None:
        dat = f"{day} {date.today().strftime('%B')}"
        await interaction.response.send_message(f"Fetching old {language} word of the day {dat}!")
    else:
        await interaction.response.send_message(f"Fetching {language} word of the day!")
    scraper = Scraper()
    if language == "Hebrew":
        i, wotd, titromtxt, titvowtxt, deftxt, art, lang, rom, eng, vow = scraper.scrape_link(language, day)
        pdicts = [{"Romanisation": titromtxt, "Niqqud": titvowtxt, "Part of speech?":art}]
        ex1, exh, qzm = {}, {}, {}
    else:
        i, wotd, deftxt, art, lang, eng = scraper.scrape_link(language, day)
        pdicts = [{"Part of speech?":art}]
        ex1, qzm = {}, {}
    exno = len(lang)
    qzm["WORD"] = wotd
    for k in range(exno):
        if language == "Hebrew": ex1[f"EXAMPLE {k+1}"]=vow[k]
        else: ex1[f"EXAMPLE {k+1}"]=lang[k]
        ex1[f"ENGLISH {k+1}"]=eng[k]
        if language == "Hebrew":
            exh[f"EXAMPLE {k+1}"]=lang[k]
            exh[f"ROMANISATION {k+1}"]=rom[k]
        qzm[f"EXAMPLE {k+1}"]=lang[k]
    if language == "Hebrew":
        for x in [ex1, exh, qzm]: pdicts.append(x)
    else:
        for x in [ex1, qzm]: pdicts.append(x)
    pagination_view = PaginationView(language, pdicts,"WORD OF THE DAY: "+wotd, deftxt,i, timeout=None)
    msg = await interaction.channel.send(view=pagination_view)
    await pagination_view.create_message(msg)
    await pagination_view.update_message(pagination_view.pages[0])#self.current_page
@bot.event
async def on_shutdown():
    scraper.close()
#========================== SPANISHDICT WOTD
@bot.tree.command(name="spanishdict-wotd", guild=discord.Object(id=714216182508552293))
async def spdict(interaction: discord.Interaction):
    await interaction.response.send_message(f"Fetching Spanishdict's word of the day!")
    scraper = SpanishDictScraper()
    wotd, deftxt, exsp, exen, i, bottomlink = scraper.daily()
    embed = discord.Embed(
    colour=discord.Colour.purple(),
    description="DEFINITION: "+deftxt,
    title="WORD OF THE DAY: "+wotd)

    embed.set_footer(text="Happy Spanish learning!")
    embed.set_author(name="SpanishDict", url="https://www.spanishdict.com/", icon_url="https://neodarwin-prod.sdcdns.com/img/common/apple-touch-icons/favicon-production.png")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/16022/16022729.png")
    embed.set_image(url=i)
    embed.add_field(name="EXAMPLE (Spanish)", value=exsp[0])
    embed.add_field(name="EXAMPLE (English)", value=exen[0], inline=False)
    view = View()
    button = Button(label="Learn More!", style=discord.ButtonStyle.primary, url=bottomlink)
    view.add_item(button)
    msg = await interaction.channel.send(embed=embed, view=view)
#PARANOIA------------------------------------------------
#========================================================
@bot.command(name='paranoia', help='Opens a new game of paranoia.')
async def open_paranoia(ctx):
    global channel_id_dict, open_games_dict
    channel_id = ctx.channel.id
    if channel_id not in channel_id_dict.keys():
        person = ctx.message.author.name
        message = await ctx.send('Paranoia has been opened by ' + ctx.message.author.name + ', all welcome to join.')
        message_id = message.id
        channel_id_dict[channel_id] = message_id
        open_games_dict[channel_id] = person
    else:
        await ctx.send('Paranoia already in progress here, feel free to join the game.')

@bot.command(name="add_name")
async def add_name(ctx, thenames):
    for i in ctx.message.mentions:
        open_games_dict[channel_id]
    await ctx.message.channel.send(ctx.message.content + " added to list.")

@bot.command()
async def choose(ctx):
    global names, lastname, lastlastname
    pick = random.choice(names)
    while pick == lastname or pick == lastlastname:
        pick = random.choice(names)
    lastlastname = lastname
    lastname = pick
    await ctx.message.channel.send(pick)

@bot.command()
async def reveal(ctx):
    await ctx.message.channel.send(random.choice(("Reveal", "Reveal", "No Reveal")))
bot.run(TOKEN)
