import discord
import socket
import json
from discord.ext import commands
from datetime import datetime
from secrets import TOKEN
from secrets import api_key
from itemparser import parse
import requests
# https://stackoverflow.com/questions/53528168/how-do-i-use-cogs-with-discord-py

client = commands.Bot(command_prefix = "!")
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# print(f'hostname: {hostname}')
# print(f'IP Adress: {ip_address}')



def api_testing():
    summoner_name = 'shiimanek'
    url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'

    response = requests.get(url, params={'api_key' : api_key})

    print(response)

    try:
        content = response.json()
        print(content['name'])
        print(content['puuid'])
        print(content['summonerLevel'])
        print('r', content['revisionDate'])
        print('p', content['profileIconId'])
        print('a', content['accountID'])
        print('f', content['id'])
    except:
        print(response)


# api_testing()





# ---------------------- events ---------------------- #




@client.event
async def on_ready():
    print('bender is online..')
    print(f'logged in as {client.user}.')
    print(f'client latency: {round(client.latency * 1000)} ms.')


@client.event
async def on_disconnect():
    print(f'bender is offline..')




# ---------------------- commands ---------------------- #




# ip and socket related
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms.')


@client.command(aliases = ['ip', 'ip address', 'address', 'myip', 'myaddress', ])
async def _ip(ctx):
    # if id == tannershimanek (214200590593425408)
    await ctx.send(f'IP Address: {ip_address}')


@client.command(aliases = ['hostname', 'host', 'myhostname'])
async def _hostname(ctx):
    # if id == tannershimanek (214200590593425408)
    await ctx.send(f'Hostname: {hostname}')


# user related
@client.command(aliases = ['user', 'member'])
async def _user(ctx, *, arg):
    if arg == 'id':
        await ctx.send(f'User ID: #{ctx.author.id}')
    elif arg == 'name':
        await ctx.send(f'User Name: {ctx.author.name}')
    elif arg == 'joined':
        await ctx.send(f'{ctx.author.name} joined on {ctx.author.joined_at}')
    else:
        str_of_cmds = '!get user, !get id, or !get joined'
        await ctx.send(f'Not a proper command.. Try one of these:  {str_of_cmds}.')


# direct message
@client.command()
async def poke(ctx, user: discord.User, *, message=None):
    try:
        message = message or 'beep boop'
        await user.send(message)
        print(f'message to user [{user.name}] with ID[{user.id}] [SUCCESSFUL]')
    except:
        await ctx.send('Not a proper command.. Try:  !poke [member you want to message].')
        print(f'message to user [{user.name}] with ID[{user.id}] [FAILED] instruction message sent')


# op.gg related
@client.command(aliases = ['op.gg', 'opgg', 'op'])
async def _op(ctx, *, user_name=None):
    user = ctx.author
    try:
        op_url = 'https://na.op.gg/summoner/userName='
        message = f'Here is your link: {op_url + user_name}'
        await user.send(message)
        print(f'message to user [{user.name}] with ID[{user.id}] [SUCCESSFUL] link: {op_url + user_name}')
    except:
        await ctx.send('Not a proper command.. Try:  !op [your account].')
        print(f'message to user [{user.name}] with ID[{user.id}] [FAILED] instruction message sent')


# items 
@client.command(aliases = ['item', 'items'])
async def _items(ctx, *, item_req=None):
    file = open('item.json', 'r')
    data = json.load(file)
    item_numbers = data['data'].keys()
    item_details = {}

    if len(item_details) == 0: # TODO: create a hashmap of items when bot loads
        for item in item_numbers: # make global or clear when done
            name = data['data'][item]['name']
            item_details[name.replace("'", "").lower()] = item

    # TODO move to itemParser.py
    if item_req in item_numbers: 
        item_name = data['data'][item_req]['name']
        item_description = data['data'][item_req]['description'] # parse
        item_price = data['data'][item_req]['gold']['base']

        item_description = item_description.replace("<mana>", "")
        item_description = item_description.replace("</mana>", "")
        item_description = item_description.replace("<stats>", "")
        item_description = item_description.replace("</stats>", "")
        item_description = item_description.replace("<unique>", "")
        item_description = item_description.replace("</unique>", "")
        item_description = item_description.replace("<br>", "\n")
        item_description = item_description.replace("<grouplimit>", "")
        item_description = item_description.replace("</grouplimit>", "")
        item_description = item_description.replace("<passive>", "")
        item_description = item_description.replace("</passive>", "")

        result = f'{item_name}:\n\n{item_description}\n\nCost: {item_price}'
    elif item_req in item_details:
        item_name = data['data'][item_details.get(item_req)]['name']
        item_number = item_details[item_req]
        item_description = data['data'][item_number]['description'] # parse
        item_price = data['data'][item_number]['gold']['base']

        item_description = item_description.replace("<mana>", "")
        item_description = item_description.replace("</mana>", "")
        item_description = item_description.replace("<stats>", "")
        item_description = item_description.replace("</stats>", "")
        item_description = item_description.replace("<unique>", "")
        item_description = item_description.replace("</unique>", "")
        item_description = item_description.replace("<br>", "\n")
        item_description = item_description.replace("<grouplimit>", "")
        item_description = item_description.replace("</grouplimit>", "")
        item_description = item_description.replace("<passive>", "")
        item_description = item_description.replace("</passive>", "")
        # FIXME
        # parse <a href="[reg a-z]"></a>
        # parse <font color="[reg 0-9]></font>

        result = f'{item_name}  {item_number}:\n\n{item_description}\n\nCost: {item_price}'
        await ctx.send(result)



# RIOT API
@client.command()
async def summoner(ctx, *, summoner_name=None):
    current_date = datetime.now()
    time_of_event = current_date.strftime("%H:%M:%S %m/%d/%y")
    url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    try:
        response = requests.get(url, params={'api_key' : api_key})
        content = response.json()
        # summoner_account_id = content['accountID']
        summoner_puuid = content['puuid']
        summoner_name = content['name']
        # summoner_profile_icon_id = content['profileIconId']
        # summoner_revision_date = content['revisionDate']
        summoner_level = content['summonerLevel']

        result = f'Summoner:\n{summoner_name}\n\nLevel:\n{summoner_level}\n\npuuid:\n{summoner_puuid}'
        await ctx.send(result)
    except:
        print('\n------ERROR------\n')
        print(ctx.author)
        print(time_of_event)
        print(f'input: !summoner {summoner_name}')
        print(f'response: {response.status_code}')
        print('\n------ERROR------\n')

        if response.status_code == 404:
            await ctx.send(f'Summoner "{summoner_name}" does not exist.')






# client.run(TOKEN)


# print(TOKEN)


# class Bender(discord.Client):

#     # def __init__(self):
#     #     self.hostname = socket.gethostname()
#     #     self.ip_address = socket.gethostbyname(self.hostname) # look into sockets
    
#     async def on_ready(self):
#         print('bender is online..')
#         print(f'logged in as {self.user}..')
    
#     async def on_disconnect(self):
#         await message.channel.send('Bender is offline.')

#     async def on_message(self, message):
#         hostname = socket.gethostname()
#         ip_address = socket.gethostbyname(hostname)

#         if message.author == self.user:
#             return

#         if message.content.startswith('!hello'):
#             await message.channel.send(f'Hello! {message.author.name}!')

#         if message.content.startswith('!ip'):
#             await message.channel.send(f'Your ip address is: {ip_address}')

#         if message.content.startswith('!hostname'):
#             await message.channel.send(f'Hostname: {hostname}')
    
    # @commands.command
    # async def ping(self, ctx, argument):
    #     await self.bot.say('pong')

#     @commands.command()
#     async def test(self, ctx, arg):
#         await ctx.send(arg)



# class Setup(Bender):
#     def __init__(self):
#         Bender.__init__()






# client = Bender()
# client = commands.Bot(command_prefix = "!")
client.run(TOKEN)