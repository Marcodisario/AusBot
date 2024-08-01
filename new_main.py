from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
# Importar funciones del scrapper
# import scrapper
import asyncio
import time
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()


intents = discord.Intents.default()
intents.message_content = True
# Inicializa el bot con un prefijo (aunque no lo usaremos para comandos de barra diagonal)
bot = commands.Bot(command_prefix='!', intents=intents)


load_dotenv()
TOKEN=os.getenv('TOKEN')
@bot.event
async def on_ready():
    global materias, notificaciones
    print(f'{bot.user} ha iniciado sesión en Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Conectado a {len(bot.guilds)} servidor(es)')
    bot.loop.create_task(print_message_periodically())


async def print_message_periodically():
    while True:
        last_rows = cursor.execute("SELECT timestamp, json_data FROM counter_data ORDER BY id DESC LIMIT 2").fetchall()
        print(last_rows)
        await asyncio.sleep(1)

# cursor.execute("SELECT * FROM counter_data ORDER BY id DESC LIMIT 1")
# last_row = cursor.fetchone()
# print(last_row)

bot.run(TOKEN)