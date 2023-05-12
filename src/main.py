import string
import discord
from discord import Intents
import random
import time
import TicTacToeMaster as ttt

TOKEN = 'YOUR TOKEN HERE'

intents = Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
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

    if message_sent == 'shutdown' and str(message.author) == 'pandomains#5375':
        await message.channel.send('shutting down')
        await client.close()

#dad joke generator
    for i in range(len(message_as_list) - 1):
        word = message_as_list[i].lower()
        nextword = message_as_list[i+1].lower()
        add_up_return = ''
        if word == 'im' or word == 'i\'m':
            for _ in range(i + 4):
                try:
                    add_up_return += ' ' + message_as_list[i + _ + 1]
                except IndexError:
                    break
            await message.channel.send('Hi' + add_up_return + ', I\'m Greg!')
            return
        elif (word == 'i' and nextword == 'am'):
            for _ in range(i + 4):
                try:
                    add_up_return += ' ' + message_as_list[i + _ + 2]
                except IndexError:
                    break
            await message.channel.send('Hi' + add_up_return + ', I\'m Greg!')


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
        a = '&quote: returns a random quote from the 2358 quotes pages \n&drawcard: returns a random card value \n&pollhelp: provides information about the polling functionality'
        b = '\n&createsentence [ngrams] [desired length]: creates a new sentence generated using the provided words as an ngram dictionary'
        c = '\n&thymecheck: returns the price of thyme, using an ounce count the same as CDT\'s 24-hour time value'
        d = '\n&rps [move]: runs a round of rock paper scissors. Your move should be the full word (rock, paper, or scissors)'
        e = '\n&newttt: provides a blank tic tac toe board and instructions to play'
        await message.channel.send(a + b + c + d + e) 
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
        await message.channel.send('**NEW POLL** \n \n' + pollname + '\n \nSend "Y" to vote yes and "N" to vote no. I will confirm that your vote has been received in chat. You *can* change your vote later if you so wish \n \n **DO NOT** spam your votes')
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
            read_key = key_1
            write_key = key_2
            f2_0 = open(key_2, 'w')
        elif f1_contents == '':
            read_key = key_2
            write_key = key_1
        elif f2_contents == '':
            read_key = key_1
            write_key = key_2
        else:
            await message.channel.send('Error! Could not determine proper file to contact. Please launch a new poll')

        #records vote (making sure to not allow double votes)
        vote_store = open(read_key, 'r')
        writeable_votes = open(write_key, 'a')
        yet_to_vote = True
        voteString = vote_store.read()
        votes = voteString.split()
        for _ in range(len(votes)):
            try:
                if votes[_ - 1] == username:
                    writeable_votes.write(' ' + message_sent + ' ')
                    yet_to_vote = False
                else:
                    writeable_votes.write(votes[_])
            except IndexError:
                writeable_votes.write(votes[_])
        if yet_to_vote:
            writeable_votes.write(username + ' ' + message_sent + ' ')
        erase_old = open(read_key, 'w')
        if message_sent == 'Y':
            await message.channel.send(username + ', you have updated your vote to yes on this poll')
        if message_sent == 'N':
            await message.channel.send(username + ', you have updated your vote to no on this poll')
        return
    
    #gathers results and returns an answer
    if message_sent == '&getresult':
        check_correct = True
        votecounts = [0, 0]
        key_1 = 'ResultStore1.txt'
        key_2 = 'ResultStore2.txt'
        f1 = open(key_1, 'r')
        f2 = open(key_2, 'r')
        f1_contents = f1.read()
        f2_contents = f2.read()
        read_key = ''
        if f1_contents == '' and f2_contents == '':
            await message.channel.send('Error! No votes logged')
        if f1_contents == '':
            vote_store = f2_contents
        elif f2_contents == '':
            vote_store = f1_contents
        else:
            await message.channel.send('Error! Votes logged incorrectly. Please launch a new poll')
        votes = vote_store.split()
        #checks vote assortment to ensure that nobody has multiple votes
        for _ in range(0, len(votes), 2):
            for a in range(_ + 2, len(votes), 2):
                if votes[_] == votes[a]:
                    await message.channel.send('Error! Someone has multiple votes logged. Please launch a new poll')
                    check_correct = False
                    return
        if check_correct:
            for _ in range(1, len(votes), 2):
                if votes[_] == 'Y':
                    votecounts[0] += 1
                elif votes[_] == 'N':
                    votecounts[1] += 1
                else:
                    pass
            await message.channel.send('the supporters count ' + str(votecounts[0]) + ' the opponents count ' + str(votecounts[1]))
            return

#speech replicator - uses an input ngram dictionary to attempt to create new sentences that could exist from it
    
    if message_as_list[0] == '&createsentence':
        #creates the ngram dictionary from which the code can pull
        custom_length = 1
        dict = {}
        if len(message_as_list) <= 3:
            await message.channel.send('Your ngram dictionary is too short! Try again with a longer one')
            return
        if message_as_list[len(message_as_list)-1].isnumeric():
            custom_length = 2
        for _ in range(1, len(message_as_list) - custom_length):
            outValue = dict.setdefault(message_as_list[_], [message_as_list[_ + 1]])
            if outValue != [message_as_list[_ + 1]]:
                outValue.append(message_as_list[_ + 1])
                dict.pop(message_as_list[_])
                dict.setdefault(message_as_list[_], outValue)

    #generates sentence from ngrams provided
        send_string = ''
        next_key = message_as_list[1]
        send_string += next_key
        length_cap = 15
        if custom_length == 2:
            length_cap = int(message_as_list[len(message_as_list)-1])
        for _ in range(length_cap - 1):
            try:
                nextWord = random.choice(dict.get(next_key))
                send_string += ' ' + nextWord
                next_key = nextWord
            except TypeError:
                await message.channel.send(send_string)
                return
                
        await message.channel.send(send_string)
        return

#thymecheck
    if message_sent == '&thymecheck':
        unix_time = time.time()
        CDT_unix = unix_time - 18000 #a very odd way to shift time zone sure, but it's easier than all the if statements for the past 00:00 edge case
        seconds = CDT_unix % 86400
        print(seconds)

        hours_decimal = seconds / 3600
        hours = int(hours_decimal)
        seconds = seconds - (hours * 3600)
        print(hours)

        minutes_decimal = seconds / 60
        minutes = int(minutes_decimal)
        print(minutes)

        ounces = (hours * 100) + minutes
        price_decimal = ounces * 39.7 #uses wrong conversion rate, should be 0.397, but this makes truncating to 2 decimals easier
        price_int = int(price_decimal)
        price = price_int / 100
        await message.channel.send(str(ounces) + ' ounces of thyme would cost $' + str(price))

#rock paper scissors
    if message_as_list[0] == '&rps':
        try:
            if message_as_list[1] == 'rock' or message_as_list[1] == 'paper' or message_as_list[1] == 'scissors':
                opponent_move = message_as_list[1]
                move_list = ['rock', 'paper', 'scissors']
                bot_move = random.choice(move_list)
                if opponent_move == 'rock':
                    if bot_move == 'rock':
                        await message.channel.send('You used ' + opponent_move + ', and I used ' + bot_move + '. Tie game!')
                    elif bot_move == 'paper':
                        await message.channel.send('You used ' + opponent_move + ', and I used ' + bot_move + '. I win!')
                    elif bot_move == 'scissors':
                        await message.channel.send('You used ' + opponent_move + ', and I used ' + bot_move + '. You win!')
            
                elif opponent_move == 'paper':
                    if bot_move == 'rock':
                        await message.channel.send('You used ' + opponent_move + ', and I used ' + bot_move + '. You win!')
                    elif bot_move == 'paper':
                        await message.channel.send('You used ' + opponent_move + ', and I used ' + bot_move + '. Tie game!')
                    elif bot_move == 'scissors':
                        await message.channel.send('You used ' + opponent_move + ', and I used ' + bot_move + '. I win!')
            
                elif opponent_move == 'scissors':
                    if bot_move == 'rock':
                        await message.channel.send('You used ' + opponent_move + ', and I used ' + bot_move + '. I win!')
                    elif bot_move == 'paper':
                        await message.channel.send('You used ' + opponent_move + ', and I used ' + bot_move + '. You win!')
                    elif bot_move == 'scissors':
                        await message.channel.send('You used ' + opponent_move + ', and I used ' + bot_move + '. Tie game!')
        
            else:
                await message.channel.send('Error! No valid move provided. Please provide a valid move')
        
        except IndexError:
            await message.channel.send('Error! No valid move provided. Please provide a valid move')

    print(message_as_list)

#tictactoe bot
    #prepares new game
    if message_sent == '&newttt':
        await message.channel.send('Instructions: Copy each board when provided, then add in your move as X into an available space')
        graphic = ttt.printBoard([" ", " ", " ", " ", " ", " ", " ", " ", " "])
        for _ in range(3):
            printTuple = (graphic[3 * _], graphic[(3 * _) + 1], graphic[(3 * _) + 2])
            builtMessage = "    ".join(printTuple)
            await message.channel.send(builtMessage)
        return
    #parses whether the message sent provides a valid tic tac toe board
    isBoard = True
    if(len(message_as_list) == 9):
        for _ in range(9):
            if message_as_list[_] != 'I':
                if message_as_list[_] != 'X':
                    if message_as_list[_] != 'O':
                        isBoard = False
        #Translates inputs to what the bot understands, calls for AI move
        if isBoard:
            isFinished = True
            newBoard = message_as_list
            for _ in range(9):
                if newBoard[_] == 'I':
                    isFinished = False
                    newBoard[_] = ' '
            if not isFinished:
                aiMovePosition = int(ttt.getAIMove(newBoard, "O", "O")[0])
            newBoard[aiMovePosition] = "O"
            #inserts the AI move and produces an output to be sent to chat, as well as any game-ending declarations
            graphic = ttt.printBoard(newBoard)
            for _ in range(3):
                printTuple = (graphic[3 * _], graphic[(3 * _) + 1], graphic[(3 * _) + 2])
                playCount = 0
                for i in range(3):
                    if printTuple[i] != 'I':
                        playCount += 1
                if playCount == 0:
                    builtMessage = "    ".join(printTuple)
                elif playCount == 1:
                    builtMessage = "   ".join(printTuple)
                else:
                    builtMessage = "  ".join(printTuple)
                await message.channel.send(builtMessage)
            if ttt.checkWin(newBoard, 'X'):
                await message.channel.send('You win')
            elif ttt.checkWin(newBoard, 'O'):
                await message.channel.send('I win')
            elif ttt.checkTie(newBoard):
                await message.channel.send('We tied')
        return


client.run(TOKEN)