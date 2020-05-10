from flask import Flask, render_template, request
from generateHTML import generate_html
from telebot import types, TeleBot
from config import *
from database import get_lvl, set_lvl
from json import load

bot = TeleBot(BOT_TOKEN, threaded=__name__ == "__main__")
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route(f"/{SECRET}", methods=["POST"])
def web_hook():
    json_string = request.get_data().decode("utf-8")
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "SpaceDuck", 200


@bot.message_handler(commands=["start"], content_types=["text"])
def start(command):
    set_lvl(command.chat.id, 0)
    bot.send_message(command.from_user.id, command)  # TODO: Welcome text


@bot.message_handler(content_types=["text"])
def instruction(message):
    lvl = get_lvl(message.chat.id)

    content = telegram_data[str(lvl)]["content"]

    for option in content:
        if type(option) is not int:
            continue

        if telegram_data[str(option)]["name"] in message.text:
            send_new_lvl_msg(lvl, message.chat.id)

    else:
        if message.text == "На главную":
            send_new_lvl_msg(0, message.chat.id)

        else:
            bot.send_message(message.from_user.id, "Простите, я вас не понял, попробуйте использовать спициальные кнопки")


def send_new_lvl_msg(lvl, uid):
    keyboard = types.ReplyKeyboardMarkup()
    content = telegram_data[lvl]
    text = []

    for option in content:
        if type(option) is int:
            option_text = telegram_data[str(option)]["name"]

            text.append(option_text)
            keyboard.add(types.KeyboardButton(text=option_text))

        else:
            text.append(option)

    text = "\n".join(text)
    bot.send_message(uid, text, parse_mode="HTML", reply_markup=keyboard)


bot.remove_webhook()
bot.set_webhook(url=f"https://{PYTHONANYWHERE_USERNAME}.pythonanywhere.com/{SECRET}")

with open("static/telegram.json") as telegram_data:
    telegram_data = load(telegram_data)

if __name__ == '__main__':
    generate_html()
    app.run()
