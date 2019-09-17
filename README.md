# LTPbot

## 目次

+ [LTPbotとは？](#LTPbotとは？)
+ [このbotでウミガメのスープを行うにあたってのルール](#このbotでウミガメのスープを行うにあたってのルール)
+ [使い方](#使い方)
  - [非コマンド命令](#非コマンド命令)
  - [コマンド命令](#コマンド命令)

___

## LTPbotとは？

discord上で水平思考パズル（lateral thinking puzzle, LTP)――ウミガメのスープをもっと楽に行うために作成したbotです。
コピペの手間を減らしたり、これまでに出た質問を一覧で確認できるようにしたりすることを目的としています。

自分が参加しているdiscordサーバーで使用することを目的として作成していますので、botそのものをweb上に公開する予定はありません。

## このbotでウミガメのスープを行うにあたってのルール

このbotではウミガメのスープを行うにあたり、次のようなルールを採用しています。

> 1. 質問は「」でくくること。「」内文章に対しYES・NOで応対する。
> 2. 解答は『』でくくること。

**質問**とは、参加者が出題者に対し、問題を解き明かすために行う問い(e.g.「男は食い逃げをしましたか？」)を指します。  
**解答**とは、参加者が予想した問題の答え(e.g.『男が飲んだスープの中に人間を自殺させる寄生虫が潜んでいたため』)を指します。

## 使い方

このbotにはコマンドを用いない命令と用いる命令の二つがあります。このreadmeでは前者を非コマンド命令、後者をコマンド命令とします。

*いづれの命令も、一回のメッセージ送信につき最初の一つしか実行されません。*

### 非コマンド命令

#### 「(質問)」

「」でくくった質問にbotが自動で番号を振ります。

~~~
「男は食い逃げをしましたか？」
↓
Q1: 男は食い逃げをしましたか？
~~~

#### 『(解答)』

『』でくくった解答にbotが自動で番号を振ります。

~~~
『男が飲んだスープの中に人間を自殺させる寄生虫が潜んでいたため』
↓
A1: 男が飲んだスープの中に人間を自殺させる寄生虫が潜んでいたため
~~~

#### Q(数字) (YES/NO)

Q(数字) (YES/NO)で数字に対応する質問への返答ができます。スペースは、数字のうしろにのみ入れて、それ以外の場所には入れないようにしてください。

~~~
Q1 NO
↓
Q1: 男は食い逃げをしましたか？ : NO
~~~

#### A(数字) (正解/不正解)

A(数字) (正解/不正解)で数字に対応する解答への返答ができます。スペースは、数字のうしろにのみ入れて、それ以外の場所には入れないようにしてください。

~~~
A1 NO
↓
A1: 男が飲んだスープの中に人間を自殺させる寄生虫が潜んでいたため : 不正解
~~~

### コマンド命令

コマンド命令は頭に?を付けて実行します。

#### ?help

コマンドの一覧を表示します。  
`?help (command)`でコマンドの詳細な説明を見ることができます。

#### ?readme

#### ?list

#### ?lista

#### ?req (数字) (修正内容)

#### ?rea (数字) (修正内容)

#### ?delall

#### ?neko

