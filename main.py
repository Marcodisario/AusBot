import discord
from discord.ext import commands
from discord import app_commands

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

load_dotenv()

TOKEN=os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Ajusta los intents según sea necesario

# Inicializa el bot con un prefijo (aunque no lo usaremos para comandos de barra diagonal)
bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_ready():
    print(f'{bot.user} ha iniciado sesión en Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Conectado a {len(bot.guilds)} servidor(es)')

    # Sincronizar comandos globalmente
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizado {len(synced)} comando(s) global(es)")
    except Exception as e:
        print(f"Error al sincronizar comandos globales: {e}")

    # Opcional: Sincronizar comandos por servidor
    for guild in bot.guilds:
        general_channel = discord.utils.find(lambda x: x.name == 'general', guild.text_channels)
        if general_channel:
            await general_channel.send("¡Hola a todos! ¡Estoy en línea y listo para funcionar!")
        else:
            print(f"No se encontró el canal 'general' en el servidor {guild.name}")
        try:
            synced = await bot.tree.sync(guild=guild)
            print(f"Sincronizado {len(synced)} comando(s) en el servidor: {guild.name} (ID: {guild.id})")
        except Exception as e:
            print(f"Error al sincronizar comandos en el servidor {guild.name} (ID: {guild.id}): {e}")








# Un ejemplo de comando de barra diagonal
@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hola, {interaction.user}!")


@bot.command()
async def sync(ctx):
    print("sync command")
    await bot.tree.sync()
    await ctx.send('Command tree synced.')

bot.run(TOKEN)
