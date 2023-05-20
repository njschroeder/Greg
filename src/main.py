import string, discord, random, time, json
from discord import Intents
import TicTacToeMaster as ttt 

TOKEN, DEVELOPERS = 'YOUR TOKEN HERE', ('pandomains#5375', "convexpine#8680")

intents = Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
global_cache = {}
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    username_with_tag = str(message.author)
    username = username_with_tag.partition('#')[0]
    message_sent = str(message.content)
    messages = message_sent.split()
    channel = str(message.channel.name)
    is_on = True
    print(f'{username}: {messages} ({channel})')

    if message.author == client.user:
        return
    elif message_sent == '&shutdown' and username_with_tag in DEVELOPERS:
        await message.channel.send('shutting down')
        await client.close()
    elif message_sent == '&stop' and username_with_tag in DEVELOPERS:
        is_on = False
    elif message_sent == '&start' and username_with_tag in DEVELOPERS:
        is_on = True

    # dad joke generator
    dad_joke = dad_joke_generator(messages)
    if is_on and dad_joke:
        await message.channel.send(dad_joke)
        return 

    # quotes sender
    if is_on and message_sent == '&quote':
        quote, name = get_quotes_and_names()
        await message.channel.send(f"{quote}\n'\n{name}")
        return

    # random card generator
    if is_on and message_sent == '&drawcard':
        await message.channel.send(random_card_generator())
        return

    # help functions
    if message_sent == '&help':
        await message.channel.send(get_help_info()) 
        return

    # poll help
    if is_on and message_sent == '&pollhelp':
        await message.channel.send('&newpoll [name]: creates a new poll with provided name (name not required)\n&getresult: returns the result of the poll at this very moment')
        return

    # activate fishgpt
    if is_on and message[0] == "&fishgpt":
        await message.channel.send('fish ' * random.randint(10, 30))
        return 

    # VOTING FUNCTION
    # creates poll, provides instructions
    if is_on and messages[0] == '&newpoll':
        await message.channel.send(create_poll(messages))
        return

    # handles all necessary operations for vote reception
    if is_on and message_sent == 'Y' or message_sent == 'N':
        await message.channel.send(vote_reception())
        return
    
    # gathers results and returns an answer
    if is_on and message_sent == '&getresult':
        await message.chanel.send(gather_results())
        return 

    # speech replicator - uses an input ngram dictionary to attempt to create new sentences that could exist from it
    if is_on and messages[0] == '&createsentence':
        await message.chanel.send(create_sentence(messages))
        return

    # thymecheck
    if is_on and message_sent == '&thymecheck':
        await message.channel.send(thyme_check())
        return

    # rock paper scissors
    if is_on and messages[0] == '&rps':
        await message.chanel.send(rock_paper_scissors(messages))
        return

    if is_on and message[0] == "&suggestions":
        with open("src/suggestions.txt", "a") as f:
            f.write(f"{username_with_tag} : {message[1:]}")
        await message.chanel.send("Thanks for your suggestion!")
        return 
    
    if is_on and message_sent == "&verify":
        await message.chanel.send("Coming soon! This feature isn't available yet.")
        return 

    print(messages)

    # TIC-TAC-TOE BOT
    # prepares new game
    if is_on and message_sent == '&newttt':
        await message.channel.send('Instructions: Copy each board when provided, then add in your move as X into an available space')
        graphic = ttt.printBoard([" ", " ", " ", " ", " ", " ", " ", " ", " "])
        for i in range(3):
            printTuple = (graphic[3 * i], graphic[(3 * i) + 1], graphic[(3 * i) + 2])
            builtMessage = "    ".join(printTuple)
            await message.channel.send(builtMessage)
        return
    # parses whether the message sent provides a valid tic tac toe board
    isBoard = True
    if is_on and (len(messages) == 9):
        for i in range(9):
            if messages[i] != 'I':
                if messages[i] != 'X':
                    if messages[i] != 'O':
                        isBoard = False
        # Translates inputs to what the bot understands, calls for AI move
        if isBoard:
            isFinished = True
            newBoard = messages
            for _ in range(9):
                if newBoard[_] == 'I':
                    isFinished = False
                    newBoard[_] = ' '
            if not isFinished:
                aiMovePosition = int(ttt.getAIMove(newBoard, "O", "O")[0])
            newBoard[aiMovePosition] = "O"
            # inserts the AI move and produces an output to be sent to chat, as well as any game-ending declarations
            graphic = ttt.printBoard(newBoard)
            for i in range(3):
                printTuple = (graphic[3 * i], graphic[(3 * i) + 1], graphic[(3 * i) + 2])
                playCount = 0
                for j in range(3):
                    if printTuple[j] != 'I':
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

def dad_joke_generator(messages):
    for i in range(len(messages) - 1):
        word = messages[i].lower()
        next_word = messages[i+1].lower()
        if word in ("im", "i'm", "i am"):
            add_up_return = ''
            for j in range(i + 4):
                try:
                    add_up_return += ' ' + messages[i + j + 1]
                except IndexError:
                    break
            return f'Hi {add_up_return}, I\'m Greg!'
    return None

def get_quotes_and_names(): 
    if "Quotes and Names" in global_cache:
        quotes, names = global_cache[(quotes, names)]
        quote = random.choice(quotes)
        name = random.choice(names)
        return quote, name

    with open("Greg/Quotes/unique_quotes.json") as q:
        quotes_and_names = json.load(q)

        quotes, names = [], []
        for i in quotes_and_names["data"]:
            quotes.append(i["quote"])
            names.append("-" + i["author"])

    global_cache["Quotes and Names"] = (quotes, names)
    quote = random.choice(quotes)
    name = random.choice(names)
    return quote, name

def random_card_generator():
    card_names = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']    
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    card = random.choice(card_names)
    suit = random.choice(suits)
    return f'Your card is the {card} of {suit}!'

def get_help_info():
    help_info = [ '&quote: returns a random quote from the 2358 quotes pages \n&drawcard: returns a random card value \n&pollhelp: provides information about the polling functionality',
                  '\n&createsentence [ngrams] [desired length]: creates a new sentence generated using the provided words as an ngram dictionary',
                  '\n&thymecheck: returns the price of thyme, using an ounce count the same as CDT\'s 24-hour time value',
                  '\n&rps [move]: runs a round of rock paper scissors. Your move should be the full word (rock, paper, or scissors)', 
                  '\n&newttt: provides a blank tic tac toe board and instructions to play' ]
    return "".join(help_info)

def create_poll(messages):
    poll_name = ''
    for message in range(1, len(messages)):
        poll_name += messages[message] + ' '
    if not poll_name:
        return 'poll '
    return f'**NEW POLL** \n\n{poll_name}\n \nSend "Y" to vote yes and "N" to vote no. I will confirm that your vote has been received in chat. You *can* change your vote later if you so wish \n \n **DO NOT** spam your votes'

def vote_reception():
    # determines which file code should read and which to manipulate
    key_1 = 'ResultStore1.txt'
    key_2 = 'ResultStore2.txt'
    read_key = ''
    f1 = open(key_1, 'r') 
    f2 = open(key_2, 'r')
    f1_contents = f1.read()
    f2_contents = f2.read()
    f2_0 = None
    message = ''
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
        message = 'Error! Could not determine proper file to contact. Please launch a new poll'

    # records vote (making sure to not allow double votes)
    vote_store = open(read_key, 'r')
    writeable_votes = open(write_key, 'a')
    yet_to_vote = True
    voteString = vote_store.read()
    votes = voteString.split()
    for idx, val in enumerate(votes):
        try:
            if votes[idx - 1] == username:
                writeable_votes.write(f' {message_sent} ')
                yet_to_vote = False
            else:
                writeable_votes.write(val)
        except IndexError:
            writeable_votes.write(val)
    if yet_to_vote:
        writeable_votes.write(f'{username} : {message_sent}')
    with open(read_key, 'w') as _:
        pass
    if message_sent == 'Y':
        message = f'{username}, you have updated your vote to yes on this poll'
    if message_sent == 'N':
        message = f'{username}, you have updated your vote to no on this poll'
    f1.close()
    f2.close()
    if f2_0:
        f2_0.close()
    vote_store.close()
    writeable_votes.close()
    return message

def gather_results():
    check_correct = True
    vote_counts = [0, 0]
    key_1 = 'ResultStore1.txt'
    key_2 = 'ResultStore2.txt'
    f1 = open(key_1, 'r')
    f2 = open(key_2, 'r')
    f1_contents = f1.read()
    f2_contents = f2.read()
    read_key = ''
    message = 'Nothing happened :/'
    if f1_contents == '' and f2_contents == '':
        message = 'Error! No votes logged'
    if f1_contents == '':
        vote_store = f2_contents
    elif f2_contents == '':
        vote_store = f1_contents
    else:
        message = 'Error! Votes logged incorrectly. Please launch a new poll'
    votes = vote_store.split()
    # checks vote assortment to ensure that nobody has multiple votes
    for i in range(0, len(votes), 2):
        for a in range(i + 2, len(votes), 2):
            if votes[i] == votes[a]:
                message = 'Error! Someone has multiple votes logged. Please launch a new poll'
                check_correct = False
                return
    if check_correct:
        for i in range(1, len(votes), 2):
            if votes[i] == 'Y':
                vote_counts[0] += 1
            elif votes[i] == 'N':
                vote_counts[1] += 1
        message = f'the supporters count {vote_counts[0]} the opponents count {vote_counts[1]}' 
    f1.close()
    f2.close()
    return message

def create_sentence(messages):
    # creates the ngram dictionary from which the code can pull
        custom_length = 1
        words = {}
        if len(messages) <= 3:
            return 'Your ngram dictionary is too short! Try again with a longer one'
        if messages[len(messages)-1].isnumeric():
            custom_length = 2
        for _ in range(1, len(messages) - custom_length):
            outValue = words.setdefault(messages[_], [messages[_ + 1]])
            if outValue != [messages[_ + 1]]:
                outValue.append(messages[_ + 1])
                words.pop(messages[_])
                words.setdefault(messages[_], outValue)

        # generates sentence from ngrams provided
        send_string = ''
        next_key = messages[1]
        send_string += next_key
        length_cap = 15
        if custom_length == 2:
            length_cap = int(messages[len(messages)-1])
        for _ in range(length_cap - 1):
            try:
                nextWord = random.choice(dict.get(next_key))
                send_string += ' ' + nextWord
                next_key = nextWord
            except TypeError:
                return send_string             
        return send_string

def thyme_check():
    unix_time = time.time()
    CDT_unix = unix_time - 18000 # a very odd way to shift time zone sure, but it's easier than all the if statements for the past 00:00 edge case
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
    price_decimal = ounces * 39.7 # uses wrong conversion rate, should be 0.397, but this makes truncating to 2 decimals easier
    price_int = int(price_decimal)
    price = price_int / 100
    return f'{ounces} ounces of thyme would cost ${price}'

def rock_paper_scissors(messages):
    error = 'Error! No valid move provided. Please provide a valid move'
    try:
        if messages[1] == 'rock' or messages[1] == 'paper' or messages[1] == 'scissors':
            opponent_move = messages[1]
            move_list = ['rock', 'paper', 'scissors']
            bot_move = random.choice(move_list)
            if opponent_move == 'rock':
                if bot_move == 'rock':
                    return f'You used {opponent_move}, and I used {bot_move}. Tie game!'
                elif bot_move == 'paper':
                    return f'You used {opponent_move}, and I used {bot_move}. I win!'
                elif bot_move == 'scissors':
                    return f'You used {opponent_move}, and I used {bot_move}. You win!'
        
            elif opponent_move == 'paper':
                if bot_move == 'rock':
                    return f'You used {opponent_move}, and I used {bot_move}. You win!'
                elif bot_move == 'paper':
                    return f'You used {opponent_move}, and I used {bot_move}. Tie game!'
                elif bot_move == 'scissors':
                    return f'You used {opponent_move}, and I used {bot_move}. I win!'

            elif opponent_move == 'scissors':
                if bot_move == 'rock':
                    return f'You used {opponent_move}, and I used {bot_move}. I win!'
                elif bot_move == 'paper':
                    return f'You used {opponent_move}, and I used {bot_move}. You win!'
                elif bot_move == 'scissors':
                    return f'You used {opponent_move}, and I used {bot_move}. Tie game!'
            else:
                return error
    except IndexError:
        return error

client.run(TOKEN)