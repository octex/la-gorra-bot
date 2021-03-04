# la-gorra-bot
Bot gorrudo para DS

Requerimientos:
```
Python 3.X
Virtual enviroment
Instalar requirements.txt en el ve
```

El bot arranca con: `python3.X bot.py`

Es necesario antes crear un archivo en el directorio raiz del proyecto con nombre `.env` con el siguiente contenido:
```
DISCORD_TOKEN=TU_TOKEN_DE_DISCORD
DB_PATH=sqlite:///DIR_WIN\\gorra-db.db
DB_PATH=sqlite:///DIR_LINUX//gorra-db.db
SQL_CONFIG_PATH=C:\Users\TU_USER\CARPETA_DEL_PROYECTO\la-gorra-bot\resources/config.sql
SQL_CONFIG_PATH=./resources/config.sql # Linux
```
Las variables que incluyen directorios varian dependiendo donde se levante el bot