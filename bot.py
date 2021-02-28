import os
import logging
from random import randint
import discord
from discord.ext import commands
from dotenv import load_dotenv
from models import Minion
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Menciones de roles
# <@&519330250535075840> GORDO BONDIOLA
# <@&507347964444934169> GORDEUS
# <@&700084198924353576> GORDO MAESTRO


# Constantes
GORDO_BONDIOLA = "<@&519330250535075840>"
GORDEUS = ""
IMPUNES = ['GORDO MAESTRO', 'GORDO BONDIOLA', 'GORDEUS']
PREFIX = '*'
MODO_VIOLENTO = False


# Inicializacion
logging.basicConfig(level=logging.INFO)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=PREFIX)
# TODO: Agregar schema de la tabla para que SQLAlchemy la reconozca en la base. Forro.
engine = create_engine('sqlite:///gorra-db.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


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
    logging.info("  - MENSAJE DE DS")
    logging.info("***********************************************************")
    logging.info(f"      Mensaje:      {message_content}")
    logging.info(f"      Autor:        {author}")
    logging.info(f"      Canal:        {message_channel_name}")
    logging.info("***********************************************************")
    if MODO_VIOLENTO:
        if message.author == bot.user:
            return
        num = randint(1, 1000)
        if num > 500:
            await message_channel.send(f"{str(author.mention)} DNI y rol o te rompo la traquea")

    if author_last_role not in IMPUNES:
        if (message_content.startswith('-p') or message_content.startswith('>')) and \
        message_channel_name != 'musica':
            await message_channel.send(f'{GORDO_BONDIOLA} *Chst! Aca hay un ladri que se esta ganando una bala.*')
            minion = Minion(username='Test', full_username='TestFull', mention_in_server='<@!12873912>', strikes=1)
            session.add(minion)
            session.commit()
        elif message_content.startswith('$') and \
            message_channel_name != 'waifus':
            await message_channel.send(f'{GORDO_BONDIOLA} Chst! Aca hay un ladri que se esta ganando una bala.')
    if message.content.startswith("<@!" + str(bot.user.id) + ">"):
        await message_channel.send(f"Que onda pa, tira: `{PREFIX}help` o `{PREFIX}info`")
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send("test")


@bot.command(name='ping', help='Para saber si esta vivo el bot')
async def ping(ctx):
    await ctx.send('Pong :ping_pong:')


@bot.command(name='reglas')
async def reglas(ctx):
    await ctx.send('Memorizalas: #reglas')


@commands.has_any_role('GORDO BONDIOLA', 'GORDEUS')
@bot.command(name='indultar', help=f'Limpia los antecedentes del civil. Ejemplo: `{PREFIX}indultar @usuario`')
async def indultar(ctx):
    content = ctx.message.content.split(" ")
    try:
        user_to_pardon = content[1]
        # Borramos los registros que coincidan con user_to_pardon
    except IndexError:
        await ctx.send('Me falta el ladri a perdonar')


@bot.command(name='enlamira')
async def enlamira(ctx):
    await ctx.send('Test')


@bot.command(name='paraexiliar')
async def paraexiliar(ctx):
    await ctx.send('Test')


@bot.event
async def on_command_error(ctx, error):
    response = 'Flasheaste rey :sunglasses: tira `>help` y anda memorizando. Gil.'
    logging.error("  - ERROR DE COMANDO")
    logging.error("***********************************************************")
    logging.error(f"        {error}")
    logging.error("***********************************************************")
    await ctx.send(response)


if __name__ == "__main__":
    bot.run(TOKEN)
