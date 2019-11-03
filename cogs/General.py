from discord.ext import commands
import discord
import random

from . import LTPcogs

# はじめに呼び出されるコグ
class General(commands.Cog):
    # ウミガメのスープ開始状態か否かの判断変数(:bool)
    has_started = 0

    #コンストラクタ
    def __init__(self, bot):
        self.bot = bot
        self.has_started = 0
        # 以下、デバッグ用設定
        #self.bot.add_cog(LTPcogs.LTPcog(self.bot))

    @commands.command(description="たまにさけびます",brief="おねこさま")
    async def neko(self, n):
        r = random.randint(0,9)
        nya = "みゃー"
        if r == 0:
            nya = "なーご"
        elif r%5 == 0:
            r = random.randint(0,9)
            if r%4 == 0:
                nya = "ﾐｬ゛ｰｯ!"
            else:
                pass
        else :
            nya = "にゃーん"
        await n.channel.send(nya)

    @commands.command(description="たまにうなります。",brief="おいぬさま")
    async def inu(self, i):
        r = random.randint(0,9)
        baw = "バウワウ！"
        if r == 0:
            baw = "くぅーん"
        elif r%5 == 0:
            r = random.randint(0,9)
            if r%4 == 0:
                baw = "Grrrrr....."
            else:
                pass
        else :
            baw = "わんっ"
        await i.channel.send(baw)

    @commands.command(description="ウミガメのスープのルールを説明します。",brief="ウミガメのスープのルールを説明します。")
    async def readme(self, recieve):
        m = """■Lateral Thinking Puzzles (ウミガメのスープ)
「出題者」が出した文章の真意を「質問者」が解く遊び。
「質問者」はYES・NOで答えられる質問を「出題者」にすることができる。
Discordで行うにあたって：
(1)質問は「」でくくること。「」内文章に対しYES・NOで応対する。
(2)解答は『』でくくること。"""
        await recieve.channel.send(m)

    # ゲーム開始
    @commands.command(description="ウミガメのスープを開始する際に使用して下さい。ウミガメのスープ関連コマンドを使用できるようにします。", brief="「ウミガメのスープ」を開始する時に実行するコマンドです")
    async def start(self, ctx):
        if self.has_started == 0:
            self.has_started = 1
            self.bot.add_cog(LTPcogs.LTPcog(self.bot))
            await self.bot.change_presence(activity=discord.Game(name="ウミガメのスープ"))
            await ctx.channel.send("ウミガメのスープを開始します")
        else :
            await ctx.channel.send("ウミガメのスープは既に始まっています")

    # ゲーム終了
    @commands.group(description="ウミガメのスープを終了する際に使用して下さい。ウミガメのスープ関連コマンドを使用できなくします。また、終了の際にはプレイログを出力します。\n`?finish nolog`でログを出力せずに終了します。", brief="「ウミガメのスープ」を終了する時に実行するコマンドです。",aliases=['fin'])
    async def finish(self, ctx):
        if ctx.invoked_subcommand is None:
            self.has_started = 0
            log = self.bot.get_cog('LTPcog')
            if log is not None:
                msg = log.showlog()
                for i in range(len(msg)):
                    await ctx.channel.send(msg[i])
            self.bot.remove_cog('LTPcog')
            await self.bot.change_presence(activity=None)
        await ctx.channel.send("ウミガメのスープを終了します")

    @finish.command()
    async def nolog(self,ctx):
        self.has_started = 0
        self.bot.remove_cog('LTPcog')
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