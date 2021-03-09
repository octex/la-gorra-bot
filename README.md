# la-gorra-bot
Bot gorrudo para DS

Requerimientos:
```
Python 3.X
Instalar los requerimientos de requirements.txt
```

El bot arranca con: `python bot.py`

Es necesario antes crear un archivo en el directorio raiz del proyecto con nombre `.env` con el siguiente contenido:
```
DISCORD_TOKEN=TU_TOKEN_DE_DISCORD
DB_PATH=sqlite:///DIR_WIN\\gorra-db.db
DB_PATH=sqlite:///./gorra-db.db # Linux
SQL_CONFIG_PATH=C:\Users\TU_USER\CARPETA_DEL_PROYECTO\la-gorra-bot\resources/config.sql
SQL_CONFIG_PATH=./resources/config.sql # Linux
```
Las variables que incluyen directorios varian dependiendo donde se levante el bot
La configuracion de base de datos varia segun el motor utilizado, en este caso dejo de ejemplo con SQLite para poder levantarlo local sin problema.

Esta incluido en el primer release el archivo de configuracion pertinente para levantar el bot desde Heroku. Sin embargo, para el correcto funcionamiento del bot, es necesario configurar una BD PostgreSQL de Heroku y modificar la variable `DB_PATH` (revisar documentacion de SQLAlchemy y Heroku para mas informacion)
