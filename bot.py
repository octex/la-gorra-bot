import os
import logging
from random import randint
import discord
from discord.ext import commands
from dotenv import load_dotenv

IMPUNES = ['GORDO MAESTRO', 'GORDO BONDIOLA', 'GORDEUS']
PREFIX = '<'
MODO_VIOLENTO = True

# @commands.has_role('admin')
logging.basicConfig(level=logging.INFO)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=PREFIX)


@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    author = message.author
    author_roles = message.author.roles
    author_last_role = author_roles[-1]
    message_channel_name = str(message.channel)
    message_channel = message.channel
    message_content = message.content

    if MODO_VIOLENTO:
        if message.author == bot.user:
            return
        num = randint(1, 1000)
        if num > 500:
            await message_channel.send(f"{str(author.mention)} DNI y rol o te rompo la traquea")

    if author_last_role not in IMPUNES:
        if (message_content.startswith('-p') or message_content.startswith('>')) and \
        message_channel_name != 'musica':
            await message_channel.send('Que onda chabon, flasheaste! (musica)')
        elif message_content.startswith('$') and \
            message_channel_name != 'waifus':
            await message_channel.send('Que onda chabon, flasheaste! (waifus)')
    if message.content.startswith("<@!" + str(bot.user.id) + ">"):
        await message_channel.send(f"Buenas pingo feo, tira: `{PREFIX}help` o `{PREFIX}info`")
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send("test")


@bot.command(name='ping', help='Para saber si esta vivo el bot')
async def ping(ctx):
    await ctx.send('Pong :ping_pong:')


@bot.command(name='ban')
@commands.has_role('GORDEUS')
@commands.has_role('GORDO BONDIOLA')
async def ban(ctx):
    await ctx.send('ban test')

@bot.event
async def on_command_error(ctx, error):
    response = 'Flasheaste rey :sunglasses: tira `>help` y anda memorizando. Gil.'
    await ctx.send(response)

"""
    El bot va a contar con las siguientes funcionalidades:
        - Una base de datos de exiliados, en la mira
        - Detector de infracciones
        - Comando de reglas
        - Respuestas automatizadas
        - Lista de exiliados
        - Lista de antecedentes
        - Lista de moderadores
        - Ayuda con los roles
"""

bot.run(TOKEN)
