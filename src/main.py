import discord
import token

TOKEN = token.getToken()

client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    message_sent = str(message.content)
    message_as_list = message_sent.split()
    channel = str(message.channel.name)
    print(f'{username}: {message_sent} ({channel})')

    if message.author == client.user:
        return

    if message_sent == 'shutdown':
        await client.close()

    for i in range(len(message_as_list)):
        word = message_as_list[i].lower()
        response = ''
        if word == 'im' or 'i\'m':
            await message.channel.send('Hi ' + username + ', I\'m Greg!')
            return
        


client.run(TOKEN)
