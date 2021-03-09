import os
import logging
from random import randint, choice
import discord
from discord.ext import commands
from dotenv import load_dotenv
from models import Minion, BotConfig
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from utils import ascii_logo, load_config_table, registro_civil, VERSION, WELCOME_MESSAGES, TILT_FRASES


# Inicializacion
logging.basicConfig(level=logging.INFO)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_PATH = os.getenv('DB_PATH')
SQL_CONFIG_PATH = os.getenv('SQL_CONFIG_PATH')
engine = create_engine(DB_PATH, echo=True)

config = open(SQL_CONFIG_PATH, encoding="utf8")
load_config_table(config=config, engine=engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


# Constantes
PREFIX = session.query(BotConfig).filter_by(keyConfig='prefix').first().value
GORDEUS = session.query(BotConfig).filter_by(keyConfig='admin_role_mention').first().value
GORDO_BONDIOLA = session.query(BotConfig).filter_by(keyConfig='mod_role_mention').first().value
REGLAS_CHANNEL = session.query(BotConfig).filter_by(keyConfig='rules_channel').first().value
WELCOME_CHANNEL = session.query(BotConfig).filter_by(keyConfig='welcome_channel_id').first().value
IMPUNES = ['GORDO MAESTRO', 'GORDO BONDIOLA', 'GORDEUS']
BOT_COLOR = discord.Color.dark_purple()
COLOR_AMARILLO = discord.Color.from_rgb(255, 233, 0)
COLOR_ROJO = discord.Color.red()
MODO_VIOLENTO = False

# Creamos la instancia del bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    ascii_logo()
    logging.info(f'{bot.user} has connected to Discord!')


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
    logging.info(f"DS MESSAGE - author: {author}    channel: {message_channel_name}     content: {message_content}")
    if MODO_VIOLENTO:
        if message.author == bot.user:
            return
        num = randint(1, 1000)
        if num > 750:
            await message_channel.send(f"{choice(TILT_FRASES)}")

    if author_last_role not in IMPUNES:
        if (message_content.startswith('-p') or message_content.startswith('>p')) and \
        message_channel_name != 'musica' or message_content.startswith('-skip') or message_content.startswith('>skip'):
            await message_channel.send(f'{GORDO_BONDIOLA} Chst! Aca hay un ladri que se esta ganando una bala.')
            await registro_civil(author=author, author_name=author_name, author_mention=author_mention,
                                 message_channel=message_channel, session=session)
        elif message_content.startswith('$w') and \
            message_channel_name != 'waifus':
            await message_channel.send(f'{GORDO_BONDIOLA} Chst! Aca hay un ladri que se esta ganando una bala.')
            await registro_civil(author=author, author_name=author_name, author_mention=author_mention,
                                 message_channel=message_channel, session=session)
    if message_content.startswith('sale') or message_content.startswith('Sale'):
        await message_channel.send(f"Sale pa :sunglasses:")
    if bot.user.mentioned_in(message):
        await message_channel.send(f"Que onda pa, tira: `{PREFIX}help`")
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL)
    welcome_message = choice(WELCOME_MESSAGES)
    await channel.send(f"{member.mention} {welcome_message}")


@bot.command(name='ping', help='Para saber si esta vivo el bot')
async def ping(ctx):
    await ctx.send('Pong :ping_pong:')


@bot.command(name='reglas', help='Por si no encontras el canal')
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


@bot.command(name='advertidos', help='los que estan para kickear')
async def advertidos(ctx):
    embed = discord.Embed(title="Advertidos", description="Los ladris con solo una falta a la ley", color=COLOR_AMARILLO)
    minions = session.query(Minion).filter_by(strikes=1).all()
    for minion in minions:
        embed.add_field(name=minion.username, value=minion.strikes, inline=False)
    await ctx.send(embed=embed)


@bot.command(name='paraechar', help='directo al ban estos hijos de puta')
async def paraechar(ctx):
    embed = discord.Embed(title="Para echar", description="Los conchesumare que deben morir", color=COLOR_ROJO)
    minions = session.query(Minion).filter(Minion.strikes > 1).all()
    for minion in minions:
        embed.add_field(name=minion.username, value=minion.strikes, inline=False)
    await ctx.send(embed=embed)


@commands.has_any_role('GORDO BONDIOLA', 'GORDEUS')
@bot.command(name='modoviolento', help='solo admins. bsos.')
async def modoviolento(ctx):
    content = ctx.message.content.split(" ")
    try:
        value = int(content[1])
        if value < 0 or value > 1:
            raise ValueError
        global MODO_VIOLENTO
        MODO_VIOLENTO = bool(value)
        await ctx.send(f"Cambiado **modo violento** a: {MODO_VIOLENTO}")
    except ValueError:
        await ctx.send("Mandaste cualquiera forro. Es 0 o 1 la opcion.")
    except IndexError:
        await ctx.send(f"El **modo violento** esta: {MODO_VIOLENTO}")


@bot.command(name='info', help='datos del bot')
async def info(ctx):
    embed = discord.Embed(title="Info", description="Informacion del bot", color=BOT_COLOR)
    embed.add_field(name='Version', value=VERSION)
    embed.add_field(name='Repositorio', value="https://github.com/octex/la-gorra-bot")
    embed.add_field(name='Autor', value="BolsaDeGlucosa")
    embed.add_field(name='Lenguaje', value="Python")
    embed.add_field(name='Host', value="Heroku")
    embed.add_field(name='Hincha de', value="Peñarol")
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    response = f'Flasheaste rey :sunglasses: tira `{PREFIX}help` y anda memorizando. Gil.'
    logging.error(f"COMMAND ERROR - error: {error}")
    await ctx.send(response)


if __name__ == "__main__":
    bot.run(TOKEN)
