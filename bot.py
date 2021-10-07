from allocation_function import allocation
from groups_dict import groups_dict
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

#TO-DO LIST:
##FUNÇÕES ADMINISTRATIVAS
##MANDAR CODINOME E LINK PARA DOC
##TESTES SÓ A GENTE
##STRESS TEST

alloc = allocation()

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
        
    everyone_role = discord.utils.get(guild.roles, name='@everyone')

    """
    #create roles, categories and channels
    for i in range(30):
        trio_number = 'trio'+str(i)
        role = await guild.create_role(name=trio_number)
        await guild.create_category(trio_number)
        category = discord.utils.get(guild.categories, name=trio_number)
        await category.set_permissions(everyone_role,view_channel=False)
        await category.create_text_channel('texto_'+trio_number)
        await category.create_voice_channel('voz_'+trio_number)
        await category.set_permissions(role,view_channel=True)
    """    

    #await channel.send(mensagem_atividade)
    
@client.event
async def on_message(message):
    user = message.author
    if user == client.user:
        return
    
    if message.channel.id == user.dm_channel.id:
        if message.content in groups_dict.lista_indices_grupos:
            guild = discord.utils.get(client.guilds, name=GUILD)
            member = guild.get_member(user.id)
            if alloc.is_user_already_assigned(member):
                response = 'Seu trio já foi definido. Vá até o canal correspondente para iniciar a atividade.'
                await message.channel.send(response)
            elif alloc.is_user_in_queue(member):
                response = 'Sua solicitação já foi recebida. Aguarde até que mais participantes entrem. Se em até 10 minutos você não for alocado a um trio, entre em contato com a organização do evento.'
                await message.channel.send(response)
            else:
                trio_finished, trio_id, trio_member_list, trio_channel_list = alloc.set_trio(int(message.content), member, message.channel)
                
                if trio_finished:
                    role = discord.utils.get(guild.roles, name='trio'+str(trio_id-1)) 
                    for trio_member in trio_member_list:
                        await trio_member.add_roles(role)

                    response = 'Seu trio foi definido. Entre no canal de voz da sua categoria para iniciar a atividade.'
                    for trio_channel in trio_channel_list:
                        await trio_channel.send(response)
                    
                else:
                    response = 'Aguarde até que mais participantes entrem. Se em até 10 minutos você não for alocado a um trio, entre em contato com a organização do evento.'
                    await message.channel.send(response)

        elif os.getenv('ADMIN_KEY') in message.content:
            print("entrou na arvore de comandos")
            command = int(message.content[-1])
            print(command)
            if command==0:
                await delete_category()
            
            # apagar categorias e canais
            # limpar fila formando grupo
            ### formar dupla
            # printa usuários e grupos na fila
            # broadcast to fila
            # limpar fila eliminando todo mundo

    print(user)

@client.event
async def delete_category():
    guild = discord.utils.get(client.guilds, name=GUILD)
    for i in range(30):
        cat_name = 'trio'+str(i)
        category = discord.utils.get(guild.categories, name=cat_name)
        category_channels = category.channels
        for channel in category_channels:
            try:
                await channel.delete()
            except:
                print("DEU ERRO NA DELEÇÃO DA CATEGORIA"+str(i))
                pass
        await category.delete()


client.run(TOKEN)