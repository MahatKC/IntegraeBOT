from allocation_function import allocation
from trio_links import trios
from groups_dict import groups_dict
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

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

@client.event
async def trio_formado(guild, trio_id, trio_member_list, trio_channel_list):
    codinomes = ["Florzinha","Lindinha","Docinho"]

    trio_finished_message = "Trio "+str(trio_id)+" formado com: "
    for membro in trio_member_list:
        trio_finished_message += membro.name+ ", "
    print(trio_finished_message)

    role = discord.utils.get(guild.roles, name='trio'+str(trio_id))

    i=0
    response = 'Seu trio foi definido. Entre no canal de voz da sua categoria para iniciar a atividade.' 
    for trio_member, trio_member_channel in zip(trio_member_list, trio_channel_list):
        await trio_member.add_roles(role)
        await trio_member_channel.send(response)
        response2 = 'Seu codinome é '+codinomes[i]+'. Acesse o arquivo no seguinte link para participar da atividade: '+trios[trio_id][i]
        await trio_member_channel.send(response2)
        i+=1

@client.event
async def membro_alocado(guild, trio_id, membro, channel):
    trio_finished_message = "Trio "+str(trio_id)+" formado com: "+membro.name
    print(trio_finished_message)

    role = discord.utils.get(guild.roles, name='trio'+str(trio_id))

    response = 'Seu trio foi definido. Entre no canal de voz da sua categoria para iniciar a atividade.' 
    await membro.add_roles(role)
    await channel.send(response)
    response2 = 'Seu codinome é Florzinha. Acesse o arquivo no seguinte link para participar da atividade: '+trios[trio_id][0]
    await channel.send(response2)

@client.event
async def create_roles_dos_trios():
    guild = discord.utils.get(client.guilds, name=GUILD)
    everyone_role = discord.utils.get(guild.roles, name='@everyone')

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
    
    print("Categorias criadas!")

@client.event
async def mensagem_inicial_bot():
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    mensagem_atividade = ('Bem-vindo ao Integraê! Me envie uma **MENSAGEM PRIVADA** com o número do seu grupo PET:\n'
    '\n**-----GRUPOS PET-----**\n')

    for group_id,group_name in zip(groups_dict.lista_indices_grupos, groups_dict.lista_nomes_grupos):
        mensagem_atividade += group_id+" - "+group_name+"\n"

    channel = discord.utils.get(guild.channels, name='canal_do_bot')
        
    await channel.send(mensagem_atividade)

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
        print("Categoria "+str(i)+" excluída.")

@client.event
async def print_queue_users():
    print("-"*10)
    print(f"A fila está com {len(alloc.user_id_queue)} pessoas")
    for person, group in zip(alloc.user_id_queue, alloc.group_id_queue):
        print(f"Grupo: {group}, User: {person.name}")
    print("-"*10)
    pass

@client.event
async def empty_queue_allocating_groups():
    guild = discord.utils.get(client.guilds, name=GUILD)
    trios_id, trios_member_list, trios_channel_list = alloc.force_trio_creation()

    for trio_id, trio_member_list, trio_channel_list in zip(trios_id, trios_member_list, trios_channel_list):
        if type(trio_member_list)!=list:
            print("IGOR, VÁ PARA A CATEGORIA TRIO"+str(trio_id)+" !!!")
            await membro_alocado(guild, trio_id, trio_member_list, trio_channel_list)
        else:
            await trio_formado(guild, trio_id, trio_member_list, trio_channel_list)

    pass

@client.event
async def broadcast_message_to_queue_users(broadcast_message):
    #SINTAXE DA MENSAGEM:
    #[ADMINKEY][MENSAGEM]2
    for person_channel in alloc.user_channel_queue:
        await person_channel.send(broadcast_message)

    pass

@client.event
async def clean_queues():
    alloc.group_id_queue = []
    alloc.user_id_queue = []
    alloc.user_channel_queue = []
    alloc.already_assigned = []
    print("Filas limpas!")

    pass

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
                    await trio_formado(guild, trio_id, trio_member_list, trio_channel_list)
                    
                else:
                    response = 'Aguarde até que mais participantes entrem. Se em até 10 minutos você não for alocado a um trio, entre em contato com a organização do evento.'
                    await message.channel.send(response)

        elif os.getenv('ADMIN_KEY') in message.content:
            command = int(message.content[-1])
            admin_funcs = {
                0: delete_category,
                1: print_queue_users,
                2: broadcast_message_to_queue_users,
                3: empty_queue_allocating_groups,
                4: mensagem_inicial_bot,
                5: create_roles_dos_trios,
                7: clean_queues
            }
            if command==2:
                broadcast_message = message.content.replace(os.getenv('ADMIN_KEY'),"").replace(str(command),"")
                await admin_funcs[command](broadcast_message)
            else:
                await admin_funcs[command]()

    print(user)

client.run(TOKEN)