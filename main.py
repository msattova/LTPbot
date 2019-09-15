# coding: utf-8

import random
import discord
import re
from discord.ext import commands

TOKEN = ""

BOT_PREFIX = '!'

client = commands.Bot(command_prefix=BOT_PREFIX)

# 質問リスト
q=[]

# 解答リスト
a=[]

#質問・解答追加処理関数
def add_to_list(msg,list,qora:bool):
    n = len(list)+1
    if qora:
        whitch = "Q"
    else :
        whitch = "A"
    list.append(whitch+str(n)+": "+msg)

#質問や解答への返答処理関数
def respond(num:int, s:str,l:list):
    print(l[num-1])
    s.split()
    print(s)
    l[num-1] = l[num-1]+" : "+s[1]

#番号振り直し関数
def reindex(l:list,type:bool)->list:
    # typeが真のときは質問、偽のときは解答とする。
    new = l
    if type :
        qa = "Q"
    else:
        qa = "A"
    for i in range(len(l)):
        new[i] = qa+str(i)+": "+list[i].split(": ",1)[1]
    return new

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    global q
    global a
    if message.author.bot:
        return
    await client.process_commands(message)
    # 行頭の空白除外処理
    message.content.lstrip(" ")
    message.content.lstrip("　")
    if message.content.startswith("!"):
        message.content.rstrip(" ")
        message.content.rstrip("　")

    if message.content.startswith("「"):
        m = message.content[1:-1]
        add_to_list(m,q,1)
        m = q[-1]
        print(q[-1])
        await message.channel.send(m)

    if message.content.startswith("『"):
        m = message.content[1:-1]
        add_to_list(m,a,0)
        m = a[-1]
        print(a[-1])
        await message.channel.send(m)

    if message.content.startswith("Q") or message.content.startswith("q") or message.content.startswith("ｑ") or message.content.startswith("Ｑ"):
        num = int(re.sub(r"\D","",message.content))
        if len(q)<num:
            m = "Error! 数値に対応する質問がまだ存在しません"
        else:
            respond(num,message.content,q)
            m = q[num-1]
        await message.channel.send(m)

    if message.content.startswith("A") or message.content.startswith("a") or message.content.startswith("ａ") or message.content.startswith("Ａ"):
        num = int(re.sub(r"\D","",message.content))
        if len(a)<num:
            m = "Error! 数値に対応する解答がまだ存在しません"
        else:
            respond(num,message.content,a)
            m = a[num-1]
        await message.channel.send(m)


@client.command(description="ウミガメのスープのルールを説明します。",brief="ウミガメのスープのルールを説明します。")
async def readme(recieve):
    m = """■Lateral Thinking Puzzles (ウミガメのスープ)
「出題者」が出した文章の真意を「質問者」が解く遊び。
「質問者」はYES・NOで答えられる質問を「出題者」にすることができる。
Discordで行うにあたって：
(1)質問は「」でくくること。「」内文章に対しYES・NOで応対する。
(2)解答は『』でくくること。"""
    await recieve.channel.send(m)

@client.command(description="""これまでに出た質問(「」で囲まれた言葉)の履歴を表示します。""",brief="これまでに出た解答の履歴を表示します。")
async def list(history):
    global q
    m = ""
    if len(q) == 0:
        m="まだ質問がされていません"
    else:
        for i in range(len(q)):
            m = m + q[i]+"\n"
    await history.channel.send(m)

@client.command(description="""これまでに出た解答(『』で囲まれた言葉)の履歴を表示します。""",brief="これまでに出た解答の履歴を表示します。")
async def lista(history):
    global a
    m = ""
    if len(a) == 0:
        m="まだ解答がされていません"
    else:
        for i in range(len(a)):
            m = m + a[i]+"\n"
    await history.channel.send(m)

@client.command(description="""質問を修正します。
*使用方法*
!req (修正したい質問番号) (質問の修正)""",brief="質問の修正ができます。")
async def req(ctx,num:int, s:str):
    global q
    if len(q)<=num-1:
    	m = "Error! 数値"+str(num)+"に対応する質問がまだ存在しません"
    else:
        q[num-1]="Q"+str(num)+": "+s
        m = "質問"+str(num)+"の変更を受理しました。"
    await ctx.channel.send(m)

@client.command(description="""解答を修正します。
*使用方法*
!rea (修正したい解答番号) (解答の修正)""",brief="解答の修正ができます。")
async def rea(ctx,num:int, s:str):
    global a
    if len(a)<=num-1:
        m = "Error! 数値に対応する解答がまだ存在しません"
    else:
        a[num-1]="A"+str(num)+": "+s
        m = "解答"+str(num)+"の変更を受理しました。"
    await ctx.channel.send(m)

@client.command(description="""質問や解答の履歴をBOTから削除し、listコマンド等で参照できないようにします。このコマンドによって削除された質問や解答は、チャンネルの履歴には残ります。
*使用方法*
!delete all : BOTに記録された全ての履歴を削除します
!delete q (質問番号) : 指定した質問番号に対応する質問の履歴を削除します。
!delete a (解答番号) : 指定した解答番号に対応する解答の履歴を削除します。""",brief="質問や解答の履歴をBOTから削除します。（なぜか使えない）")
async def delete(ctx,*, arg):
    global a
    global q
    m="Error"
    print(arg)
    if len(arg) == 1:
        a.clear()
        q.clear()
        m = "全て削除しました"
    elif len(arg) == 2:
        num = int(arg[1])
        print(num)
        if arg[0] == "q":
            m = q[num-1]
            del q[num-1]
            reindex(q,0)
        if arg[0] == "a":
            m = a[num-1]
            del a[num-1]
            reindex(a,1)
        m=m+" を削除しました。"
    await ctx.channel.send(m)

@client.command(description="10回に1回,「なーご」と鳴きます。",brief="おねこさま")
async def neko(n):
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
    await n.message.send(nya)

client.run(TOKEN)
