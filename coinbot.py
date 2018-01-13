import telepot, time, random, emoji, pprint, json, os, sys , schedule, requests
from telepot.namedtuple \
    import InlineKeyboardButton, InlineKeyboardMarkup

urltoken = "http://database98.altervista.org/Bots/pygamebot/token.txt"
action = None

users = {}
admins = [144218415]


def edit_and_log(msg_identifier, text, parse_mode=None, disable_web_page_preview=None, reply_markup=None):
    edit_message(msg_identifier, text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview , reply_markup=reply_markup)
    print("#" + str(action) + " " + str(msg_identifier[0]) + " Edit message: " + text.replace("\n", "").replace("\t", ""))


def create_new_user(chatid: int, msgID: int, name: str, sec_name: str = None, username: str = None, money: int = 0, gevs: int = 5):
    global users
    obj = {}
    obj["msg"] = msgID
    obj["name"] = name
    obj["second_name"] = sec_name
    obj["username"] = username
    obj["money"] = money
    obj["gevs"] = gevs
    users[int(chatid)] = obj


def save_users():
    global users
    # print("Saving users...")
    with open(r".\accounts.json", "w") as file:
        file.write(json.dumps(users))


def load_users():
    global users
    # print("Loading users...")
    if os.path.isfile(r".\accounts.json"):
        with open(r".\accounts.json", "r") as file:
            users = json.loads(file.read())
    else:
        users = {}


def send_and_log(chatid,
                 text,
                 parse_mode=None,
                 disable_web_page_preview=None,
                 disable_notification=None,
                 reply_to_message_id=None,
                 reply_markup=None):
    global bot
    global action
    msg_id = bot.sendMessage(chatid,
                             text, parse_mode=parse_mode,
                             disable_web_page_preview=disable_web_page_preview,
                             disable_notification=disable_notification,
                             reply_to_message_id=reply_to_message_id,
                             reply_markup=reply_markup)
    print("#" + str(action) + "\tRisposta: " + text.replace("\n", " ").replace("\t", ""))
    return msg_id


def chat_handle(msg):
    global action
    global users
    # loadUsers()
    try:
        # pprint.pprint(msg)
        action = random.randint(0, 99999)
        content_type, chat_type, chatid, msg_date, msg_id = telepot.glance(msg, flavor='chat', long=True)
        text = msg["text"].replace("/", "")

        if text == "start":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                 [InlineKeyboardButton(text="🕹 Gioca! 🕹", callback_data="play")],
                 [InlineKeyboardButton(text="👾 Profilo 👾", callback_data="profile"),
                  InlineKeyboardButton(text="📟 Classifica 📟", callback_data="leaderboard")],
                 [InlineKeyboardButton(text="🤖 Info sul bot 🤖", callback_data="info")]
            ])
            msg_id = send_and_log(chatid, "***Benvenuto su pyGameBot! Il primo bot Telegram di mini-giochi!***" +
                                          "\n\n```" + '\t'*12 + "Bot Sviluppato da @MRtecno98```",
                                  parse_mode='Markdown',
                                  reply_markup=keyboard)

            try:
                username = msg["from"]["username"]
            except KeyError:
                username = None

            try:
                surname = msg["from"]["last_name"]
            except KeyError:
                surname = None

            if chatid not in list(users.keys()):
                create_new_user(chatid, msg_id["message_id"], msg["from"]["first_name"], surname, username)
    finally:
        # saveUsers()
        print("", end='')

    return


def callback_handle(msg):
    global action
    global users
    # print(users)
    # loadUsers()
    try:
        action = random.randint(0, 99999)
        callback_id, from_id, data = telepot.glance(msg, flavor="callback_query")
        from_id = str(from_id)
        if data == "profile":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
            ])
            # print(users[from_id]["msg"])
            message = ""
            message += "***Profilo di: " + users[from_id]["name"] + "***\n"
            message += "👱" + "Name: " + users[from_id]["name"] + "\n"
            if users[from_id]["second_name"] is not None: message += "👪" + " Second Name: " \
                                                                     + users[from_id]["second_name"] + "\n"
            if users[from_id]["username"] is not None: message += "🌐" + " Username: " + \
                                                                  users[from_id]["username"] + "\n"
            message += emoji.EMOJI_ALIAS_UNICODE[":credit_card:"] + " Money: " + str(users[from_id]["money"]) + "💎"
            bot.editMessageText((from_id, users[from_id]["msg"]),
                                message,
                                reply_markup=keyboard, parse_mode="Markdown")
            return

        if data == "menu":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🕹 Gioca! 🕹", callback_data="play")],
                [InlineKeyboardButton(text="👾 Profilo 👾", callback_data="profile"),
                 InlineKeyboardButton(text="📟 Classifica 📟", callback_data="leaderboard")],
                [InlineKeyboardButton(text="🤖 Info sul bot 🤖", callback_data="info")]
            ])
            bot.editMessageText((from_id, users[from_id]["msg"]),
                                "***Benvenuto su pyGameBot! Il primo bot Telegram di mini-giochi!***" +
                                "\n\n```" + '\t'*12 + "Bot Sviluppato da @MRtecno98```",
                                reply_markup=keyboard,
                                parse_mode="Markdown")
            return

        if data == "info":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Sviluppatore Bot", url="http://bit.ly/subscribemrtecno")],
                [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
            ])
            bot.editMessageText((from_id, users[from_id]["msg"]),
                                "Bot sviluppato da @MRtecno98\nCopyright 2017 MRtecno98, All Rights Reserved",
                                reply_markup=keyboard)
            return

        if data == "leaderboard":
            moneys = {}
            for user in list(users.values()):
                moneys[user["money"]] = user["username"] if user["username"] is not None else user["name"]
            sort = sorted(moneys)
            sort.reverse()
            sort = sort[:10]
            msg = "💯Leaderboard💯\n"
            for m in sort:
                msg += "@" + moneys[m] + "   " + str(m) + "💎\n"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
            ])
            bot.editMessageText((from_id, users[from_id]["msg"]),
                                msg,
                                reply_markup=keyboard)
            return

        if data == "play":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Sasso Carta Forbice", callback_data="scf"), InlineKeyboardButton(text="Gratta e Vinci", callback_data="gev")],
                [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
            ])
            bot.editMessageText((from_id, users[from_id]["msg"]),
                                "***Scegli il gioco in cui ti vuoi cimentare!***",
                                reply_markup=keyboard,
                                parse_mode="Markdown")
            return

        if data == "scf":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Sasso", callback_data='scf:{"obj":"rock" , "points":0 , "count":0}'),
                 InlineKeyboardButton(text="Carta", callback_data='scf:{"obj":"paper" , "points":0 , "count":0}'),
                 InlineKeyboardButton(text="Forbice", callback_data='scf:{"obj":"forb" , "points":0 , "count":0}')],
                [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
            ])
            bot.editMessageText((from_id, users[from_id]["msg"]),
                                "***Benvenuto su Sasso Carta Fobice, seleziona un oggetto per cominciare!***",
                                reply_markup=keyboard,
                                parse_mode="Markdown")
            return

        if data.startswith("scf:"):
            newData = data[4:]
            obj = json.loads(newData)
            text = ""
            points = obj["points"]
            ogg = obj["obj"]
            count = obj["count"]
            aiobj = ""
            plobj = ""
            ai = random.randint(1, 3)
            if (ai == 1 and ogg == "paper") or (ai == 2 and ogg == "forb") or (ai == 3 and ogg == "rock"):
                text = "***Hai Vinto!***\n___1 Punto è stato aggiunto al tuo conto___"
                points += 1
            if (ai == 1 and ogg == "rock") or (ai == 2 and ogg == "paper") or (ai == 3 and ogg == "forb"):
                text = "***Pareggio***"
            if (ai == 1 and ogg == "forb") or (ai == 2 and ogg == "rock") and (ai == 3 and ogg == "paper"):
                text = "***Hai Perso!***"

            if ai == 1:
                aiobj = "Sasso"
            if ai == 2:
                aiobj = "Carta"
            if ai == 3:
                aiobj = "Forbice"

            if ogg == "rock":
                plobj = "Sasso"
            if ogg == "paper":
                plobj = "Carta"
            if ogg == "forb":
                plobj = "Forbice"

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Sasso", callback_data='scf:{"obj":"rock" , "points":0 , "count":' + str(count+1) + '}'),
                 InlineKeyboardButton(text="Carta", callback_data='scf:{"obj":"paper" , "points":0, "count":' + str(count+1) + '}'),
                 InlineKeyboardButton(text="Forbice", callback_data='scf:{"obj":"forb" , "points":0, "count":' + str(count+1) + '}')],
                [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
            ])

            bot.editMessageText((from_id, users[from_id]["msg"]),
                                "Match N° " + str(count) + "\n\nMossa dell'utente: " + plobj
                                + "\nMossa del computer: " + aiobj + "\n" + text,
                                parse_mode='Markdown',
                                reply_markup=keyboard)

            users[from_id]["money"] += points
            return

        if data == "gev":

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Gratta!", callback_data="geva")],
                [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
            ])
            bot.editMessageText((from_id, users[from_id]["msg"]),
                                """***In questo gioco verranno estratti 2 numeri casuali***
                                se essi saranno uguali vincerai 5 punti!""",
                                reply_markup=keyboard,
                                parse_mode="Markdown")
            return

        if data == "geva":
            if users[from_id]["gevs"] <= 0:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Shop", callback_data="shop")],
                    [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
                ])
                bot.editMessageText((from_id, users[from_id]["msg"]),
                                    "Mi dispiace, per oggi hai terminato tutti i tuoi Gratta & Vinci"
                                    "\n\n                         ***Puoi comprarne altri allo Shop!***",
                                    parse_mode="Markdown",
                                    reply_markup=keyboard
                                    )
                return
            users[from_id]["gevs"] -= 1
            n1 = random.randint(0, 10)
            n2 = random.randint(0, 10)
            add = 0
            if n1 == n2:
                is_valid = "I numeri sono identici!\n___5 punti sono stati aggiunti al tuo conto___"
                add = 5
            else:
                is_valid = "Mi dispiace, i numeri sono diversi."
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Gratta!", callback_data="geva")],
                [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
            ])
            bot.editMessageText((from_id, users[from_id]["msg"]),
                                "Gratta&Vinci rimanenti per oggi: "
                                + str(users[from_id]["gevs"]) + "\n" +
                                "Numero 1: " + str(n1) + "\n"
                                "Numero 2: " + str(n2) + "\n"
                                + is_valid,
                                reply_markup=keyboard,
                                parse_mode="Markdown")
            users[from_id]["money"] += add
            return

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="↩ Torna al menu", callback_data="menu")]
        ])
        bot.editMessageText((from_id, users[from_id]["msg"]),
                            "Questa funzionalità non è ancora disponibile\nA breve verranno attivate tutte le funzioni",
                            reply_markup=keyboard,
                            parse_mode="Markdown")

        return
    finally:
        # saveUsers()
        print("", end='')


def inline_handle(msg):
    global action
    global users
    # loadUsers()
    try:
        action = random.randint(0, 99999)
        return
    finally:
        # saveUsers()
        print("", end='')


def handle(msg):
    global users
    load_users()
    try:
        f = telepot.flavor(msg)
        if f == "chat":
            chat_handle(msg)
        if f == "callback_query":
            callback_handle(msg)
        if f == "inline_query":
            inline_handle(msg)
    finally:
        save_users()


def update_gevs():
    for user in list(users.keys()):
        users[user]["gevs"] = 5


# print(users)
# route = {"chat" : chatHandle , "callback_query" : callbackHandle , "inline_query" : inlineHandle}

request = requests.get(urltoken)
request.raise_for_status()

bot = telepot.Bot(request.text)
edit_message = bot.editMessageText
bot.editMessageText = edit_and_log
bot.message_loop(handle)

update_gevs()
schedule.every().day.do(update_gevs)

while True:
    schedule.run_pending()
    time.sleep(1)
