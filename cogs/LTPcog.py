from discord.ext import commands
import discord
import re
import random
from datetime import datetime, timedelta, timezone

# はじめに呼び出されるコグ
class General(commands.Cog):
    # ?startコマンドを打たないと、コマンドが認識されないようにするための判断変数(:bool)
    has_started = 0
    
    #コンストラクタ
    def __init__(self, bot):
        self.bot = bot
        self.has_started = 0
        # 以下、デバッグ用設定
        #self.bot.add_cog(LTPcog(self.bot))
    
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
        self.has_started = 1
        self.bot.add_cog(LTPcog(self.bot))
        await self.bot.change_presence(activity=discord.Game(name="ウミガメのスープ"))
        await ctx.channel.send("ウミガメのスープを開始します")
    
    # ゲーム終了
    @commands.command(description="ウミガメのスープを終了する際に使用して下さい。ウミガメのスープ関連コマンドを使用できなくします。また、終了の際にはプレイログを出力します。", brief="「ウミガメのスープ」を終了する時に実行するコマンドです。")
    async def finish(self, ctx):
        self.has_started = 0
        log = self.bot.get_cog('LTPcog')
        if log is not None:
            msg = log.showlog()
            await ctx.channel.send(msg)
        self.bot.remove_cog('LTPcog')
        await self.bot.change_presence(activity=None)
        await ctx.channel.send("ウミガメのスープを終了します")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return


#コグとして用いるクラスを定義
class LTPcog(commands.Cog):
    # Q1などをキーとする質問辞書
    questions = {}
    # A1などをキーとする解答辞書
    answers = {}
    # playlog用時刻記録ディクショナリ
    # timelog仕様
    # キー：質問や解答に割り当てられた英数字(Q1やA1など)。応答に対しては、英数字末尾に'r'を追加する。
    # 値：質問や解答、応答がなされた時刻
    timelog = {}
    # Q1rなどをキーとする質問への応答辞書
    reply_q = {}
    # A1rなどをキーとする解答への応答辞書
    reply_a = {}

    # questionsやanswersへのキーのリスト
    q_key = []
    a_key = []
    start_time = ""

    #コンストラクタ
    def __init__(self, bot):
        self.bot = bot
        self.questions = {}
        self.answers = {}
        self.timelog = {}
        self.reply_q = {}
        self.reply_a = {}
        self.q_key = []
        self.a_key = []
        self.start_time = jst_now()

    #質問・解答追加処理関数
    def add_to_dic(self, msg:str,qora:bool):
        if qora:
            qa = "Q"
            num = len(self.q_key)+1
            self.q_key.append(f"{qa}{num}")
            self.questions[self.q_key[num-1]] = msg
            self.reply_q[f"{self.q_key[num-1]}r"] = ""
            self.timelog[self.q_key[num-1]] = datetime.now().strftime("%Y/%m/%d %H:%M")
            self.timelog[f"{self.q_key[num-1]}r"] = ""
        else:
            qa = "A"
            num = len(self.a_key)+1
            self.a_key.append(f"{qa}{num}")
            self.answers[self.a_key[num-1]] = msg
            self.reply_a[f"{self.a_key[num-1]}r"] = ""
            self.timelog[self.a_key[num-1]] = datetime.now().strftime("%Y/%m/%d %H:%M")
            self.timelog[f"{self.a_key[num-1]}r"] = ""


    #質問や解答への返答処理関数
    def respond(self, num:int, s:str, qora:bool):
        s = s.split()
        if qora :
            k = self.q_key[num-1]
            self.reply_q[f"{k}r"] = s[1]
            self.timelog[f"{k}r"] = datetime.now().strftime("%Y/%m/%d %H:%M")
        else :
            k = self.a_key[num-1]
            self.reply_a[f"{k}r"] = s[1]
            self.timelog[f"{k}r"] = datetime.now().strftime("%Y/%m/%d %H:%M")

    @commands.command(description="""これまでに出た質問(「」で囲まれた言葉)の履歴を表示します。""",brief="これまでに出た解答の履歴を表示します。")
    async def list(self, history):
        
        m = ""
        line = ""
        if len(self.q_key) == 0 :
            m="まだ質問がされていません"
        else:
            
            for i in range(len(self.q_key)):
                line = template(self.q_key[i], self.questions[self.q_key[i]], self.reply_q[self.q_key[i]+'r'])
                m = f'{m}{line}\n'
        print(m)
        await history.channel.send(m)

    @commands.command(description="""これまでに出た解答(『』で囲まれた言葉)の履歴を表示します。""",brief="これまでに出た解答の履歴を表示します。")
    async def lista(self, history):
        m = ""
        line = ""
        if len(self.a_key) == 0 :
            m="まだ解答がされていません"
        else:
            for i in range(len(self.a_key)):
                line = template(self.a_key[i], self.answers[self.a_key[i]], self.reply_a[self.a_key[i]+"r"])
                m = f'{m}{line}\n'
                print(m)
        await history.channel.send(m)

    @commands.command(description="""質問を修正します。
*使用方法*
?req (修正したい質問番号) (質問の修正)""",brief="質問の修正ができます。")
    async def req(self, ctx,num:int, s:str):
        if len(self.q_key) > (num-1) :
            k = self.q_key[num-1]
            self.questions[k] = s
            self.reply_q[f"{k}r"] = ""
            self.timelog[k] = datetime.now().strftime("%Y/%m/%d %H:%M")
            self.timelog[f"{k}r"] = ""
            m = f"Q{num}の変更を受理しました。"
        else:
            m = f"Error! Q{num}はまだ存在しません"
        await ctx.channel.send(m)

    @commands.command(description="""解答を修正します。
*使用方法*
?rea (修正したい解答番号) (解答の修正)""",brief="解答の修正ができます。")
    async def rea(self, ctx,num:int, s:str):
        if len(self.a_key) > (num-1) :
            k = self.a_key[num-1]
            self.answers[k] = s
            self.reply_a[f"{k}r"] = ""
            self.timelog[k] = datetime.now().strftime("%Y/%m/%d %H:%M")
            self.timelog[f"{k}r"] = ""
            m = f"A{num}の変更を受理しました。"
        else:
            m = f"Error! A{num}はまだ存在しません"
        await ctx.channel.send(m)

    """なんか動かない
    @commands.group(description='''質問や解答の履歴をBOTから削除し、listコマンド等で参照できないようにします。このコマンドによって削除された質問や解答は、チャンネルの履歴には残ります。全削除は!delallで実行して下さい。
*使用方法*
!delete q (質問番号) : 指定した質問番号に対応する質問の履歴を削除します。
!delete a (解答番号) : 指定した解答番号に対応する解答の履歴を削除します。''',brief="質問や解答の履歴をBOTから削除します。",aliases=['del'])
    async def delete(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Error! 引数が指定されていません。!help deleteで使用方法を確認して下さい。")

    @delete.command(aliases=['q'])
    async def question(self, num:int):
        print(num)
        if len(self.q_list)>=num:
            m = self.q_list[num-1]+" を削除しました。"
            del self.q_list[num-1]
            self.reindex(self.q_list,0)
        else:
            m = "Error! Q"+str(num)+"はまだ存在しません。"
        await ctx.channel.send(m)

    @delete.command(aliases=['a'])
    async def answer(self, num:int):
        print(num)
        if len(self.a_list)>=num:
            m = self.a_list[num-1]+" を削除しました。"
            del self.a_list[num-1]
            self.reindex(self.a_list,1)
        else:
            m = "Error! A"+str(num)+"はまだ存在しません。"
        await ctx.channel.send(m)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('引数が正しく指定されていません。!help deleteで使用方法を確認して下さい。')
    """

    @commands.command(description="""質問や解答の履歴をBOTから削除し、listコマンド等で参照できないようにします。このコマンドによって削除された質問や解答は、チャンネルの履歴には残ります。
*使用方法*
?delall : BOTに記録された全ての履歴を削除します""",brief="質問や解答の履歴をBOTから全て削除します。")
    async def delall(self, ctx):
        m="Error"
        self.a_key.clear()
        self.q_key.clear()
        self.timelog.clear()
        self.questions.clear()
        self.answers.clear()
        self.reply_q.clear()
        self.reply_a.clear()
        m = "全て削除しました"
        await ctx.channel.send(m)

    # ゲーム開始からのプレイログを出力する
    @commands.command(description="""ゲーム開始からのプレイログを出力します。
現在、発言者名は表示されませんが、今後の改良で表示するように変更していきます。""",brief="ゲーム開始からのプレイログを出力します", aliases=['log'])
    async def playlog(self, ctx):
        msg = self.showlog()
        await ctx.channel.send(msg)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # 行頭の空白除外処理
        message.content.lstrip(" ")
        message.content.lstrip("　")
        if message.content.startswith("!"):
            message.content.rstrip(" ")
            message.content.rstrip("　")

        # 質問への処理
        if message.content.startswith("「"):
            m = message.content[1:-1]
            self.add_to_dic(m, 1)
            k = self.q_key[-1]
            m = template(k, self.questions[k], self.reply_q[f"{k}r"])
            print("{}: {}".format(k, self.questions[k]))
            await message.channel.send(m)

        # 解答への処理
        if message.content.startswith("『"):
            m = message.content[1:-1]
            self.add_to_dic(m, 0)
            k = self.a_key[-1]
            print(k)
            print(self.answers[k])
            m = template(k, self.answers[k], self.reply_a[f"{k}r"])
            await message.channel.send(m)

        if message.content.startswith("Q") or message.content.startswith("q") or message.content.startswith("ｑ") or message.content.startswith("Ｑ"):
            num = int(re.sub(r"\D","",message.content))
            if len(self.q_key) > (num-1) :
                self.respond(num, message.content, 1)
                k = self.q_key[num-1]
                m = template(k, self.questions[k], self.reply_q[f"{k}r"])
            else:
                m = "Error! 数値に対応する質問がまだ存在しません"
            await message.channel.send(m)

        if message.content.startswith("A") or message.content.startswith("a") or message.content.startswith("ａ") or message.content.startswith("Ａ"):
            num = int(re.sub(r"\D","",message.content))
            if len(self.a_key) > (num-1) :
                self.respond(num, message.content, 0)
                k = self.a_key[num-1]
                m = template(k, self.answers[k], self.reply_a[f"{k}r"])
            else:
                m = "Error! 数値に対応する質問がまだ存在しません"
            await message.channel.send(m)

        #await self.bot.process_commands(message)
        
        
    def showlog(self)-> str:
        q_start = ""
        a_start = ""
        line = ""
        q_log = ""
        a_log = ""
        msg = ""
        if len(self.q_key) == 0 :
            q_start = "【質問がありません】"
        else:
            q_start = "【質問ログ】"
            for i in range(len(self.q_key)):
                kr = self.q_key[i]+'r'
                print(kr)
                line = f"{self.q_key[i]}: {self.questions[self.q_key[i]]} ({self.timelog[self.q_key[i]]})\n"
                rep = "{} ({})\n".format((" "*4)+"<- "+self.reply_q[kr], self.timelog[kr]) \
                if self.reply_q[kr] else \
                "{}\n".format((" "*4)+"<- No reply")
                q_log = q_log + line + rep
        if len(self.a_key) == 0 :
            a_start = "【解答がありません】"
        else:
            a_start = "【解答ログ】"
            for i in range(len(self.a_key)):
                kr = self.a_key[i]+'r'
                print(kr)
                line = f"{self.a_key[i]}: {self.answers[self.a_key[i]]} ({self.timelog[self.a_key[i]]})\n"
                rep = "{} ({})\n".format((" "*4)+"<- "+self.reply_a[kr], self.timelog[kr]) \
                if self.reply_a[kr] else \
                "{}\n".format((" "*4)+"<- No reply")
                a_log = a_log + line + rep
        msg = "====={0}=====\n{1}\n{2}{5}\n{3}\n{4}{5}".format(self.start_time+" 開始", q_start, q_log, a_start, a_log,"-"*20)
        return msg


# BOT本体からコグを読み込む際に呼び出される関数
def setup(bot):
    bot.add_cog(General(bot))

# 定型文生成関数
def template(s1:str, s2:str, s3:str) -> str:
    return f"{s1}: {s2}" if not s3 else f"{s1}: {s2} : {s3}"

# 現在の日本時間取得
def jst_now()->str:
    JST = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(JST).strftime("%Y/%m/%d %H:%M")
