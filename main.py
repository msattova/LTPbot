#! coding: utf-8

from discord.ext import commands
import os
import traceback

TOKEN = os.environ["TOKEN"]
BOT_PREFIX = '?'
INITIAL_EXTENSIONS = [
        'cogs.General'
]


class LTPbot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print('------')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


def main():
    bot = LTPbot(command_prefix=BOT_PREFIX)
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
