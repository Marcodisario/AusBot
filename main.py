import discord
from discord.ext import commands
from discord import app_commands

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
        try:
            synced = await bot.tree.sync(guild=guild)
            print(f"Sincronizado {len(synced)} comando(s) en el servidor: {guild.name} (ID: {guild.id})")
        except Exception as e:
            print(f"Error al sincronizar comandos en el servidor {guild.name} (ID: {guild.id}): {e}")

# Un ejemplo de comando de barra diagonal
@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hola, {interaction.user}!")

@bot.tree.command(name="chau")
async def chau(interaction: discord.Interaction):
    await interaction.response.send_message(f"chau, {interaction.user}!")


@bot.command()
async def sync(ctx):
    print("sync command")
    await bot.tree.sync()
    await ctx.send('Command tree synced.')


