import os
import logging
from random import randint
import discord
from discord.ext import commands
from dotenv import load_dotenv
from models import Minion, BotConfig
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from utils import ascii_logo, load_config_table


# Inicializacion
logging.basicConfig(level=logging.INFO)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_PATH = os.getenv('DB_PATH')
SQL_CONFIG_PATH = os.getenv('SQL_CONFIG_PATH')
engine = create_engine(DB_PATH, echo=True)

config = open(SQL_CONFIG_PATH)
load_config_table(config=config, engine=engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


# Constantes
PREFIX = session.query(BotConfig).filter_by(keyConfig='prefix').first().value
GORDEUS = session.query(BotConfig).filter_by(keyConfig='admin_role_mention').first().value
GORDO_BONDIOLA = session.query(BotConfig).filter_by(keyConfig='mod_role_mention').first().value
REGLAS_CHANNEL = session.query(BotConfig).filter_by(keyConfig='rules_channel').first().value
IMPUNES = ['GORDO MAESTRO', 'GORDO BONDIOLA', 'GORDEUS']
# MODO_VIOLENTO = False


bot = commands.Bot(command_prefix=PREFIX)


@bot.event
async def on_ready():
    ascii_logo()
    logging.info(f'{bot.user} has connected to Discord!')


async def registro_civil(author, author_name, author_mention, message_channel):
    minion_q = session.query(Minion).filter_by(username=author_name).first()
    if minion_q:
        minion_q.strikes = minion_q.strikes + 1
        session.add(minion_q)
        session.commit()
        await message_channel.send(f'{author_mention} Guarda amigo que vas por {minion_q.strikes} strikes')
    else:
        minion_n = Minion(username=str(author_name), full_username=str(author), mention_in_server=str(author_mention), strikes=1)
        session.add(minion_n)
        session.commit()
        await message_channel.send(f'{author_mention} Primer strike, tene cuidado...')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    author = message.author
    author_name = str(author).split("#")[0]
    author_mention = author.mention
    author_roles = author.roles
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
    # if MODO_VIOLENTO:
    #     if message.author == bot.user:
    #         return
    #     num = randint(1, 1000)
    #     if num > 500:
    #         await message_channel.send(f"{str(author.mention)} DNI y rol o te rompo la traquea")

    if author_last_role not in IMPUNES:
        if (message_content.startswith('-p') or message_content.startswith('>p')) and \
        message_channel_name != 'musica' or message_content.startswith('-skip') or message_content.startswith('>skip'):
            await message_channel.send(f'{GORDO_BONDIOLA} Chst! Aca hay un ladri que se esta ganando una bala.')
            await registro_civil(author=author, author_name=author_name, author_mention=author_mention,
                                 message_channel=message_channel)
        elif message_content.startswith('$w') and \
            message_channel_name != 'waifus':
            await message_channel.send(f'{GORDO_BONDIOLA} Chst! Aca hay un ladri que se esta ganando una bala.')
            await registro_civil(author=author, author_name=author_name, author_mention=author_mention,
                                 message_channel=message_channel)
    if message_content.startswith('sale') or message_content.startswith('Sale'):
        await message_channel.send(f"Sale pa :sunglasses:")
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
    await ctx.send(f'Memorizalas: {REGLAS_CHANNEL}')


@commands.has_any_role('GORDO BONDIOLA', 'GORDEUS')
@bot.command(name='indultar', help=f'Limpia los antecedentes del civil. Ejemplo: {PREFIX}indultar @usuario. Si el lokito no esta en el servidor, pasame el usuario con el tag SIN el arroba, ejemplo: {PREFIX}indultar molymolyProd#1234')
async def indultar(ctx):
    content = ctx.message.content.split(" ")
    try:
        user_to_pardon = content[1]
        minion_to_pardon = session.query(Minion).filter_by(mention_in_server=user_to_pardon).first()
        if minion_to_pardon is None:
            await ctx.send('No lo registro a este che.')
        else:
            session.delete(minion_to_pardon)
            session.commit()
            await ctx.send(f'{user_to_pardon} tas indultado pa.')
    except IndexError:
        await ctx.send('Me falta el ladri a indultar')


@bot.command(name='enlamira')
async def enlamira(ctx):
    await ctx.send('Test')


@bot.command(name='alparedon')
async def alparedon(ctx):
    await ctx.send('Test')


@bot.event
async def on_command_error(ctx, error):
    response = f'Flasheaste rey :sunglasses: tira `{PREFIX}help` y anda memorizando. Gil.'
    logging.error("  - ERROR DE COMANDO")
    logging.error("***********************************************************")
    logging.error(f"        {error}")
    logging.error("***********************************************************")
    await ctx.send(response)


if __name__ == "__main__":
    bot.run(TOKEN)
