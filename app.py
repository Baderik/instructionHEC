from flask import Flask, render_template, request
from generateHTML import generate_html
from telebot import types, TeleBot
from config import *

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
    bot.send_message(command.from_user.id, command)  # TODO: Welcome text


@bot.message_handler(content_types=["text"])
def instruction(message):
    bot.send_message(message.from_user.id, message)


bot.remove_webhook()
bot.set_webhook(url=f"https://{PYTHONANYWHERE_USERNAME}.pythonanywhere.com/{SECRET}")

if __name__ == '__main__':
    generate_html()
    app.run()
