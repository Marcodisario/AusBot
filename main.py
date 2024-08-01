from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
# Importar funciones del scrapper
import scrapper
import asyncio
import time

# ///////////////////////////////////
# ///////      SETTINGS       ///////
# ///////////////////////////////////
load_dotenv()
TOKEN=os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True
# Inicializa el bot con un prefijo (aunque no lo usaremos para comandos de barra diagonal)
bot = commands.Bot(command_prefix='!', intents=intents)

# ///////////////////////////////////
# ///////        EVENTS       ///////
# ///////////////////////////////////
@bot.event
async def on_ready():
    global materias, notificaciones
    print(f'{bot.user} ha iniciado sesión en Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Conectado a {len(bot.guilds)} servidor(es)')
    try:
        try:
            materias, notificaciones = scrapper.scrape_data()
        except Exception as e:
            print(f"Error al realizar el scraping: {e}")
    except Exception as e:
        print(f"Error al realizar el scraping: {e}")

    try:
        synced = await bot.tree.sync()
        print(f"Sincronizado {len(synced)} comando(s) global(es)")
    except Exception as e:
        print(f"Error al sincronizar comandos globales: {e}")

    for guild in bot.guilds:
        try:
            synced = await bot.tree.sync(guild=guild)
            print(f"Sincronizado {len(synced)} comando(s) en el servidor: {guild.name} (ID: {guild.id})")
        except Exception as e:
            print(f"Error al sincronizar comandos en el servidor {guild.name} (ID: {guild.id}): {e}")

async def run_every_3_hours():
    while True:
        try:
            materias, notificaciones = scrapper.scrape_data()
            print("Scraping realizado correctamente.")
        except Exception as e:
            print(f"Error al realizar el scraping: {e}")
        await asyncio.sleep(3 * 60 * 60)  # 3 hours in seconds

async def main():
    asyncio.create_task(run_every_3_hours())
    await bot.start(TOKEN)

asyncio.run(main())

# ///////////////////////////////////
# ///////       COMMANDS      ///////
# ///////////////////////////////////

@bot.tree.command(name="ver_materias")
async def ver_materias(interaction: discord.Interaction):
    """Muestra las materias scrapeadas almacenadas."""
    if materias:
        embed = discord.Embed(title=f"Materias Disponibles - {len(materias)}", color=discord.Color.blue())
        for materia, data in materias.items():
            embed.add_field(
                name=materia, 
                value=f"[Ver materia]({data['url']})\n**Cupos:** {data.get('cupos', 'N/A')} | **Inscriptos:** {data.get('inscriptos', 'N/A')}\n**Descripción:** {data.get('description', 'N/A')}", 
                inline=False
            )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No se encontraron materias.")


@bot.tree.command(name="ver_notificaciones")
async def ver_notificaciones(interaction: discord.Interaction):
    """Muestra solo las notificaciones leídas almacenadas."""
    leidas = [notif for notif in notificaciones if "[no_leído]" in notif]
    
    if leidas:
        response = "\n".join(leidas)
    else:
        response = "No se encontraron notificaciones leídas."

    await interaction.response.send_message(f"```\n{response}\n```")

@bot.command()
async def sync(ctx):
    print("sync command")
    await bot.tree.sync()
    await ctx.send('Command tree synced.')

# ///////////////////////////////////
# ///////      INITIALIZE     ///////
# ///////////////////////////////////

bot.run(TOKEN)
