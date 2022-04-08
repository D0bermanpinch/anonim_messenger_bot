import telebot
from telebot import types;
import json
import random
import uuid

BOT = telebot.TeleBot("")
USERS = {}
MESSAGES = {}


try:
    with open("database.json", "r") as dbfile:
        all_lines = dbfile.readlines()
        joined_lines = "".join(all_lines)
        USERS = json.loads(joined_lines)
except:
    pass

try:
    with open("database2.json", "r") as dbfile:
        all_lines = dbfile.readlines()
        joined_lines = "".join(all_lines)
        MESSAGES = json.loads(joined_lines)
except:
    pass

@BOT.message_handler(content_types=['text'])
def on_message(message):
    user_id = str(message.from_user.id)
    if (message.text == '/start') or (message.text == '/help') or (message.text == '/play'):
        if message.text == '/start':
            nick = message.from_user.username
            if not user_id in USERS :
                user_id = str(uuid.uuid4)
                USERS[user_id] = {"nick": nick, "user_id":user_id}
                write_json()
                BOT.send_message(user_id, "Registration successful!\n This bot have a few commands. Check them by writing /help")
            else:    
                BOT.send_message(user_id, "This bot have a few command. Check them by write /help")
        if message.text == "/chat":
            init_chat(user_id,nick)
def init_chat(p1_id, p1_nick):
    p1_nick=USERS[p1_id]['nick']
    p1_id=USERS[p1_id]['user_id']
    all_ids=set(USERS.keys())
    all_ids.remove(p1_id)

    p2_id=random.choice(list(all_ids))
    p2_id=USERS[p2_id]['user_id']
    p2_nick=USERS[p2_id]['nick']
    
    chat_id=str(uuid.uuid4())

    MESSAGES[chat_id] = {'p1_id':p1_id, 'p2_id' : p2_id}
    print(f"Chat created: {chat_id} / {p1_nick} / {p2_nick}")

    BOT.send_message(p1_id, f'You will play with @{p2_nick}')
    BOT.send_message(p2_id, f'You will play with @{p1_nick}')

def chat_process(p1_id, p2_id ,p1_nick, p2_nick, message):
    if message.from_user.username == p1_nick:
        p1_text = message.text
        BOT.send_message(p2_id, p1_text)
    if message.from_user.username == p2_nick:
        p2_text = message.text
        BOT.send_message(p1_id, p2_text)


def init_game2(p1_id, p2_nick):
    p1_nick=USERS[p1_id]['nick']
    all_ids=set(USERS.keys())
    all_ids.remove(p1_id)
    p2_id = None
    if p2_nick == p1_nick:
        '''BOT.send_message(p1_id, 'По-моему ты что-то перепутал')'''
        data = open('1.mp4','rb')
        BOT.send_video(p1_id, data)
        data.close()
    else:
        for (key, value) in USERS.items():
            if value ['nick'] == p2_nick:
                p2_id = key

                game_id=str(uuid.uuid4())

                MESSAGES[game_id] = {'p1_id':p1_id, 'p2_id' : p2_id, 'p1_move' : None, 'p2_move' : None}
                print(f"Game created: {game_id} / {p1_nick} / {p2_nick}")

                BOT.send_message(p1_id, f'You will chat with @{p2_nick}')
                BOT.send_message(p2_id, f'You will chat with @{p1_nick}')
        if p2_id == None:
            BOT.send_message(p1_id, 'This user is not registrated!')
'''def keyboard(game_id, p_id):
    keyboard = types.InlineKeyboardMarkup(); 
    rock = types.InlineKeyboardButton(text='rock', callback_data=f"{game_id}_{p_id}_r")
    paper = types.InlineKeyboardButton(text='paper', callback_data=f"{game_id}_{p_id}_p")
    scissors = types.InlineKeyboardButton(text='scissors', callback_data=f"{game_id}_{p_id}_s")
    keyboard.add(rock) 
    keyboard.add(paper)
    keyboard.add(scissors)

    return keyboard'''


@BOT.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    items = call.data.split("_")
    game_id, p_id, move = items
    nick = USERS[p_id]["nick"]
    print(f"{game_id} {nick} {move}")
    BOT.edit_message_reply_markup(p_id, call.message.id, reply_markup=None)
    process_chat(game_id, p_id, move)

def process_chat(game_id, p_id, move):
    game = MESSAGES.get(game_id)
    if game is None:
        BOT.send_message(p_id, "Sorry, game info was lost somehow! Pls /play again")
    else:
        if p_id == game['p1_id'] and game['p1_move']== None:
            game['p1_move']  = move
            write_json2()
        if p_id == game['p2_id'] and game['p2_move']== None:
            game['p2_move']  = move
            write_json2()
    
def write_json():
    with open('database.json', 'w') as file:
        json_line =  json.dumps(USERS, indent=4, ensure_ascii=False)
        file.write(json_line)
def write_json2():
    with open('database2.json', 'w') as file:
        json_line =  json.dumps(MESSAGES, indent=4, ensure_ascii=False)
        file.write(json_line)

BOT.polling(none_stop=True)
