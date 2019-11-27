from discord.ext import commands
import discord
import random

from . import LTPcogs
from . import LTPlib as ltp
from . import Twenty_doors


# はじめに呼び出されるコグ
class General(commands.Cog):

    # コンストラクタ
    def __init__(self, bot):
        self.bot = bot
        # ゲーム中か否かの判断変数。鍵の名前はそのままコグの名前にする
        self.has_started = {'LTPcog': 0, 'Twenty_doors': 0}
        # 以下、デバッグ用設定
        # self.bot.add_cog(LTPcogs.LTPcog(self.bot))

    @commands.command(description="たまにさけびます", brief="おねこさま")
    async def neko(self, n):
        r = random.randint(0, 9)
        nya = "みゃー"
        if r == 0:
            nya = "なーご"
        elif r % 5 == 0:
            r = random.randint(0, 9)
            if r % 4 == 0:
                nya = "ﾐｬ゛ｰｯ!"
            else:
                pass
        else:
            nya = "にゃーん"
        await n.channel.send(nya)

    @commands.command(description="たまにうなります。", brief="おいぬさま")
    async def inu(self, i):
        r = random.randint(0, 9)
        baw = "バウワウ！"
        if r == 0:
            baw = "くぅーん"
        elif r % 5 == 0:
            r = random.randint(0, 9)
            if r % 4 == 0:
                baw = "Grrrrr....."
            else:
                pass
        else:
            baw = "わんっ"
        await i.channel.send(baw)

    @commands.command(description="ウミガメのスープのルールを説明します。",
                      brief="ウミガメのスープのルールを説明します。",
                      aliases=['rdm', 'read'])
    async def readme(self, recieve, *n):
        m = ("■Lateral Thinking Puzzles (ウミガメのスープ)\n"
             "「出題者」が出した文章の真意を「質問者」が解く遊び。\n"
             "「質問者」はYES・NOで答えられる質問を「出題者」にすることができる。\n"
             "Discordで行うにあたって：\n"
             "(1)質問は「」でくくること。「」内文章に対しYES・NOで応対する。\n"
             "(2)解答は『』でくくること。"
             if len(n) == 0 else
             "■20の扉\n"
             "「出題者」が出した問いの答えを「質問者」が探す遊び。\n"
             "「質問者」はYES・NOで答えられる質問を「出題者」にすることができる。\n"
             "ただし、質問ができる回数には限りがある。\n"
             "そのため「質問者」は互いに相談して質問の内容を考えることが推奨される。\n"
             "Discordで行うにあたって：\n"
             "(1)質問は「」でくくること。「」内文章に対しYES・NOで応対する。\n"
             "(2)解答は『』でくくること。\n"
             "(3)相談は「」でも『』でもくくらないこと。")
        await recieve.channel.send(m)
        # sended = await recieve.channel.send(m)
        # await sended.delete(delay=ltp.DELAY_SECONDS_LONGER)

    # ゲーム開始
    @commands.command(description="""ウミガメのスープを開始する際に使用して下さい。
                      ウミガメのスープ関連コマンドを使用できるようにします。""",
                      brief="「ウミガメのスープ」を開始する時に実行するコマンドです")
    async def start(self, ctx):
        if 1 not in self.has_started.values():
            self.has_started['LTPcog'] = 1
            self.bot.add_cog(LTPcogs.LTPcog(self.bot))
            await self.bot.change_presence(
                activity=discord.Game(name="ウミガメのスープ"))
            await ctx.channel.send("ウミガメのスープを開始します")
        else:
            sended = await ctx.channel.send("ゲーム中です！")
            await sended.delete(delay=ltp.DELAY_SECONDS)

    # ゲーム開始
    @commands.command(description="""「20の扉」を開始する際に使用して下さい。
                      「20の扉」関連コマンドを使用できるようにします。""",
                      brief="「20の扉」を開始する時に実行するコマンドです")
    async def start20(self, ctx, *n):
        if 1 not in self.has_started.values():
            self.has_started['Twenty_doors'] = 1
            num = (20
                   if len(n) == 0 else
                   n[0]
                   if ltp.is_num(n[0]) else
                   20)
            self.bot.add_cog(Twenty_doors.Twenty_doors(self.bot, num))
            await self.bot.change_presence(
                activity=discord.Game(name="20の扉"))
            await ctx.channel.send("20の扉を開始します\n質問は{num}回まで可能です")
        else:
            sended = await ctx.channel.send("ゲーム中です！")
            await sended.delete(delay=ltp.DELAY_SECONDS)

    # ゲーム終了
    @commands.group(description="""ゲームを終了する際に使用して下さい。
                    「ウミガメのスープ」/「20の扉」関連コマンドを使用できなくします。
                    また、終了の際にはプレイログを出力します。
                    `?finish nolog`でログを出力せずに終了します。""",
                    brief="「ウミガメのスープ」を終了する時に実行するコマンドです。",
                    aliases=['fin'])
    async def finish(self, ctx):
        if ctx.invoked_subcommand is None:
            now_game = [k for k, v in self.has_started.items() if v == 1]
            if now_game:
                print(now_game)
                self.has_started[now_game[0]] = 0
                log = self.bot.get_cog(now_game[0])
                if log is not None:
                    msg = log.showlog()
                    for i in range(len(msg)):
                        await ctx.channel.send(msg[i])
                self.bot.remove_cog(now_game[0])
                game = "ウミガメのスープ" if now_game[0] == 'LTPcog' else "20の扉"
                await self.bot.change_presence(activity=None)
                m = f"{game}を終了します。"
            else:
                m = "まだゲームが開始されていません。"
        await ctx.channel.send(m)

    @finish.command()
    async def nolog(self, ctx):
        self.has_started = 0
        now_game = [k for k, v in self.has_started.items() if v == 1]
        self.bot.remove_cog(now_game[0])
        await self.bot.change_presence(activity=None)

    '''
    @finish.command()
    async def file(self, ctx):
        self.has_started = 0
        log = self.bot.get_cog('LTPcog')
        if log is not None:
            with codecs.open('log.txt','a','utf-8_sig',"ignore") as f:
                msg = log.showlog()
                for i in range(len(msg)):
                    f.write(msg[i])
            with codecs.open('log.txt','r','utf-8_sig',"ignore") as f:
                await ctx.channel.send(file=discord.File(f))
        self.bot.remove_cog('LTPcog')
        await self.bot.change_presence(activity=None)
    '''

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return


# BOT本体からコグを読み込む際に呼び出される関数
def setup(bot):
    bot.add_cog(General(bot))
