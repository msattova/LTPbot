from discord.ext import commands
import discord
import re
import random
from datetime import datetime, timedelta, timezone
import codecs

# はじめに呼び出されるコグ
class General(commands.Cog):
    # ウミガメのスープ開始状態か否かの判断変数(:bool)
    has_started = 0

    #コンストラクタ
    def __init__(self, bot):
        self.bot = bot
        self.has_started = 0
        # 以下、デバッグ用設定
        # self.bot.add_cog(LTPcog(self.bot))

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
            self.bot.add_cog(LTPcog(self.bot))
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

#コグとして用いるクラスを定義
class LTPcog(commands.Cog):
    # Q1などをキーとする質問辞書
    questions = {}
    # A1などをキーとする解答辞書
    answers = {}
    # playlog用発言記録ディクショナリ
    # authors仕様
    # キー：質問や解答に割り当てられた英数字(Q1やA1など)。
    # 値：質問や解答を行った人の名前
    authors = {}
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

    # 正規表現オブジェクト
    reg_q = re.compile(r'^「(.*)」$')
    reg_a = re.compile(r'^『(.*)』$')
    reg_reply = re.compile(r'^\D(\d+)\s.*$')

    #コンストラクタ
    def __init__(self, bot):
        self.bot = bot
        self.questions = {}
        self.answers = {}
        self.timelog = {}
        self.authors = {}
        self.reply_q = {}
        self.reply_a = {}
        self.q_key = []
        self.a_key = []
        self.start_time = jst_now()
        self.reg_q = re.compile(r'^「(.*)」$')
        self.reg_a = re.compile(r'^『(.*)』$')
        self.reg_reply = re.compile(r'^\D(\d+)\s.*$')

    #質問・解答追加処理関数(qoraが1なら質問、0なら解答と認識)
    def add_to_dic(self, msg:str, qora:bool, ctx):
        if qora:
            qa = "Q"
            num = len(self.q_key)+1
            self.q_key.append(f"{qa}{num}")
            self.questions[self.q_key[num-1]] = msg
            self.reply_q[f"{self.q_key[num-1]}r"] = ""
            self.authors[self.q_key[num-1]] = ctx.author.display_name
            self.timelog[self.q_key[num-1]] = jst_now()
            self.timelog[f"{self.q_key[num-1]}r"] = ""
        else:
            qa = "A"
            num = len(self.a_key)+1
            self.a_key.append(f"{qa}{num}")
            self.answers[self.a_key[num-1]] = msg
            self.reply_a[f"{self.a_key[num-1]}r"] = ""
            self.authors[self.a_key[num-1]] = ctx.author.display_name
            self.timelog[self.a_key[num-1]] = jst_now()
            self.timelog[f"{self.a_key[num-1]}r"] = ""


    #質問や解答への返答処理関数(こちらも質問は1,解答は0）
    def respond(self, num:int, s:str, qora:bool):
        s = s.split()
        if qora :
            k = self.q_key[num-1]
            self.reply_q[f"{k}r"] = s[1]
            self.timelog[f"{k}r"] = jst_now()
        else :
            k = self.a_key[num-1]
            self.reply_a[f"{k}r"] = s[1]
            self.timelog[f"{k}r"] = jst_now()

    # 文字列が数字かどうか判定
    def is_num(self, s:str) :
        try:
            float(s)
        except ValueError:
            return False
        else:
            return True

    #番号振り直し関数
    #timelogをどうするか考える（現状では番号を振りなおすとプレイログが出力できない）
    def reindex(self, key:list, dic:dict, rep:dict, qora:bool):
        num = len(key)
        # tmp = keyではtmpとkeyは同じデータを参照してしまう
        tmp = key.copy()
        qa = "Q" if qora else "A"
        tmp_dic = dic.copy()
        tmp_rep = rep.copy()
        tmp_log = timelog.copy()
        dic.clear()
        rep.clear()
        timelog.clear()
        for i in range(num):
            print(f"{key[i]} to {qa}{i+1}")
            key[i] = f"{qa}{i+1}"
        for i in range(num):
            print(f"key = {key[i]}")
            print(f"tmp_dic = {tmp_dic[tmp[i]]}")
            dic[key[i]] = tmp_dic[tmp[i]]
            rep[key[i]+'r'] = tmp_rep[tmp[i]+'r']


    @commands.command(description="""これまでに出た質問(「」で囲まれた言葉)の履歴を表示します。数字で表示件数を指定することも可能です。負数による指定も可能です。\n`?list 20`：最初の20件を表示\n`?list -20`：最後の20件を表示\n未応答の解答のみを表示することも可能です。\n`?list nr`""",brief="これまでに出た質問の履歴を表示します。数字で表示件数を指定することもできます。")
    async def list(self, history, *n):
        m = ""
        line = ""
        #表示件数の指定。指定なしなら、全部。指定がある場合はその分だけ。0が指定された場合も全部。
        num = len(self.q_key) if len(n)==0 else n[0] if self.is_num(str(n[0]))==False else int(n[0]) if int(n[0])!=0 else len(self.q_key)
        print(num)
        print(self.is_num(str(num)))
        if self.is_num(str(num))==True:
            if len(self.q_key) == 0 :
                m="まだ質問がされていません"
            elif abs(num) > len(self.q_key):
                m=f"{history.author.mention} Error! 指定された数字が質問数よりも多いです"
            else:
                #正数の場合は古い方からn個を、負数の場合は新しい方からn個を表示
                if num>0:
                    for i in range(num):
                        line = template(self.q_key[i], self.questions[self.q_key[i]], self.reply_q[self.q_key[i]+'r'])
                        m = f'{m}{line}\n'
                else:
                    for i in reversed(range(num*(-1))):
                        i = (i+1)*(-1)
                        print(i)
                        line = template(self.q_key[i], self.questions[self.q_key[i]], self.reply_q[self.q_key[i]+'r'])
                        m = f'{m}{line}\n'
        # 引数が「応答なしのものを表示する指定」かどうか
        else :
            num = len(self.q_key)
            for i in range(num):
                if self.reply_q[self.q_key[i]+'r'] == '' :
                    line = template(self.q_key[i], self.questions[self.q_key[i]], self.reply_q[self.q_key[i]+'r'])
                    m = f'{m}{line}\n'
        print(m)
        await history.channel.send(m)

    @commands.command(description="""これまでに出た解答(『』で囲まれた言葉)の履歴を表示します。数字で表示件数を指定することも可能です。負数による指定も可能です。\n`?list 20`：最初の20件を表示\n`?list -20`：最後の20件を表示\n未応答の解答のみを表示することも可能です。\n`?list nr`""",brief="これまでに出た解答の履歴を表示します。数字で表示件数を指定することもできます。")
    async def lista(self, history, *n):
        m = ""
        line = ""
        #表示件数の指定。指定なしなら、全部。指定がある場合はその分だけ。0が指定された場合も全部。
        num = len(self.a_key) if len(n)==0 else n[0] if self.is_num(str(n[0]))==False else int(n[0]) if int(n[0])!=0 else len(self.a_key)
        print(num)
        print(self.is_num(str(num)))
        if self.is_num(str(num))==True:
            if len(self.a_key) == 0 :
                m="まだ質問がされていません"
            elif abs(num) > len(self.a_key):
                m=f"{history.author.mention} Error! 指定された数字が質問数よりも多いです"
            else:
                #正数の場合は古い方からn個を、負数の場合は新しい方からn個を表示
                if num>0:
                    for i in range(num):
                        line = template(self.a_key[i], self.answers[self.a_key[i]], self.reply_a[self.a_key[i]+'r'])
                        m = f'{m}{line}\n'
                else:
                    for i in reversed(range(num*(-1))):
                        i = (i+1)*(-1)
                        print(i)
                        line = template(self.a_key[i], self.answers[self.a_key[i]], self.reply_a[self.a_key[i]+'r'])
                        m = f'{m}{line}\n'
        # 引数が「応答なしのものを表示する指定」かどうか
        else :
            num = len(self.a_key)
            for i in range(num):
                if self.reply_a[self.a_key[i]+'r'] == '' :
                    line = template(self.a_key[i], self.answers[self.a_key[i]], self.reply_a[self.a_key[i]+'r'])
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
            self.timelog[k] = jst_now()
            self.timelog[f"{k}r"] = ""
            m = f"{ctx.author.mention} Q{num}の変更を受理しました。"
        else:
            m = f"{ctx.author.mention} Error! Q{num}はまだ存在しません"
        await ctx.channel.send(m)

    @req.error
    async def req_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
                await ctx.channel.send('引数が正しく指定されていません。!help reqで使用方法を確認して下さい。')

    @commands.command(description="""解答を修正します。
*使用方法*
?rea (修正したい解答番号) (解答の修正)""",brief="解答の修正ができます。")
    async def rea(self, ctx,num:int, s:str):
        if len(self.a_key) > (num-1) :
            k = self.a_key[num-1]
            self.answers[k] = s
            self.reply_a[f"{k}r"] = ""
            self.timelog[k] = jst_now()
            self.timelog[f"{k}r"] = ""
            m = f"{ctx.author.mention} A{num}の変更を受理しました。"
        else:
            m = f"{ctx.author.mention} Error! A{num}はまだ存在しません"
        await ctx.channel.send(m)

    @rea.error
    async def rea_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send('引数が正しく指定されていません。!help reaで使用方法を確認して下さい。')


    """
    #なんか動かない
    @commands.group(description='''質問や解答の履歴をBOTから削除し、listコマンド等で参照できないようにします。このコマンドによって削除された質問や解答は、チャンネルの履歴には残ります。全削除は!delallで実行して下さい。
*使用方法*
!delete q (質問番号) : 指定した質問番号に対応する質問の履歴を削除します。
!delete a (解答番号) : 指定した解答番号に対応する解答の履歴を削除します。''',brief="質問や解答の履歴をBOTから削除します。",aliases=['del'])
    async def delete(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Error! 引数が指定されていません。!help deleteで使用方法を確認して下さい。")

    @delete.command(aliases=['q'])
    async def question(self, ctx, num:int):
        print(num)
        if len(self.q_key)>(num-1):
            k = self.q_key.pop(num-1)
            delq = self.questions.pop(k)
            delqr = self.reply_q.pop(f"{k}r")
            del self.timelog[k]
            content = template(k, delq, delqr)
            m = f"“{content}”を削除しました。"
            self.reindex(self.q_key,self.questions,self.reply_q,1)
        else:
            m = "Error! Q"+str(num)+"はまだ存在しません。"
        await ctx.channel.send(m)

    @delete.command(aliases=['a'])
    async def answer(self, ctx, num:int):
        print(num)
        if len(self.a_key)>(num-1):
            k = self.a_key.pop(num-1)
            delq = self.answers.pop(k)
            delqr = self.reply_a.pop(f"{k}r")
            del self.timelog[k]
            content = template(k, dela, delar)
            m = f"“{content}”を削除しました。"
            self.reindex(self.a_key,self.answers,self.reply_a,0)
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
        for i in range(len(msg)):
            await ctx.channel.send(msg[i])


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # 行頭の空白除外処理(なしに)
        #message.content.lstrip(" ")
        #message.content.lstrip("　")
        if message.content.startswith("!"):
            message.content.rstrip(" ")
            message.content.rstrip("　")

        # 質問への処理（正規表現を利用することにした）
        if message.content.startswith("「"):
            has_matched = self.reg_q.search(message.content)
            if has_matched is not None :
                m = has_matched.group(1)
                self.add_to_dic(m, 1, message)
                k = self.q_key[-1]
                m = template(k, self.questions[k], self.reply_q[f"{k}r"])
                print("{}: {}".format(k, self.questions[k]))
                await message.channel.send(m)

        # 解答への処理（正規表現を利用することにした）
        if message.content.startswith("『"):
            has_matched = self.reg_a.search(message.content)
            if has_matched is not None :
                m = has_matched.group(1)
                self.add_to_dic(m, 0, message)
                k = self.a_key[-1]
                m = template(k, self.answers[k], self.reply_a[f"{k}r"])
                print("{}: {}".format(k, self.answers[k]))
                await message.channel.send(m)

        if message.content.startswith("Q") or message.content.startswith("q") or message.content.startswith("ｑ") or message.content.startswith("Ｑ"):
            has_matched = self.reg_reply.search(message.content)
            if has_matched is not None :
                num = int(has_matched.group(1))
                if len(self.q_key) > (num-1) :
                    self.respond(num, message.content, 1)
                    k = self.q_key[num-1]
                    m = template(k, self.questions[k], self.reply_q[f"{k}r"])
                else:
                    m = f"{message.author.mention} Error! 質問(Q{num})はまだ存在しません"
                await message.channel.send(m)

        if message.content.startswith("A") or message.content.startswith("a") or message.content.startswith("ａ") or message.content.startswith("Ａ"):
            has_matched = self.reg_reply.search(message.content)
            if has_matched is not None :
                num = int(has_matched.group(1))
                if len(self.a_key) > (num-1) :
                    self.respond(num, message.content, 0)
                    k = self.a_key[num-1]
                    m = template(k, self.answers[k], self.reply_a[f"{k}r"])
                else:
                    m = f"{message.author.mention} Error! 解答(A{num})はまだ存在しません"
                await message.channel.send(m)

        #await self.bot.process_commands(message)

    def showlog(self)-> list:
        q_start = ""
        a_start = ""
        line = ""
        q_log = ""
        a_log = ""
        msg = []
        border = "-"*16
        msg.append(f"===={self.start_time} 開始====")
        if len(self.q_key) == 0 :
            q_start = "【質問がありません】"
            msg.append(q_start)
        else:
            q_start = "【質問ログ】"
            msg.append(q_start)
            for i in range(len(self.q_key)):
                kr = self.q_key[i]+'r'
                print(kr)
                line = f"{self.q_key[i]}: {self.questions[self.q_key[i]]} ({self.timelog[self.q_key[i]]}) by {self.authors[self.q_key[i]]}\n"
                rep = "{} ({})\n".format((" "*4)+"<- "+self.reply_q[kr], self.timelog[kr]) \
                  if self.reply_q[kr] else \
                  "{}\n".format((" "*4)+"<- No reply")
                msg.append(line + rep)
        msg.append(border)
        if len(self.a_key) == 0 :
            a_start = "【解答がありません】"
            msg.append(a_start)
        else:
            a_start = "【解答ログ】"
            msg.append(a_start)
            for i in range(len(self.a_key)):
                kr = self.a_key[i]+'r'
                print(kr)
                line = f"{self.a_key[i]}: {self.answers[self.a_key[i]]} ({self.timelog[self.a_key[i]]}) by {self.authors[self.a_key[i]]}\n"
                rep = "{} ({})\n".format((" "*4)+"<- "+self.reply_a[kr], self.timelog[kr]) \
                  if self.reply_a[kr] else \
                  "{}\n".format((" "*4)+"<- No reply")
                msg.append(line + rep)
        msg.append(border)
        #msg = "====={0}=====\n{1}\n{2}{5}\n{3}\n{4}{5}".format(self.start_time+" 開始", q_start, q_log, a_start, a_log,"-"*20)
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

