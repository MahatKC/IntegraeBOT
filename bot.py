import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

lista_indices_grupos = ['1','2','3']
lista_nomes_grupos = ['UNIOESTE','UFAL','UFSM']

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild: \n' 
        f'{guild.name} (id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    mensagem_atividade = ('Bem-vindo ao Integraê! Envie uma mensagem com o número do seu grupo PET:\n'
    '\n --GRUPOS PET--\n 1-PETComp UNIOESTE\n2-PETComp UFSM')

    channel = discord.utils.get(guild.channels, name='canal_do_bot')
    role = await guild.create_role(name='cat3ppl')
    
    everyone_role = discord.utils.get(guild.roles, name='@everyone')

    await guild.create_category('cat3')
    category = discord.utils.get(guild.categories, name='cat3')
    await category.set_permissions(everyone_role,view_channel=False)
    await category.create_text_channel('simborax')
    await category.create_voice_channel('bora proseax')
    await category.set_permissions(role,view_channel=True)

    await channel.send(mensagem_atividade)
    
@client.event
async def on_message(message):
    user = message.author
    if user == client.user:
        return
    
    if message.channel.id == user.dm_channel.id:
        if message.content in lista_indices_grupos:
            guild = discord.utils.get(client.guilds, name=GUILD)
            role = discord.utils.get(guild.roles, name='cat3ppl')

            member = guild.get_member(user.id)
            await member.add_roles(role)
            response = 'Seu grupo é o '+lista_nomes_grupos[int(message.content)-1]
            await message.channel.send(response)

client.run(TOKEN)