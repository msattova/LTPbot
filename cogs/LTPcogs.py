from discord.ext import commands
import discord
import re
import random
from datetime import datetime, timedelta, timezone
import codecs


#コグとして用いるクラスを定義
class LTPcog(commands.Cog):

    # 正規表現オブジェクト(インスタンスごとに独立させる必要がないのでクラス変数扱いにする)
    reg_q = re.compile(r'^「(.*)」$')
    reg_a = re.compile(r'^『(.*)』$')
    reg_reply = re.compile(r'^\D(\d+)\s.*$')

    #コンストラクタ
    def __init__(self, bot):
        self.bot = bot
        # Q1, A1などをキーとする質問・解答辞書(変数名は手掛かり=clueより)
        self.clue = {}
        # playlog用発言記録ディクショナリ
        # authors仕様
        # キー：質問や解答に割り当てられた英数字(Q1やA1など)。
        # 値：質問や解答を行った人の名前
        self.authors = {}
        # playlog用時刻記録ディクショナリ
        # timelog仕様
        # キー：質問や解答に割り当てられた英数字(Q1やA1など)。応答に対しては、英数字末尾に'r'を追加する。
        # 値：質問や解答、応答がなされた時刻
        self.timelog = {}
        # Q1rやA1rなどをキーとする応答辞書
        self.reply = {}
        # questionsやanswersへのキーのリスト(順番を保持しなくてはならないのでリスト型)
        self.q_key = []
        self.a_key = []
        # ウミガメのスープの開始時間
        self.start_time = jst_now()

    #質問・解答追加処理関数(qoraが1なら質問、0なら解答と認識)
    def add_to_dict(self, qora:bool, ctx, key, has_matched):
        if has_matched is not None :
            qa = "Q" if qora else "A"
            num = len(key)+1
            key.append(f"{qa}{num}")
            self.clue[key[-1]] = has_matched.group(1)
            self.reply[f"{key[-1]}r"] = ""
            self.authors[key[-1]] = ctx.author.display_name
            self.timelog[key[-1]] = jst_now()
            k = key[-1]
            print(f"{k}: {self.clue[k]}")
            return template(k, self.clue[k], self.reply[f"{k}r"])
        else:
            return None

    #質問や解答への返答処理関数(こちらも質問は1,解答は0）
    def respond(self, num:int, s:str, qora:bool):
        s = s.split()
        k = self.q_key[num-1] if qora else self.a_key[num-1]
        self.reply[f"{k}r"] = s[1]
        self.timelog[f"{k}r"] = jst_now()


    # 履歴表示用関数
    def show_list(self, ctx, key, n, tmp:str) -> str:
        m = ""
        line = ""
        #表示件数の指定。指定なしなら、全部。指定がある場合はその分だけ。0が指定された場合も全部。
        num = (len(key) if len(n)==0 else
               n[0] if is_num(str(n[0]))==False else
               int(n[0]) if int(n[0])!=0 else
               len(key))
        print(num)
        print(is_num(str(num)))
        # 引数が数字かどうか
        if is_num(str(num))==True:
            if len(key) == 0 :
                m= f"{ctx.author.mention} まだ{tmp}がされていません"
            elif abs(num) > len(key):
                m= f"{ctx.author.mention} Error! 指定された数字が{tmp}数よりも多いです"
            else:
                #正数の場合は古い方からn個を、負数の場合は新しい方からn個を表示
                if num>0:
                    for i in range(num):
                        line = template(key[i], self.clue[key[i]], self.reply[f"{key[i]}r"])
                        m = f'{m}{line}\n'
                else:
                    for i in reversed(range(num*(-1))):
                        i = (i+1)*(-1)
                        print(i)
                        line = template(key[i], self.clue[key[i]], self.reply[f"{key[i]}r"])
                        m = f'{m}{line}\n'
        else :
            # rならば応答ありのものを、iならば応答に"!"を含むもののみを、それ以外の場合は応答のないものを表示
            if num == 'r':
                num = len(key)
                for i in range(num):
                    if self.reply[f"{key[i]}r"] != '' :
                        line = template(key[i], self.clue[key[i]], self.reply[f"{key[i]}r"])
                        m = f'{m}{line}\n'
            elif num == 'i':
                num = len(key)
                for i in range(num):
                    if '!' in self.reply[f"{key[i]}r"] or '！' in self.reply[f"{key[i]}r"]:
                        line = template(key[i], self.clue[key[i]], self.reply[f"{key[i]}r"])
                        m = f'{m}{line}\n'
            else:
                num = len(key)
                for i in range(num):
                    if self.reply[f"{key[i]}r"] == '' :
                        line = template(key[i], self.clue[key[i]], self.reply[f"{key[i]}r"])
                        m = f'{m}{line}\n'
        return m

    def amend(self, ctx, key, num:int, s:str, tmp:str) -> str:
        if len(key) > (num-1) :
            k = key[num-1]
            print(k)
            if self.authors[k] == ctx.author.display_name:
                self.clue[k] = s
                self.reply[f"{k}r"] = ""
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

    def make_lines(self, key, m_append):
        for i in range(len(key)) :
            kr = f'{key[i]}r'
            print(kr)
            line = f"{key[i]}: {self.clue[key[i]]} ({self.timelog[key[i]]}) by {self.authors[key[i]]}\n"
            rep = (f"    <- {self.reply[kr]} ({self.timelog[kr]})\n"
                   if self.reply[kr] else
                   "    <- No reply\n")
            m_append(f"{line}{rep}")

    def showlog(self)-> list:
        q_start = ""
        a_start = ""
        line = ""
        q_log = ""
        a_log = ""
        msg = []
        border = "-"*16
        container = ""
        m_append = msg.append
        m_append(f"===={self.start_time} 開始====")
        if len(self.q_key) == 0 :
            q_start = "【質問がありません】"
            m_append(q_start)
        else:
            q_start = "【質問ログ】"
            m_append(q_start)
            self.make_lines(self.q_key, m_append)
        m_append(border)
        if len(self.a_key) == 0 :
            a_start = "【解答がありません】"
            m_append(a_start)
        else:
            a_start = "【解答ログ】"
            m_append(a_start)
            self.make_lines(self.a_key, m_append)
        m_append(border)
        return msg


    @commands.command(description="これまでに出た質問(「」で囲まれた言葉)の履歴を表示します。数字で表示件数を指定することも可能です。負数による指定も可能です。\n`?list 20`：最初の20件を表示\n`?list -20`：最後の20件を表示\n未応答の解答のみを表示することも可能です。\n`?list nr`",brief="これまでに出た質問の履歴を表示します。数字で表示件数を指定することもできます。")
    async def list(self, history, *n):
        m = self.show_list(history, self.q_key, n, '質問')
        print(m)
        await history.channel.send(m)

    @commands.command(description="""これまでに出た解答(『』で囲まれた言葉)の履歴を表示します。数字で表示件数を指定することも可能です。負数による指定も可能です。\n`?list 20`：最初の20件を表示\n`?list -20`：最後の20件を表示\n未応答の解答のみを表示することも可能です。\n`?list nr`""",brief="これまでに出た解答の履歴を表示します。数字で表示件数を指定することもできます。")
    async def lista(self, history, *n):
        m = self.show_list(history, self.a_key, n, '解答')
        print(m)
        await history.channel.send(m)

    @commands.command(description="""質問を修正します。
*使用方法*
?req したい質問番号) (質問の修正)""",brief="質問の修正ができます。")
    async def req(self, ctx, num:int, s:str):
        m = self.amend(ctx, self.q_key, num, s, '質問')
        await ctx.channel.send(m)

    @req.error
    async def req_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
                await ctx.channel.send(f'{ctx.author.mention} 引数が正しく指定されていません。!help reqで使用方法を確認して下さい。')

    @commands.command(description="""解答を修正します。
*使用方法*
?rea (修正したい解答番号) (解答の修正)""",brief="解答の修正ができます。")
    async def rea(self, ctx, num:int, s:str):
        m = self.amend(ctx, self.a_key, num, s, '解答')
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
        self.clue.clear()
        self.reply.clear()
        m = "全て削除しました"
        await ctx.channel.send(m)

    # ゲーム開始からのプレイログを出力する
    @commands.command(description="""ゲーム開始からのプレイログを出力します。
現在、発言者名は表示されませんが、今後の改良で表示するように変更していきます。""",brief="ゲーム開始からのプレイログを出力します", aliases=['log'])
    async def playlog(self, ctx):
        msg = self.showlog()
        for i in msg:
            await ctx.channel.send(i)

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
            has_matched = LTPcog.reg_q.search(message.content)
            m = self.add_to_dict(1, message, self.q_key, has_matched)
            if m is not None:
                await message.channel.send(m)

        # 解答への処理（正規表現を利用することにした）
        if message.content.startswith("『"):
            has_matched = LTPcog.reg_a.search(message.content)
            m = self.add_to_dict(0, message, self.a_key, has_matched)
            if m is not None:
                await message.channel.send(m)

        if message.content.startswith("Q") or message.content.startswith("q") or message.content.startswith("ｑ") or message.content.startswith("Ｑ"):
            has_matched = LTPcog.reg_reply.search(message.content)
            if has_matched is not None :
                num = int(has_matched.group(1))
                if len(self.q_key) > (num-1) :
                    self.respond(num, message.content, 1)
                    k = self.q_key[num-1]
                    m = template(k, self.clue[k], self.reply[f"{k}r"])
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
                    m = template(k, self.clue[k], self.reply[f"{k}r"])
                else:
                    m = f"{message.author.mention} Error! 解答(A{num})はまだ存在しません"
                await message.channel.send(m)

        #await self.bot.process_commands(message)

# 定型文生成関数
def template(s1:str, s2:str, s3:str) -> str:
    return f"{s1}: {s2}" if s3 == "" else f"{s1}: {s2} : {s3}"

# 現在の日本時間取得
def jst_now()->str:
    JST = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(JST).strftime("%Y/%m/%d %H:%M")

# 文字列が数字かどうか判定
def is_num(s:str) :
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


