# nand2tetris
『コンピュータシステムの理論と実装－モダンなコンピュータの作り方』のプロジェクト

# コンピュータシステムの理論と実装－モダンなコンピュータの作り方
> コンピュータを理解するための最善の方法はゼロからコンピュータを作ることです。コンピュータの構成要素は、ハードウェア、ソフトウェア、コンパイラ、OSに大別できます。本書では、これらコンピュータの構成要素をひとつずつ組み立てます。具体的には、NANDという電子素子からスタートし、論理ゲート、加算器、CPUを設計します。そして、オペレーティングシステム、コンパイラ、バーチャルマシンなどを実装しコンピュータを完成させて、最後にその上でアプリケーション（テトリスなど）を動作させます。実行環境はJava（Mac、Windows、Linuxで動作）。（裏表紙より引用）

# 取り組んでいるプロジェクト
プロジェクト5：コンピュータアーキテクチャ

# 実装方法が分からなかったプロジェクト
* プロジェクト4のFill.asm

# 躓いたところ
## エラー：',', or ')' are expected
ピンの名前に_を使うとこのエラーが発生する。
そのため、ピンの名前には英数字のみを使用する。

## エラー：Sub bus of an internal node may not be used
プロジェクト2のALUを実装するときに発生した。

やりたかったことは、Or8Way(in[8], out)という部品に、ALUの入力バス（INの後で定義されるバス）でない内部バスintenal[16]の前半部分と後半部分を2つのOr8Wayのinに分けて入れる、ということだった。
イメージとしては次のような記述である。

```hdl
Or8Way(in=internal[0..7], out=out0)
Or8Way(in=internal[8..15], out=out1)
```

しかし、こうすると上記のエラーが発生する。
調べたところ、どうやらin=a[0..7]のようなinの右辺に[　]を使う記述ができるのは、aが入力バスのときのみのようだった。
このエラーの解決策としては、Or16Way(in[16], out)のような部品を自分で用意して、その部品内で

```hdl
Or8Way(in=in[0..7], out=out0)
Or8Way(in=in[8..15], out=out1)
```

としておいて、元の部品内（今回の場合、ALU）では

```hdl
Or16Way(in=internal, out=out0)
```

とするやり方がある。
この場合、inはOr16Way内では入力バスなので、in=a[0..7]のようなinの右辺に[　]を使う記述をしてもエラーは発生しない。
詳細はプロジェクト2のALU.hdlを参照する。

## エラー：Expression Expected
プロジェクト4のFill.asmを実装するところで発生した。

Mに直接0、1、-1以外の数字を代入しようとすると発生する。

```asm
@1
M=1024 // エラー
```

Mに0、1、-1以外の数字を代入する場合は、AとDを経由して代入するとエラーが出なくなる。

```asm
@1024
D=A
@1
M=D
```
