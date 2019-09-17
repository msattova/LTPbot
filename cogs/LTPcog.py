from discord.ext import commands
import discord
import re
import random

#コグとして用いるクラスを定義
class LTPcog(commands.Cog):
    # 質問リスト
    q_list=[]
    # 解答リスト
    a_list=[]
    
    #コンストラクタ
    def __init__(self, bot):
        self.bot = bot
        self.q_list = []
        self.a_list = []

    #質問・解答追加処理関数
    def add_to_list(self, msg,l:list,qora:bool):
        n = len(l)+1
        if qora:
            whitch = "Q"
        else :
            whitch = "A"
        l.append(whitch+str(n)+": "+msg)

    #質問や解答への返答処理関数
    def respond(self, num:int, s:str,l:list):
        print(l)
        s=s.split()
        print(s)
        l[num-1] = l[num-1]+" : "+s[1]

    #番号振り直し関数
    def reindex(self, l:list,type:bool)->list:
        # typeが真のときは質問、偽のときは解答とする。
        new = l
        if type :
            qa = "Q"
        else:
            qa = "A"
        for i in range(len(l)):
            msg = l[i].split(": ",1)
            print(msg)
            new[i] = qa+str(i)+": "+msg[1]
        return new

    @commands.command(description="ウミガメのスープのルールを説明します。",brief="ウミガメのスープのルールを説明します。")
    async def readme(self, recieve):
        m = """■Lateral Thinking Puzzles (ウミガメのスープ)
「出題者」が出した文章の真意を「質問者」が解く遊び。
「質問者」はYES・NOで答えられる質問を「出題者」にすることができる。
Discordで行うにあたって：
(1)質問は「」でくくること。「」内文章に対しYES・NOで応対する。
(2)解答は『』でくくること。"""
        await recieve.channel.send(m)

    @commands.command(description="""これまでに出た質問(「」で囲まれた言葉)の履歴を表示します。""",brief="これまでに出た解答の履歴を表示します。")
    async def list(self, history):
        m = ""
        if len(self.q_list) == 0:
            m="まだ質問がされていません"
        else:
            for i in range(len(self.q_list)):
                m = m + self.q_list[i]+"\n"
        print(m)
        await history.channel.send(m)

    @commands.command(description="""これまでに出た解答(『』で囲まれた言葉)の履歴を表示します。""",brief="これまでに出た解答の履歴を表示します。")
    async def lista(self, history):
        m = ""
        if len(self.a_list) == 0:
            m="まだ解答がされていません"
        else:
            for i in range(len(self.a_list)):
                m = m + self.a_list[i]+"\n"
        print(m)
        await history.channel.send(m)

    @commands.command(description="""質問を修正します。
*使用方法*
!req (修正したい質問番号) (質問の修正)""",brief="質問の修正ができます。")
    async def req(self, ctx,num:int, s:str):
        if len(self.q_list)<=num-1:
    	    m = "Error! Q"+str(num)+"はまだ存在しません"
        else:
            self.q_list[num-1]="Q"+str(num)+": "+s
            m = "Q"+str(num)+"の変更を受理しました。"
        await ctx.channel.send(m)

    @commands.command(description="""解答を修正します。
*使用方法*
!rea (修正したい解答番号) (解答の修正)""",brief="解答の修正ができます。")
    async def rea(self, ctx,num:int, s:str):
        if len(self.a_list)<=num-1:
            m = "Error! A"+str(num)+"はまだ存在しません"
        else:
            self.a_list[num-1]="A"+str(num)+": "+s
            m = "A"+str(num)+"の変更を受理しました。"
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


    @commands.command(description="10回に1回,「なーご」と鳴きます。",brief="おねこさま")
    async def neko(self, n):
        r = random.randint(0,9)
        nya = "みゃー"
        if r == 0:
            nya = "なーご"
        elif r%5 == 0:
            r = random.randint(0,9)
            if r%4 == 0:
                nya = "にゃん"
            else:
                pass
        else :
            nya = "にゃーん"
        await n.channel.send(nya)

    @commands.command(description="""質問や解答の履歴をBOTから削除し、listコマンド等で参照できないようにします。このコマンドによって削除された質問や解答は、チャンネルの履歴には残ります。
*使用方法*
!delall : BOTに記録された全ての履歴を削除します""",brief="質問や解答の履歴をBOTから全て削除します。チャンネルからは削除されません。")
    async def delall(self, ctx):
        m="Error"
        self.a_list.clear()
        self.q_list.clear()
        m = "全て削除しました"
        await ctx.channel.send(m)

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

        if message.content.startswith("「"):
            m = message.content[1:-1]
            self.add_to_list(m,self.q_list,1)
            m = self.q_list[-1]
            print(self.q_list[-1])
            await message.channel.send(m)

        if message.content.startswith("『"):
            m = message.content[1:-1]
            self.add_to_list(m,self.a_list,0)
            m = self.a_list[-1]
            print(self.a_list[-1])
            await message.channel.send(m)

        if message.content.startswith("Q") or message.content.startswith("q") or message.content.startswith("ｑ") or message.content.startswith("Ｑ"):
            num = int(re.sub(r"\D","",message.content))
            if len(self.q_list)<num:
                m = "Error! 数値に対応する質問がまだ存在しません"
            else:
                self.respond(num,message.content,self.q_list)
                m = self.q_list[num-1]
            await message.channel.send(m)

        if message.content.startswith("A") or message.content.startswith("a") or message.content.startswith("ａ") or message.content.startswith("Ａ"):
            num = int(re.sub(r"\D","",message.content))
            if len(self.a_list)<num:
                m = "Error! 数値に対応する解答がまだ存在しません"
            else:
                self.respond(num,message.content,self.a_list)
                m = self.a_list[num-1]
            await message.channel.send(m)

        #await self.bot.process_commands(message)


# BOT本体からコグを読み込む際に呼び出される関数
def setup(bot):
    bot.add_cog(LTPcog(bot))

