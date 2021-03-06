from discord.ext import commands

from . import LTPlib as ltp


# コグとして用いるクラスを定義
class LTPcog(commands.Cog):

    # コンストラクタ
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
        self.start_time = ltp.jst_now()

    # 質問・解答追加処理関数(qoraが1なら質問、0なら解答と認識)
    def add_to_dict(self, ctx, key: dict, matched_str: str):
        # matched_str = has_matched.group(1)
        # 空白しかないもの、「」だけのものを除外するため
        if set((i for i in matched_str if i != " " and i != "　")):
            qa = "Q" if key is self.q_key else "A"
            key_str = f"{qa}{len(key)+1}"
            key.append(key_str)
            k = key[-1]
            self.clue[k] = matched_str
            self.reply[f"{k}r"] = ""
            self.authors[k] = ctx.author.display_name
            self.timelog[k] = ltp.jst_now()
            print(f"{k}: {self.clue[k]}")
            return ltp.template(k, self.clue[k], self.reply[f"{k}r"])
        else:
            return None

    # 質問や解答への返答処理関数(こちらも質問は1,解答は0）
    def respond(self, ctx, num: int, key: dict) -> str:
        if len(key) > (num-1) and self.clue[key[num-1]]:
            k = key[num-1]
            s = ctx.content.split(None, 1)
            self.reply[f"{k}r"] = s[1]
            self.timelog[f"{k}r"] = ltp.jst_now()
            m = ltp.template(k, self.clue[k], self.reply[f"{k}r"])
        else:
            t = f"質問(Q{num})" if key is self.q_key else f"解答(A{num})"
            m = f"{ctx.author.mention} Error! {t}はまだ存在しません"
        return m

    def make_message(self, msg, app):
        str_ = ""
        for i in msg:
            str_ = f"{str_}{i}"
            if len(str_) > 1500:
                app(str_)
                str_ = ""
        if str_:
            app(str_)

    # 履歴表示用関数
    def show_list(self, ctx, key: dict, n, tmp: str) -> list:
        m = ""
        line = ""
        # 表示件数の指定。指定なしなら、全部。指定がある場合はその分だけ。0が指定された場合も全部。
        num = (len(key) if len(n) == 0 else
               n[0] if not ltp.is_num(str(n[0])) else
               int(n[0]) if int(n[0]) != 0 else
               len(key))
        print(num)
        print(ltp.is_num(str(num)))
        # 引数が数字かどうか
        if ltp.is_num(str(num)):
            if not key:
                m = f"{ctx.author.mention} まだ{tmp}がされていません"
            elif abs(num) > len(key):
                m = f"{ctx.author.mention} Error! 指定された数字が{tmp}数よりも多いです"
            else:
                # 正数の場合は古い方からn個を、負数の場合は新しい方からn個を表示
                lst = range(num) if num > 0 else reversed(range(num*(-1)))
                for i in lst:
                    if not self.clue[key[i]]:
                        continue
                    i = i if num > 0 else (i+1)*(-1)
                    print(i)
                    line = ltp.template(key[i],
                                        self.clue[key[i]],
                                        self.reply[f"{key[i]}r"])
                    m = f'{m}{line}\n'
        else:
            # rならば応答ありのものを、iならば応答に"!"を含むもののみを、それ以外の場合は応答のないものを表示
            if num == 'i':
                key = [i for i in key
                       if '!' in self.reply[f"{i}r"] or
                       '！' in self.reply[f"{i}r"]]
            elif num == 'r':
                key = [i for i in key if self.reply[f"{i}r"]]
            # 試験的に導入。質問への応答が肯定か否定かで分ける。
            elif num == 'y':
                key = [i for i in key
                       if 'y' in self.reply[f"{i}r"].lower() or
                       'はい' in self.reply[f"{i}r"] or
                       'うです' in self.reply[f"{i}r"]]
            elif num == 'n':
                key = [i for i in key
                       if 'n' in self.reply[f"{i}r"].lower() or
                       'いいえ' in self.reply[f"{i}r"] or
                       'います' in self.reply[f"{i}r"]]
            elif num == '.':
                key = [i for i in key if not self.reply[f"{i}r"]]
            print(key)
            print(set(key))
            if key:
                for k in key:
                    if not self.clue[k]:
                        continue
                    line = ltp.template(k, self.clue[k], self.reply[f"{k}r"])
                    m = f'{m}{line}\n'
            else:
                m = f"{ctx.author.mention} What you want is Nothing."
        lst = []
        self.make_message(m, lst.append)
        return lst

    def amend(self, ctx, key, num: int, s: str) -> str:
        (tmp, qa) = (("質問", f"Q{num}")
                     if key is self.q_key else
                     ("解答", f"A{num}"))
        lst = [i for i in key if self.clue[key]]
        print(lst)
        if len(lst) > (num-1):
            k = key[num-1]
            print(k)
            if self.authors[k] == ctx.author.display_name:
                self.clue[k] = s
                self.reply[f"{k}r"] = ""
                self.timelog[k] = ltp.jst_now()
                self.timelog[f"{k}r"] = ""
                m = f"{ctx.author.mention} {qa}の変更を受理しました。"
            else:
                m = (f"{ctx.author.mention} 不正ユーザーです。"
                     f"{tmp}の訂正はその{tmp}をした本人にのみ許されています。")
        else:
            m = f"{ctx.author.mention} Error! {qa}{num}はまだ存在しません"
        print(m)
        return m

    def make_lines(self, key, m_append):
        print(key)
        key_gen = (k for k in key if self.clue[k])
        for k in key_gen:
            kr = f'{k}r'
            print(kr)
            line = (f"{k}: {self.clue[k]} ({self.timelog[k]}) "
                    f"by {self.authors[k]}\n")
            rep = (f"    <- {self.reply[kr]} ({self.timelog[kr]})\n"
                   if self.reply[kr] else
                   "    <- No reply\n")
            m_append(f"{line}{rep}")

    def showlog(self) -> list:
        msg = []
        border = "----------------\n"
        m_append = msg.append
        m_append(f"===={self.start_time} 開始====\n")
        if not self.q_key:
            m_append(f"【質問がありません】\n")
        else:
            m_append(f"【質問ログ】\n")
            self.make_lines(self.q_key, m_append)
        m_append(f"{border}")
        if not self.a_key:
            m_append(f"【解答がありません】\n")
        else:
            m_append(f"【解答ログ】\n")
            self.make_lines(self.a_key, m_append)
        m_append(f"{border}")
        lst = []
        l_append = lst.append
        self.make_message(msg, l_append)
        print(lst)
        return lst

    def what_delete(self, ctx, key: dict, num: int) -> str:
        (tmp, qa) = (("質問", f"Q{num}")
                     if key is self.q_key else
                     ("解答", f"A{num}"))
        if self.authors[qa] == ctx.author.display_name:
            if qa in key:
                # 中身が空なら無視する、というように出力形関数を仕様変更
                self.clue[qa] = ""
                print({k: v for k, v in self.clue.items()})
                return f"{qa}を削除しました"
            else:
                return f"{qa}は存在しません"
        else:
            return f"不正ユーザです。{tmp}の削除はその{tmp}をした本人にのみ許されています。"

    @commands.command(description="これまでに出た質問(「」で囲まれた言葉)の履歴を表示します。"
                      "数字で表示件数を指定することも可能です。負数による指定も可能です。\n"
                      "`?list 20`：最初の20件を表示\n"
                      "`?list -20`：最後の20件を表示\n"
                      "未応答の解答のみを表示することも可能です。\n"
                      "`?list .`"
                      "**試験導入**"
                      "`?list y` : 応答が肯定のもののみを出力します"
                      "`?list n` : 応答が否定のもののみを出力します",
                      brief="これまでに出た質問の履歴を表示します。"
                      "数字で表示件数を指定することもできます。")
    async def list(self, history, *n):
        lst = self.show_list(history, self.q_key, n, '質問')
        print(lst)
        snd = []
        snd_append = snd.append
        for i in lst:
            sended = await history.channel.send(i)
            snd_append(sended)
        for i in snd:
            await i.delete(delay=ltp.DELAY_SECONDS_LONGER)

    @commands.command(description="これまでに出た解答(『』で囲まれた言葉)の履歴を表示します。"
                      "詳細は?help list を参照してください。",
                      brief="これまでに出た解答の履歴を表示します。"
                      "数字で表示件数を指定することもできます。")
    async def lista(self, history, *n):
        lst = self.show_list(history, self.a_key, n, '解答')
        print(lst)
        snd = []
        snd_append = snd.append
        for i in lst:
            sended = await history.channel.send(i)
            snd_append(sended)
        for i in snd:
            await i.delete(delay=ltp.DELAY_SECONDS_LONGER)

    @commands.command(description="質問を修正します。\n"
                      "*使用方法*\n"
                      "?req したい質問番号) (質問の修正)",
                      brief="質問の修正ができます。")
    async def req(self, ctx, num: int, s: str):
        m = self.amend(ctx, self.q_key, num, s)
        print(m)
        sended = await ctx.channel.send(m)
        await sended.delete(delay=ltp.DELAY_SECONDS)

    @req.error
    async def req_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            sended = await ctx.channel.send(
                f'{ctx.author.mention} 引数が正しく指定されていません。'
                '!help reqで使用方法を確認して下さい。')
            await sended.delete(delay=DELAY_SECONDS)

    @commands.command(description="解答を修正します。"
                      "*使用方法*"
                      "?rea (修正したい解答番号) (解答の修正)",
                      brief="解答の修正ができます。")
    async def rea(self, ctx, num: int, s: str):
        m = self.amend(ctx, self.a_key, num, s)
        print(m)
        sended = await ctx.channel.send(m)
        await sended.delete(delay=ltp.DELAY_SECONDS)

    @rea.error
    async def rea_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            sended = await ctx.channel.send(
                f'{ctx.author.mention} 引数が正しく指定されていません。'
                '!help reaで使用方法を確認して下さい。')
            await sended.delete(delay=ltp.DELAY_SECONDS)

    @commands.group(aliases=['del'])
    async def delete(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @delete.command()
    async def q(self, ctx, num: int):
        m = self.what_delete(ctx, self.q_key, num)
        sended = await ctx.channel.send(f"{ctx.author.mention} {m}")
        await sended.delete(delay=ltp.DELAY_SECONDS)

    @delete.command()
    async def a(self, ctx, num: int):
        m = self.what_delete(ctx, self.a_key, num)
        sended = await ctx.channel.send(f"{ctx.author.mention} {m}")
        await sended.delete(delay=ltp.DELAY_SECONDS)

    @commands.command(
        description="質問や解答の履歴をBOTから削除し、listコマンド等で参照できないようにします。"
        "このコマンドによって削除された質問や解答は、チャンネルの履歴には残ります。",
        brief="質問や解答の履歴をBOTから全て削除します。")
    async def delall(self, ctx):
        m = "Error"
        self.a_key.clear()
        self.q_key.clear()
        self.timelog.clear()
        self.clue.clear()
        self.reply.clear()
        m = "全て削除しました"
        sended = await ctx.channel.send(m)
        await sended.delete(delay=ltp.DELAY_SECONDS)

    # ゲーム開始からのプレイログを出力する
    @commands.command(description="ゲーム開始からのプレイログを出力します。",
                      brief="ゲーム開始からのプレイログを出力します",
                      aliases=['log'])
    async def playlog(self, ctx):
        msg = self.showlog()
        for i in msg:
            await ctx.channel.send(i)

    @commands.command()
    async def restart(self, ctx):
        self.start_time = ltp.jst_now()
        sended = await ctx.channel.send("ウミガメのスープを再開します")
        await sended.delete(delay=ltp.DELAY_SECONDS)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # 質問への処理（正規表現を利用することにした）
        if (message.content.startswith("「") or
                message.content.startswith("｢")):
            has_matched = ltp.reg_q.search(message.content)
            if has_matched is not None:
                m = self.add_to_dict(message, self.q_key, has_matched.group(1))
                if m is not None:
                    sended = await message.channel.send(m)
                    await sended.delete(delay=ltp.DELAY_SECONDS)

        # 解答への処理（正規表現を利用することにした）
        if (message.content.startswith("『") or
                message.content.startswith("『")):
            has_matched = ltp.reg_a.search(message.content)
            if has_matched is not None:
                m = self.add_to_dict(message, self.a_key, has_matched.group(1))
                if m is not None:
                    sended = await message.channel.send(m)
                    await sended.delete(delay=ltp.DELAY_SECONDS)

        if (message.content.startswith("Q") or
                message.content.startswith("q") or
                message.content.startswith("ｑ") or
                message.content.startswith("Ｑ")):
            has_matched = ltp.reg_reply.search(message.content)
            if has_matched is not None:
                num = int(has_matched.group(1))
                m = self.respond(message, num, self.q_key)
                sended = await message.channel.send(m)
                await sended.delete(delay=ltp.DELAY_SECONDS)

        if (message.content.startswith("A") or
                message.content.startswith("a") or
                message.content.startswith("ａ") or
                message.content.startswith("Ａ")):
            has_matched = ltp.reg_reply.search(message.content)
            if has_matched is not None:
                num = int(has_matched.group(1))
                m = self.respond(message, num, self.a_key)
                sended = await message.channel.send(m)
                await sended.delete(delay=ltp.DELAY_SECONDS)

        # await self.bot.process_commands(message)
