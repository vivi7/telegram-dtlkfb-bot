#!/usr/bin/env python3

from os import getenv
import subprocess, signal
import argparse
import logging

from time import sleep
from random import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


BOT_VERSION = "1.0"
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")

parser = argparse.ArgumentParser(
    description="Script to search in DataFB."
)
parser.add_argument(
    "--bot_token",
    required=TELEGRAM_BOT_TOKEN == None,
    type=str,
    default=TELEGRAM_BOT_TOKEN,
    help="Bot token",
)
args = parser.parse_args()
bot_token = args.bot_token


def exec_subprocess_cmd(cmd):
    return subprocess.check_output([cmd], shell=True, preexec_fn=lambda: signal.signal(signal.SIGPIPE, signal.SIG_DFL)).decode("utf-8")


def start(update, context):
    update.message.reply_text('Hi! telegram-dtlkfb-bot version: ' + BOT_VERSION)


def help(update, context):
    message = "How to use: data_to_search COUNTRY from list:"
    update.message.reply_text(message)
    countries(update, context)


def countries(update, context):
    cmd = "ls -1 /resources | sed 's/\.[a-z]*//g'"
    output = exec_subprocess_cmd(cmd)
    logger.warning("countries OUTPUT" + output)
    update.message.reply_text(output)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    print(str(context.error))
    update.message.reply_text(str(context.error))
    help(update, context)


def search_fb(update, context):
    text = update.message.text
    arr = text.split()
    string_to_search = arr[0]
    country = "*" if len(arr) <=1 else arr[1]
    cmd = "/app/zgrep " + string_to_search + " /resources/" + country + ".zip"
    output = exec_subprocess_cmd(cmd)
    logger.warning("search_fb OUTPUT" + output)
    # output_list = output_string.splitlines()
    # for e in output_list:
    #     print(e)
    if len(output) > 4096:
        for x in range(0, len(output), 4096):
            update.message.reply_text(output[x:x+4096])
    else:
        update.message.reply_text(output)


def main():
    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher # Get the dispatcher to register handlers

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", countries))
    dp.add_handler(CommandHandler("countries", countries))

    dp.add_handler(MessageHandler(Filters.text, search_fb)) #Filters.regex('^/start$')
    dp.add_error_handler(error)

    updater.start_polling() # Start the Bot
    updater.idle()


if __name__ == '__main__':
    main()

