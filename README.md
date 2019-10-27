# LTPbot

## 目次

+ [LTPbotとは？](#LTPbotとは？)
+ [このbotでウミガメのスープを行うにあたってのルール](#このbotでウミガメのスープを行うにあたってのルール)
+ [使い方](#使い方)
  - [ウミガメのスープ関連コマンド](#ウミガメのスープ関連コマンド)
  - [その他のコマンド](#その他のコマンド)
+ [今後の予定](#今後の予定)
+ [AUTHOR](#AUTHOR)
+ [LICENSE](#LICENSE)
___

## LTPbotとは？

discord上で水平思考パズル（lateral thinking puzzle, LTP)――ウミガメのスープをもっと楽に行うために作成したbotです。
コピペの手間を減らしたり、これまでに出た質問を一覧で確認できるようにしたりすることを目的としています。

自分が参加しているdiscordサーバーで使用することを目的として作成していますので、botそのものをweb上に公開する予定はありません。

## このbotでウミガメのスープを行うにあたってのルール

このbotではウミガメのスープを行うにあたり、次のようなルールを採用しています。

> 1. 質問は「」でくくること。「」内文章に対しYES・NOで応対する。
> 2. 解答は『』でくくること。

**質問**とは、参加者が出題者に対し、問題を解き明かすために行う問いを指します。  
~~~
e.g.「男は食い逃げをしましたか？」
~~~
**解答**とは、参加者が予想した問題の答えを指します。
~~~
e.g.『男が飲んだスープの中に人間を自殺させる寄生虫が潜んでいたため』
~~~

## このbotを用いたウミガメのスープの流れ

1. `?start`でbotのウミガメのスープ関連コマンドを有効にしましょう。
2. 出題者が問題を出します。
3. 参加者は質問をしていきましょう。出題者は質問に答え、情報を出していきます。
4. 答えが分かった参加者は解答をしましょう。それに出題者が正解と言えばゲームは終了です。
5. `?finish`でウミガメのスープ関連コマンドを無効にしましょう。

*コマンドは、一回のメッセージ送信につき**最初の一つ**しか実行されません。*

### ウミガメのスープ関連コマンド

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

Q(数字) (YES/NO)で数字に対応する質問への返答ができます。“Q(数字)”と“(YES/NO)”の間にはスペースを入れてください。

~~~
Q1 NO
↓
Q1: 男は食い逃げをしましたか？ : NO
~~~

#### A(数字) (正解/不正解)

A(数字) (YES/NO)で数字に対応する質問への返答ができます。“A(数字)”と“(YES/NO)”の間にはスペースを入れてください。

~~~
A1 不正解
↓
A1: 男が飲んだスープの中に人間を自殺させる寄生虫が潜んでいたため : 不正解
~~~

#### ?list

これまでに出た質問の一覧を表示します。質問への返答がある場合はそれも一緒に表示されます。
引数として、**数値**と**文字列**を指定できます。

数値を引数にとると、その数値分だけ質問を表示します。正の数を指定すると古い順にn件、負の数を指定すると新しい順にn件表示します（nは引数）。
文字列を引数にとると、応答がない質問のみを表示します。現在の仕様上、どのような文字列でも構いませんが、"no reply"の頭文字をとって"n"や"nr"を引数とすることを推奨します。

#### ?lista

これまでに出た解答の一覧を表示します。解答への返答がある場合はそれも一緒に表示されます。
引数の仕様は`?list`と同じです。

#### ?delall

botに登録された質問と解答の履歴を全て削除します。チャンネルに送信されたメッセージ自体は残ります。

#### ?req(数字) (修正内容)

質問を修正します。

#### ?rea(数字) (修正内容)

解答を修正します。

#### ?playlog

プレイログを表示します。ゲームの振り返りなどにご利用下さい。

`?log`でも実行可能です。

### その他のコマンド

#### ?help

コマンドの一覧を表示します。  
`?help (command)`でコマンドの詳細な説明を見ることができます。

#### ?start

ウミガメのスープ関連コマンドを有効にします。ウミガメのスープを開始する際に使用して下さい。

#### ?finish

ウミガメのスープ関連コマンドを無効にします。ウミガメのスープを終了する際に使用して下さい。

また、終了と同時にプレイログを出力します（ここで出力されるプレイログは`?playlog`コマンドを使用した時のものと同じものです）。

#### ?readme

ウミガメのスープのルールを表示します。

#### ?neko

にゃーん。

おねこさまが鳴きます。鳴き方はランダム。

#### ?inu

わんっ。

おいぬさまが鳴きます。鳴き方はランダム。

## 今後の予定

+ 個別の質問/解答を削除するコマンド`?delete`や出題された問題を確認するコマンド`?theme`などを実装していきます。
+ `Q(数字) (YES/NO)`と`A(数字) (正解/不正解)`をその回の問題の出題者のみが使えるようにしようと考えています。
+ `?req (数字) (修正内容)`、`?rea (数字) (修正内容)`によって第三者が勝手に質問や解答を書き変えることができないようにするつもりです。
+ BOTの発言でログが埋まらないように改良を重ねます
+ 希望する人のdmにコマンドの実行結果を送信するようにします
+ 折を見てコードのリファクタリングを行っていきます。
+ ~~`?playlog`を実行した際、プレイログに発言者名も記載されるようにします。~~（実装済）

## AUTHOR

[msattova](https://github.com/msattova)

## LICENSE

This software is released under the MIT License.
