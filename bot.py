import os, logging, requests, shutil, discord
from PIL import Image, UnidentifiedImageError, ImageDraw, ImageFont
from random import choice, randint, uniform
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound
from discord.ext import commands
from dotenv import load_dotenv
from models import Minion, BotConfig
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from utils import ascii_logo, load_config_table, \
registro_civil, VERSION, WELCOME_MESSAGES, TILT_FRASES, \
TILT_PROBABILITY, TILT_CHANNELS, inmunidad_diplomatica


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
MODO_VIOLENTO = bool(int(session.query(BotConfig).filter_by(keyConfig='tilt_mode').first().value))
BOT_COLOR = discord.Color.dark_purple()
COLOR_AMARILLO = discord.Color.from_rgb(255, 233, 0)
COLOR_ROJO = discord.Color.red()


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
    author_mention = author.mention
    message_channel_name = str(message.channel)
    message_channel = message.channel
    message_content = message.content
    logging.info(f"DS MESSAGE - author: {author}    channel: {message_channel_name}     content: {message_content}")
    if MODO_VIOLENTO and message_channel_name in TILT_CHANNELS:
        if message.author == bot.user:
            return
        num = uniform(0, 1)
        if num < TILT_PROBABILITY:
            await message_channel.send(f"{choice(TILT_FRASES)}")
    
    es_impune = inmunidad_diplomatica(author.roles)

    if not es_impune:
        if (message_content.startswith('-p') or message_content.startswith('>p')) and \
        message_channel_name != 'musica' or message_content.startswith('-skip') or message_content.startswith('>skip'):
            await message_channel.send(f'{GORDO_BONDIOLA} Chst! Aca hay un ladri que se esta ganando una bala.')
            await registro_civil(author=author, author_mention=author_mention, message_channel=message_channel, session=session)
        elif message_content.startswith('$w') and \
            message_channel_name != 'waifus':
            await message_channel.send(f'{GORDO_BONDIOLA} Chst! Aca hay un ladri que se esta ganando una bala.')
            await registro_civil(author=author, author_mention=author_mention, message_channel=message_channel, session=session)
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
async def indultar(ctx, user: discord.User):
    minion_to_pardon = session.query(Minion).filter_by(full_username=str(user)).first()
    if minion_to_pardon is None:
        await ctx.send('No lo registro a este che.')
    else:
        session.delete(minion_to_pardon)
        session.commit()
        await ctx.send(f'{user.mention} tas indultado pa.')


@indultar.error
async def indultar_error_handler(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"Pero sos pelotudo o te faltan teclas en el genius? Poneme a quien tengo que buscar.")


@bot.command(name='advertidos', help='los que estan para kickear')
async def advertidos(ctx):
    embed = discord.Embed(title="Advertidos", description="Los ladris con solo una falta a la ley", color=COLOR_AMARILLO)
    minions = session.query(Minion).filter_by(strikes=1).all()
    for minion in minions:
        embed.add_field(name=minion.full_username, value=f"Strikes: {minion.strikes}", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='paraechar', help='directo al ban estos hijos de puta')
async def paraechar(ctx):
    embed = discord.Embed(title="Para echar", description="Los conchesumare que deben morir", color=COLOR_ROJO)
    minions = session.query(Minion).filter(Minion.strikes > 1).all()
    for minion in minions:
        embed.add_field(name=minion.full_username, value=f"Strikes: {minion.strikes}", inline=False)
    await ctx.send(embed=embed)


@commands.has_any_role('GORDO BONDIOLA', 'GORDEUS')
@bot.command(name='multar', help='para desconocer a algun pelotudo')
async def multar(ctx, user: discord.User):
    await registro_civil(author=user, author_mention=user.mention, message_channel=ctx.channel, session=session)
    await ctx.send(f"{user.mention} A la lista, pete.")


@multar.error
async def multar_error_handler(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"Pone a quien queres multar, salame.")


@commands.has_any_role('GORDO BONDIOLA', 'GORDEUS')
@bot.command(name='modoviolento', help='solo admins. bsos. Pone un 1 para activarlo o un 0 para desactivarlo.')
async def modoviolento(ctx, val: int):
    try:
        if val < 0 or val > 1:
            raise ValueError
        global MODO_VIOLENTO
        tmp_config = session.query(BotConfig).filter_by(keyConfig='tilt_mode').first()
        tmp_config.value = str(val)
        session.commit()
        MODO_VIOLENTO = bool(int(session.query(BotConfig).filter_by(keyConfig='tilt_mode').first().value))
        await ctx.send(f"Cambiado **modo violento** a: {MODO_VIOLENTO}")
    except ValueError:
        await ctx.send("Mandaste cualquiera forro. Es 0 o 1 la opcion.")


@modoviolento.error
async def modoviolento_error_handler(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"El **modo violento** esta en: {MODO_VIOLENTO}")


@bot.command(name='elchotode', help='Te tira la medida del pingo del miembro que pongas.')
async def elchotode(ctx, user: discord.User):
    pingo = randint(1, 35)
    await ctx.send(f"{user.mention} Le mide: {pingo}cm")


@elchotode.error
async def elchotode_error_handler(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"Tengo la regla pero no el pingo maestro.")


@bot.command(name='piky', help='Invocalo con una fotarda y una frase :sunglasses:')
async def piky(ctx):
    """
        Primero valido que tenga imagen y texto (msg y attachment)
            Si no es asi, no hago nada y devuelvo el error
        Si cumplo eso, descargo la imagen ;OJO; Veamos si podemos procesarla sin
        necesidad de descargarla
            Me aseguro de que si algo sale mal, la imagen se elimine
        Una vez que la proceso con PIL, le agrego el texto
        cargado por mensaje en la parte centrica de la imagen
        Le agrego ademas, un @frasesmillonarias en la parte de abajo
        Si todo sale bien, subo la imagen editada como respuesta.
    """
    text_message = ctx.message.content
    text_message = text_message.replace(f'{PREFIX}piky', '')
    attachments_msg = ctx.message.attachments
    if len(attachments_msg) == 0 or text_message == '':
        await ctx.send(f"Una imagen, y un texto. No es tan complicado simio.")

    attachment_first = ctx.message.attachments[0]
    attachment_url = attachment_first.url
    attachment_filename = attachment_first.filename
    tmp_file_dir = f"./{attachment_filename}"

    response = requests.get(attachment_url, stream=True)

    with open(tmp_file_dir, "wb") as tmp_file:
        shutil.copyfileobj(response.raw, tmp_file)
    img = Image.open(tmp_file_dir)
    try:
        img.verify() #TODO: Por que nos larga error?
    except UnidentifiedImageError:
        await ctx.send(f"Si me vas a tomar de boludo, hacela bien...")
        os.remove(tmp_file_dir) #TODO: probar esto
    except AttributeError:
        pass
    img.load()
    img_size_px = img.size
    text_font = ImageFont.truetype('resources/BebasNeue-Regular.ttf', int(img_size_px[0] / 10)) #TODO: Buscar una formula para esto
    text_pos_px = (0, img_size_px[1] / 2) #TODO: Buscar una formula para esto
    text_color = (255, 255, 255) # Blanco
    img_modified = ImageDraw.Draw(img)
    img_modified.text(text_pos_px, text_message, text_color, 
                      font=text_font, stroke_fill=(0,0,0), stroke_width=2)
    img.save(tmp_file_dir)
    await ctx.send(file=discord.File(tmp_file_dir))
    img.close()
    os.remove(tmp_file_dir)
    #TODO: Revisar como hacer para que no perdamos texto si sobrepasa la dimension de la imagen

    


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
    logging.error(f"COMMAND ERROR - error: {error}")
    if isinstance(error, CommandNotFound):
        response = 'No sabes invocar un comando capo?'
        await ctx.send(response)


if __name__ == "__main__":
    bot.run(TOKEN)
