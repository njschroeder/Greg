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
            for _ in range(4):
                try:
                    add_up_return += ' ' + message_as_list[i + _ + 1]
                except IndexError:
                    break
            await message.channel.send('Hi' + add_up_return + ', I\'m Greg!')
            return
        elif word == 'i\'m':
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
    names = ['-Abraham Lincoln', '-Barack Obama', '-George Washington', '-Sun Tzu', '-Winston Churchill', '-Franklin Delano Roosevelt', '-Confucius', '-Dwayne \"The Rock\" Johnson', '-Socrates', '-John Locke']
    g = ['-William Shakespeare']
    names.extend(g)
    
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

#help functions
    if message_sent == '&help':
        await message.channel.send('&quote: returns a random quote from the 2358 quotes pages \n&drawcard: returns a random card value \n&pollhelp: provides information about the polling functionality')
        return

    if message_sent == '&pollhelp':
        await message.channel.send('&newpoll [name]: creates a new poll with provided name (name not required)\n&getresult: returns the result of the poll at this very moment')
        return

#voting function
    #creates poll, provides instructions
    if message_as_list[0] == '&newpoll':
        erase_1 = open('ResultStore1.txt', 'w')
        erase_2 = open('ResultStore2.txt', 'w')
        pollname = ''
        for _ in range(1, len(message_as_list)):
            pollname += message_as_list[_] + ' '
        await message.channel.send('**NEW POLL** \n \n' + pollname + '\n \nSend "Y" to vote yes and "N" to vote no. I will confirm that your vote has been received in chat. You *can* change your vote later if you so wish')
        return

    #handles all necessary operations for vote reception
    if message_sent == 'Y' or message_sent == 'N':
        #determines which file code should read and which to manipulate
        key_1 = 'ResultStore1.txt'
        key_2 = 'ResultStore2.txt'
        read_key = ''
        f1 = open(key_1, 'r')
        f2 = open(key_2, 'r')
        f1_contents = f1.read()
        f2_contents = f2.read()
        if f1_contents == '' and f2_contents == '':
            print('both are blank')
            read_key = key_1
            write_key = key_2
            f2_0 = open(key_2, 'w')
        elif f1_contents == '':
            print('1 is blank, two is filled')
            read_key = key_2
            write_key = key_1
        elif f2_contents == '':
            print('2 is blank, 1 is filled')
            read_key = key_1
            write_key = key_2
        else:
            await message.channel.send('Error! Could not determine proper file to contact')

        #records vote (making sure to not allow double votes)
        vote_store = open(read_key, 'r')
        writeable_votes = open(write_key, 'a')
        yet_to_vote = True
        voteString = vote_store.read()
        votes = voteString.split()
        for _ in range(len(votes)):
            try:
                if votes[_ - 1] == username:
                    print(votes[_ - 1] + ' is ' + username)
                    writeable_votes.write(' ' + message_sent + ' ')
                    yet_to_vote = False
                else:
                    print(votes[_ - 1] + ' is not ' + username)
                    writeable_votes.write(votes[_])
            except IndexError:
                print(str(_) + ' is zero')
                writeable_votes.write(votes[_])
        if yet_to_vote:
            print(username + ' was not found')
            writeable_votes.write(username + ' ' + message_sent + ' ')
        erase_old = open(read_key, 'w')
        if message_sent == 'Y':
            await message.channel.send(username + ', you have updated your vote to yes on this poll')
        if message_sent == 'N':
            await message.channel.send(username + ', you have updated your vote to no on this poll')
        return
    
    #gathers results and returns an answer
    if message_sent == '&getresult':
        votecounts = [0, 0]
        key_1 = 'ResultStore1.txt'
        key_2 = 'ResultStore2.txt'
        f1 = open(key_1, 'r')
        f2 = open(key_2, 'r')
        f1_contents = f1.read()
        f2_contents = f2.read()
        print('f1 ' + f1_contents)
        print('f2 ' + f2_contents)
        read_key = ''
        if f1_contents == '' and f2_contents == '':
            await message.channel.send('Error! No votes logged')
        if f1_contents == '':
            vote_store = f2_contents
        elif f2_contents == '':
            vote_store = f1_contents
        else:
            await message.channel.send('Error! Votes logged incorrectly')
        votes = vote_store.split()
        for _ in range(1, len(votes), 2):
            if votes[_] == 'Y':
                votecounts[0] += 1
            elif votes[_] == 'N':
                votecounts[1] += 1
            else:
                pass
        await message.channel.send('the supporters count ' + str(votecounts[0]) + ' the opponents count ' + str(votecounts[1]))
        return



client.run(TOKEN)
