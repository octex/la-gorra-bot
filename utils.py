from sqlalchemy.exc import IntegrityError
from models import Minion


VERSION = '1.0.0'

WELCOME_MESSAGES = ["DNI y papeles por favor. Puede pasar, comportese y no haga que se me vaya la mano...",
                    "Que tal, libreta de enrolamiento y papeles del auto por favor. Cuidado con lo que hace y disfrute del chori.",
                    "Amigo que olor a culo que tenes, pero esta perfecto loko asi me gusta la gente, sin pudor y sin verguenza. Bienvenido y no te mandes ninguna.",
                    "DAAALE BOOOOOOOO DAAAAALE BOOOOOOOOOO",
                    "Ojo con Jorge que no hay culo que perdone...",
                    "Al que madruga dios lo achura. Patria, familia y ley. Bienvenido.",
                    "El problema no es mirar la vidriera, sino cuando te entran ganas de tocar.",
                    "Entra papi, no muerdo... Al menos no tan fuerte...",
                    "Disculpame pibe, ahora no te puedo dar la bienvenida. Está jugando peñarol."]
#TODO: Mudar esta shit a la base


def ascii_logo():
    print("_____________       ______________________________________ ")
    print("___  /___    |      __  ____/_  __ \__  __ \__  __ \__    |")
    print("__  / __  /| |      _  / __ _  / / /_  /_/ /_  /_/ /_  /| |")
    print("_  /___  ___ |      / /_/ / / /_/ /_  _, _/_  _, _/_  ___ |")
    print("/_____/_/  |_|      \____/  \____/ /_/ |_| /_/ |_| /_/  |_|")
    print(f"                                        Version: {VERSION}")
    print("                                      © Gordos Loleros inc.")


def load_config_table(config, engine):
    statements = config.read().split('\n')
    for statement in statements:
        try:
            engine.execute(statement)
        except IntegrityError:
            print("Key already on DB")


async def registro_civil(session, author, author_name, author_mention, message_channel):
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
