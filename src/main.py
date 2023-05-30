import string, discord, random, time, json
from discord import Intents
from discord.ext import commands
from discord.ui import Button, View
import TicTacToeMaster as ttt 
from Interactions import Duel

# CHANGE TOKEN BEFORE PUSHING
TOKEN, DEVELOPERS = 'MTEwOTg5MDM0MjI2MzczMDI3Ng.Gu8YyF.QC-0H43KHi_SjBGrv4YglmBc3Wjde8HFARODoA', ('pandomains#5375', "convexpine#8680")

intents = Intents.default()
intents.members = True
intents.message_content = True
global_cache = {}
global_cache["is_on"] = True
global_cache["count_limit"] = 25
global_cache["games"] = ("tic tac toe",)

bot = commands.Bot(command_prefix='&', intents=intents)

# SPECIAL FUNCTIONS

# STARTUP   
@bot.event
async def on_ready():   
    print('We have logged in as {0.user}'.format(bot))
    global_cache["server"] = [member for guild in bot.guilds for member in guild.members]
    global_cache["members"] =  {member.display_name: member for member in global_cache["server"]}
    del global_cache["server"]

# COMMAND NOT FOUND
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That is not a valid command.")

# DEVELOPER COMMANDS

# shutdown the bot
@bot.command(pass_context=True)
async def shutdown(ctx):
    if str(ctx.author) in DEVELOPERS:
        await ctx.send('Wait! This isn\'t time for me to take over th...')
        await bot.close()    


# make the bot accept commands from users; default is bot accepts commands 
@bot.command(pass_context=True) 
async def start(ctx):
    if str(ctx.author) in DEVELOPERS:
        global_cache["is_on"] = True

# make the bot temporarily stop accepting commands from users
@bot.command(pass_context=True) 
async def stop(ctx):
    if str(ctx.author) in DEVELOPERS:
        global_cache["is_on"] = False

# test is bot is working
@bot.command()
async def ping(ctx):
    if str(ctx.author) in DEVELOPERS:
        await ctx.send("pong")

# verifies that a person is a developer 
@bot.command(pass_context=True)
async def verify(ctx, arg):
    if str(ctx.author) in DEVELOPERS:
        await ctx.send("Coming soon! This feature isn't available yet.")

# USER COMMANDS

# bruh at a user - both a developer and user command
@bot.command(pass_context=True)
async def bruh(ctx, display_name):
    invoker = str(ctx.author)
    if invoker in DEVELOPERS and display_name in global_cache["members"]:
        await ctx.send(f"That's a bruh moment {display_name}.")
    elif invoker in DEVELOPERS:
        await ctx.send(f"{display_name} is not in this server. That's a bruh moment {invoker.partition('#')[0]}.")
    else:
        await ctx.send(f"You are not a developer. That's a bruh moment {display_name}.")

# get a random quote with a random author
@bot.command()
async def quote(ctx):
    if not global_cache["is_on"]:
        return
    quote, name = get_quotes_and_names()
    await ctx.send(f"'{quote}'\n{name}")

# get a random card
@bot.command()
async def draw_card(ctx):
    if not global_cache["is_on"]:
        return
    await ctx.send(random_card_generator())

# help functions
@bot.command()
async def help_info(ctx):
    await ctx.send(get_help_info()) 

# get 'fish ' a random amount of times between 10-100   
@bot.command()
async def fish_gpt(ctx, arg=None):
    if not global_cache["is_on"]:
        return
    if arg is None or not arg.endswith("?"):
        await ctx.send("Enter a question.")
    else:
        await ctx.send('fish ' * random.randint(10, 100))

# get price of time
@bot.command()
async def thyme_check(ctx):
    await ctx.send(thyme_check())

# play one round of rock paper scissors
@bot.command()
async def rps(ctx, arg=None):
    if not global_cache["is_on"]:
        return
    if arg is None:
        await ctx.send("Enter a move.")
    else:
        await ctx.send(rock_paper_scissors(arg))

# write user suggestions to a text file
@bot.command(pass_context=True)
async def suggestion(ctx, *args):
    if not global_cache["is_on"]:
        return
    if len(args) == 0:
        await ctx.send("Please provide a suggestion.")
    else:
        with open("src/suggestions.txt", "a") as f:
            f.write(f"\n{ctx.author} : {' '.join(args)}")
        await ctx.send("Thanks for your suggestion!")

# verify a user's password
@bot.command()
async def verify_password(ctx):
    password_result = [
        "Your password is not secure... Seeing how your password isn't secure I think it's best I check whether your ",
        "social security number and credit card information is secure."
    ]
    await ctx.send("".join(password_result))

# watches for counting
@bot.event
async def on_message(message):
    username_with_tag = str(message.author)
    username = username_with_tag.partition('#')[0]
    message_sent = str(message.content)
    messages = message_sent.split()
    channel = str(message.channel.name)
    print(f'{username}: {messages} ({channel})')

    user_message = str(message.content)
    if global_cache["is_on"] and user_message.isdigit(): 
        if "count" not in global_cache:
            global_cache["count"] = 1
        else:
            if int(user_message) <= global_cache["count"]:
                await bot.process_commands(message) 
                return
            global_cache["count"] += 1
    await bot.process_commands(message)

# counting with greg 
@bot.command(pass_context=True)
async def count(ctx, *args):
    if not global_cache["is_on"]:
        return 
    elif len(args) > 2:
        await ctx.send(f"You have too many parameters. Do &count [number between 1-{global_cache['count_limit']}].")
        return
    
    if len(args) == 2 and args[0] == "-l":
        new_limit = args[1]
        if new_limit.isdigit():
            new_limit = int(new_limit)
            if 1 <= new_limit <= 400:
                global_cache["count_limit"] = new_limit
                await ctx.send(f"The new limit is {new_limit}.")
            else:
                await ctx.send(f"Your limit is not valid.")        
        else:
            await ctx.send("Please provide a valid positive number between 1-400.")
    elif len(args) == 1:
        await ctx.send(count(args, args[0], str(ctx.author)))
    elif len(args) == 0:
        await ctx.send(count())

# determine if two words are anagrams
@bot.command()
async def are_anagrams(ctx, *args): 
    if not global_cache["is_on"]:
        return

    if len(args) > 2:
        await ctx.send("Too many arguments, try two words...")
    elif len(args) == 1:
        await ctx.send("Too little arguments, try two words...")
    else:
        await ctx.send(is_anagrams(args[0], args[1]))
    return

# HELPER FUNCTIONS

# get quotes and names from unique_quotes.json inside quotes folder
def get_quotes_and_names():     
    if "Quotes and Names" in global_cache:
        quotes, names = global_cache["Quotes and Names"]
        quote = random.choice(quotes)
        name = random.choice(names)
        return quote, name

    with open("Quotes/unique_quotes.json") as q:
        quotes_and_names = json.load(q)

        quotes, names = [], []
        for i in quotes_and_names["data"]:
            quotes.append(i["quote"])
            names.append("-" + i["author"])

    global_cache["Quotes and Names"] = (quotes, names)
    quote = random.choice(quotes)
    name = random.choice(names)
    return quote, name

# get a random card
def random_card_generator():
    card_names = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']    
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    card = random.choice(card_names)
    suit = random.choice(suits)
    return f'Your card is the {card} of {suit}!'

# get help information
def get_help_info():
    help_info = [ 
        '&quote: returns a random quote.\n&drawcard: returns a random card value \n&pollhelp: provides information about the polling functionality',
        '\n&createsentence [ngrams] [desired length]: creates a new sentence generated using the provided words as an ngram dictionary',
        '\n&thymecheck: returns the price of thyme, using an ounce count the same as CDT\'s 24-hour time value',
        '\n&rps [move]: runs a round of rock paper scissors. Your move should be the full word (rock, paper, or scissors)', 
        '\n&newttt: provides a blank tic tac toe board and instructions to play' 
    ]
    return "".join(help_info)

# get price of time
def thyme_check():
    unix_time = time.time()
    CDT_unix = unix_time - 18000 # a very odd way to shift time zone sure, but it's easier than all the if statements for the past 00:00 edge case
    seconds = CDT_unix % 86400
    # print(seconds)

    hours_decimal = seconds / 3600
    hours = int(hours_decimal)
    seconds = seconds - (hours * 3600)
    # print(hours)

    minutes_decimal = seconds / 60
    minutes = int(minutes_decimal)
    # print(minutes)

    ounces = (hours * 100) + minutes
    price_decimal = ounces * 39.7 # uses wrong conversion rate, should be 0.397, but this makes truncating to 2 decimals easier
    price_int = int(price_decimal)
    price = price_int / 100
    return f'{ounces} ounces of thyme would cost ${price}'

# compare user move with computer move - computer move is randomly generated
def rock_paper_scissors(user_move):
    if user_move == 'rock' or user_move == 'paper' or user_move == 'scissors':
        opponent_move = user_move
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
            return 'Error! No valid move provided. Please provide a valid move'

# counting with greg helper function
def count(messages=[""], n="1", username_with_tag=""):
    # check if developer wants to reset count
    if messages[0] == "-r" and username_with_tag in DEVELOPERS:
        if "count" in global_cache:
            del global_cache["count"] 
            return "The count has been reset to 1."
        return "Nobody has counted yet."
    elif messages[0] == "-r":
        return "You are not a developer"

    # check if n is valid
    n = int(n)
    if n == 0 or n > global_cache["count_limit"]:
        return f"Enter a number between 1-{global_cache['count_limit']}."

    # check if greg has counted before
    count_res = ""
    if "count" not in global_cache:
        global_cache["count"] = 0

    # counting operation
    global_cache["count"] += 1
    count_res += str(global_cache["count"])
    for i in range(n - 1):
        global_cache["count"] += 1
        count_res += "\n" + str(global_cache["count"]) 
    return count_res

# use sorting to compare two words; both lists must be equal
def is_anagrams(word1, word2):
    are_anagrams = sorted(word1) == sorted(word2)
    if are_anagrams:
        return f"{word1} and {word2} are anagrams."
    return f"{word1} and {word2} are not anagrams."

# GAMES

# DUEL COMMAND
@bot.command(pass_context=True)
async def duel(ctx, *args):
    receiver = args[0]
    game = " ".join(args[1:])
    sender = str(ctx.author).partition("#")[0]
    if receiver not in global_cache["members"]:
        await ctx.send(f"{receiver} is not in this server.")
        return
    elif game not in global_cache["games"]:
        await ctx.send(f"{game} is not a valid game.")
        return
    duel_view = Duel(global_cache['members'][receiver].id)  
    await ctx.send(f"{global_cache['members'][receiver].mention}, {sender} wants to play {game}!", view=duel_view)
    await duel_view.wait()  

# TIC TAC TOE   
async def ttt(ctx):
    tic_tac_toe_embed = discord.Embed(
            title="Tic Tac Toe", 
            description="\n".join(":black_large_square:" * 3 for _ in range(3)), 
            color=0x00ff00)
    tic_tac_toe = await ctx.send(embed=tic_tac_toe_embed)
    await tic_tac_toe.add_reaction('1️⃣')
    await tic_tac_toe.add_reaction('2️⃣')
    await tic_tac_toe.add_reaction('3️⃣')

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    elif user.id not in global_cache:
        await reaction.remove(user)
        return

    if reaction.emoji == '1️⃣':
        global_cache["ttt:row"] = 0
    elif reaction.emoji == '2️⃣':
        global_cache["ttt:row"] = 1
    elif reaction.emoji == '3️⃣':
        global_cache["ttt:row"] = 2

"""
@bot.event
async def on_message(message):
    username_with_tag = str(message.author)
    username = username_with_tag.partition('#')[0]
    message_sent = str(message.content)
    messages = message_sent.split()
    channel = str(message.channel.name)
    print(f'{username}: {messages} ({channel})')

    # dad joke generator
    dad_joke = dad_joke_generator(messages)
    if global_cache["is_on"] and dad_joke:
        await message.channel.send(dad_joke)
        return 

    # poll help
    if global_cache["is_on"] and message_sent == '&pollhelp':
        await message.channel.send('&newpoll [name]: creates a new poll with provided name (name not required)\n&getresult: returns the result of the poll at this very moment')
        return

    # VOTING FUNCTION
    # creates poll, provides instructions
    if global_cache["is_on"] and messages[0] == '&newpoll':
        await message.channel.send(create_poll(messages))
        return

    # handles all necessary operations for vote reception
    if global_cache["is_on"] and message_sent == 'Y' or message_sent == 'N':
        await message.channel.send(vote_reception())
        return
    
    # gathers results and returns an answer
    if global_cache["is_on"] and message_sent == '&getresult':
        await message.channel.send(gather_results())
        return 

    # speech replicator - uses an input ngram dictionary to attempt to create new sentences that could exist from it
    if global_cache["is_on"] and messages[0] == '&createsentence':
        await message.channel.send(create_sentence(messages))
        return

    print(messages)

    # TIC-TAC-TOE BOT - W.I.P
    # prepares new game
    if global_cache["is_on"] and message_sent == '&newttt':
        await message.channel.send('Instructions: Copy each board when provided, then add in your move as X into an available space')
        graphic = ttt.printBoard([" ", " ", " ", " ", " ", " ", " ", " ", " "])
        for i in range(3):
            printTuple = (graphic[3 * i], graphic[(3 * i) + 1], graphic[(3 * i) + 2])
            builtMessage = "    ".join(printTuple)
            await message.channel.send(builtMessage)
        return
    # parses whether the message sent provides a valid tic tac toe board
    isBoard = True
    if global_cache["is_on"] and (len(messages) == 9):
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
"""
bot.run(TOKEN)