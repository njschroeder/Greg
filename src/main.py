import discord
import random

TOKEN = 'YOUR TOKEN HERE'

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

    if message_sent == 'shutdown' and username == 'pandomains':
        await message.channel.send('shutting down')
        await client.close()



#dad joke generator
    for i in range(len(message_as_list) - 1):
        word = message_as_list[i].lower()
        add_up_return = ''
        if word == 'im':
            print(word)
            for _ in range(4):
                try:
                    add_up_return += ' ' + message_as_list[i + _ + 1]
                except IndexError:
                    break
            await message.channel.send('Hi' + add_up_return + ', I\'m Greg!')
            return
        elif word == 'i\'m':
            print(word)
            for _ in range(4):
                try:
                    add_up_return += ' ' + message_as_list[i + _ + 1]
                except IndexError:
                    break
            await message.channel.send('Hi' + add_up_return + ', I\'m Greg!')
            return

#quotes sender
    quotes = ['Do as I say, NOT as I do', 'Arnold Schwarzenegger: half motor oil, half anti-freeze', 'It\'s only communism when I say it\'s communism']
    a = ['\"I\'m hungy, I\'m gonna go eat my cookie\"', '\"Yo I didn\'t know you guys kept gatorade in here!\" * grabs windex *', '\"I don\'t have insomnia I just can\'t sleep at night\"']
    b = ['\"I have to bark back or else it feels awkward\"', '\"Though I\'m pretty they don\'t have to do anything\"', '\"Okay who nominated Mr. Beast\"']
    c = ['\"My brain is a code.org assignment\"', '\"Did Carl Sagan write the Communist Manifesto?\"', '\"Diaphragm\" (pronounced as spelled)', '\"I thought Apple Bottom Jeans was a song from the forties\"']
    d = ['\"Did you know about the surgery they used to do for Cadillacs\"', '\"Using discord light mode is Adrian\'s only personality trait\"', '\"Explain this, Santa deniers\"']
    e = ['\"Joe Biden isn\'t black\"', '\"Why is there Al Gore Fanfiction?\"', '\"Work fast safety last!\"', '\"This club is NOT a safe space for left handed people\"']
    f = ['\"Y\'know what\'s fun? Arson\"', '\"It\'s like using a nuclear bomb to kill a spider in your house\"', '\"Who sells communist fan merch?\"']
    quotes.extend(a)
    quotes.extend(b)
    quotes.extend(c)
    quotes.extend(d)
    quotes.extend(e)
    quotes.extend(f)
    names = ['-Abraham Lincoln', '-Barack Obama', '-George Washington', '-Sun Tzu', '-Winston Churchill', '-Franklin Delano Roosevelt']
    
    if message_sent == '&quote':
        quote = random.choice(quotes)
        name = random.choice(names)
        await message.channel.send(quote + '\n' + '\n' + name)
        return


#random card generator
    card_names = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']    
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    if message_sent == '&drawcard':
        card = random.choice(card_names)
        suit = random.choice(suits)
        await message.channel.send('Your card is the ' + card + ' of ' + suit + '!')
        return

#help function
    if message_sent == '&help':
        await message.channel.send('&quote: returns a random quote from the 2358 quotes pages \n&drawcard: returns a random card value')
        return


client.run(TOKEN)
