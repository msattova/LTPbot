from discord.ext import commands
import discord
import re
import random
from datetime import datetime, timedelta, timezone
import codecs



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

    # 履歴表示用関数
    def show_list(self, ctx, key, mentions, reply, n, tmp:str) -> str:
        m = ""
        line = ""
        #表示件数の指定。指定なしなら、全部。指定がある場合はその分だけ。0が指定された場合も全部。
        num = len(key) if len(n)==0 else n[0] if self.is_num(str(n[0]))==False else int(n[0]) if int(n[0])!=0 else len(key)
        print(num)
        print(self.is_num(str(num)))
        # 引数が数字かどうか
        if self.is_num(str(num))==True:
            if len(key) == 0 :
                m= f"{ctx.author.mention} まだ{tmp}がされていません"
            elif abs(num) > len(key):
                m= f"{ctx.author.mention} Error! 指定された数字が{tmp}数よりも多いです"
            else:
                #正数の場合は古い方からn個を、負数の場合は新しい方からn個を表示
                if num>0:
                    for i in range(num):
                        line = template(key[i], mentions[key[i]], reply[key[i]+'r'])
                        m = f'{m}{line}\n'
                else:
                    for i in reversed(range(num*(-1))):
                        i = (i+1)*(-1)
                        print(i)
                        line = template(key[i], mentions[key[i]], reply[key[i]+'r'])
                        m = f'{m}{line}\n'
        else :
            # rならば応答ありのものを、iならば応答に"!"を含むもののみを、それ以外の場合は応答のないものを表示
            if num == 'r':
                num = len(key)
                for i in range(num):
                    if reply[key[i]+'r'] != '' :
                        line = template(key[i], mentions[key[i]], reply[key[i]+'r'])
                        m = f'{m}{line}\n'
            elif num == 'i':
                num = len(key)
                for i in range(num):
                    if '!' in reply[key[i]+'r'] or '！' in reply[key[i]+'r']:
                        line = template(key[i], mentions[key[i]], reply[key[i]+'r'])
                        m = f'{m}{line}\n'
            else:
                num = len(key)
                for i in range(num):
                    if reply[key[i]+'r'] == '' :
                        line = template(key[i], mentions[key[i]], reply[key[i]+'r'])
                        m = f'{m}{line}\n'
        return m

    def amend(self, ctx, key, mentions, reply, num:int, s:str, tmp:str) -> str:
        if len(key) > (num-1) :
            k = key[num-1]
            print(k)
            if self.authors[k] == ctx.author.display_name:
                mentions[k] = s
                reply[f"{k}r"] = ""
                self.timelog[k] = jst_now()
                self.timelog[f"{k}r"] = ""
                qa = 'Q' if tmp=='質問' else 'A'
                m = f"{ctx.author.mention} {qa}{num}の変更を受理しました。"
            else:
                m = f"{ctx.author.mention} 不正ユーザーです。{tmp}の訂正はその質問をした本人にのみ許されています。"
        else:
            m = f"{ctx.author.mention} Error! {qa}{num}はまだ存在しません"
            print(m)
        return m

    def showlog(self)-> list:
        q_start = ""
        a_start = ""
        line = ""
        q_log = ""
        a_log = ""
        msg = []
        border = "-"*16
        container = ""
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
        return msg

    @commands.command(description="これまでに出た質問(「」で囲まれた言葉)の履歴を表示します。数字で表示件数を指定することも可能です。負数による指定も可能です。\n`?list 20`：最初の20件を表示\n`?list -20`：最後の20件を表示\n未応答の解答のみを表示することも可能です。\n`?list nr`",brief="これまでに出た質問の履歴を表示します。数字で表示件数を指定することもできます。")
    async def list(self, history, *n):
        m = self.show_list(history, self.q_key, self.questions, self.reply_q, n, '質問')
        print(m)
        await history.channel.send(m)

    @commands.command(description="""これまでに出た解答(『』で囲まれた言葉)の履歴を表示します。数字で表示件数を指定することも可能です。負数による指定も可能です。\n`?list 20`：最初の20件を表示\n`?list -20`：最後の20件を表示\n未応答の解答のみを表示することも可能です。\n`?list nr`""",brief="これまでに出た解答の履歴を表示します。数字で表示件数を指定することもできます。")
    async def lista(self, history, *n):
        m = self.show_list(history, self.a_key, self.answers, self.reply_a, n, '解答')
        print(m)
        await history.channel.send(m)

    @commands.command(description="""質問を修正します。
*使用方法*
?req (修正したい質問番号) (質問の修正)""",brief="質問の修正ができます。")
    async def req(self, ctx, num:int, s:str):
        m = self.amend(ctx, self.q_key, self.questions, self.reply_q, num, s, '質問')
        await ctx.channel.send(m)

    @req.error
    async def req_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
                await ctx.channel.send(f'{ctx.author.mention} 引数が正しく指定されていません。!help reqで使用方法を確認して下さい。')

    @commands.command(description="""解答を修正します。
*使用方法*
?rea (修正したい解答番号) (解答の修正)""",brief="解答の修正ができます。")
    async def rea(self, ctx, num:int, s:str):
        m = self.amend(ctx, self.a_key, self.answers, self.reply_a, num, s, '解答')
        await ctx.channel.send(m)

    @rea.error
    async def rea_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
                await ctx.channel.send(f'{ctx.author.mention} 引数が正しく指定されていません。!help reaで使用方法を確認して下さい。')


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

# 定型文生成関数
def template(s1:str, s2:str, s3:str) -> str:
    return f"{s1}: {s2}" if not s3 else f"{s1}: {s2} : {s3}"

# 現在の日本時間取得
def jst_now()->str:
    JST = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(JST).strftime("%Y/%m/%d %H:%M")

