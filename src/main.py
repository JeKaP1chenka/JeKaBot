import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

from dotenv import load_dotenv

from config import *

import vtc

load_dotenv()

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! Write /help")


@dp.message(Command(commands="vtc", prefix="!"))
async def vtc_command_handler(message: Message, command: CommandObject) -> None:
    await vtc.process_vtc_command(message, command, False)


@dp.message(Command(commands="vtccrop", prefix="!"))
async def vtc_command_handler(message: Message, command: CommandObject) -> None:
    await vtc.process_vtc_command(message, command, True)


@dp.message(Command("help"))
async def help_command_handler(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer(TEXT_HELP,parse_mode="HTML")
        return
    args_ = list(filter(None, command.args.split(" ")))
    if args_[0] in TEXTS_HELP_COMMANDS:
        await message.answer(TEXTS_HELP_COMMANDS[args_[0]], parse_mode="HTML")


async def main() -> None:
    bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())