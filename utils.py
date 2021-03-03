from sqlalchemy.exc import IntegrityError


VERSION = '1.0.0'


def ascii_logo():
    print("_____________       ______________________________________ ")
    print("___  /___    |      __  ____/_  __ \__  __ \__  __ \__    |")
    print("__  / __  /| |      _  / __ _  / / /_  /_/ /_  /_/ /_  /| |")
    print("_  /___  ___ |      / /_/ / / /_/ /_  _, _/_  _, _/_  ___ |")
    print("/_____/_/  |_|      \____/  \____/ /_/ |_| /_/ |_| /_/  |_|")
    print(f"                                        Version: {VERSION}")
    print("                                         © Gordos inc.")


def load_config_table(config, engine):
    statements = config.read().split('\n')
    for statement in statements:
        try:
            engine.execute(statement)
        except IntegrityError:
            print("Key already on DB")
