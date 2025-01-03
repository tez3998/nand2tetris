この第1版のプロジェクトを完遂する前に第2版が出てしまったので、そちらに取り組み中。

第2版用のリポジトリはこちら：
[tez3998/nand2tetris-2nd-ed](https://github.com/tez3998/nand2tetris-2nd-ed)

# nand2tetris
『コンピュータシステムの理論と実装－モダンなコンピュータの作り方』のプロジェクト

# コンピュータシステムの理論と実装－モダンなコンピュータの作り方
> コンピュータを理解するための最善の方法はゼロからコンピュータを作ることです。コンピュータの構成要素は、ハードウェア、ソフトウェア、コンパイラ、OSに大別できます。本書では、これらコンピュータの構成要素をひとつずつ組み立てます。具体的には、NANDという電子素子からスタートし、論理ゲート、加算器、CPUを設計します。そして、オペレーティングシステム、コンパイラ、バーチャルマシンなどを実装しコンピュータを完成させて、最後にその上でアプリケーション（テトリスなど）を動作させます。実行環境はJava（Mac、Windows、Linuxで動作）。（裏表紙より引用）

# 取り組んでいるプロジェクト
プロジェクト10: コンパイラ\#1：構文解析

# 躓いたところ
## エラー
### ',', or ')' are expected
ピンの名前に_を使うとこのエラーが発生する。
そのため、ピンの名前には英数字のみを使用する。

### Sub bus of an internal node may not be used
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

### Expression expected
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

## 不具合
### Windows 11にてディスプレイの大きさによってはHardwareSimulatorの実行結果の欄が表示されない
Windows 11ではディスプレイの縦の長さが約8cm未満だと、HardwareSimulatorを画面いっぱいに表示しても、テストの実行結果やエラーが表示される欄が表示されない。

<img width="728" alt="nand2tetris-win-bug" src="https://user-images.githubusercontent.com/90051826/185859924-8bb1b008-f5ce-45db-aa17-c40a00885c8f.png">

一方、Ubuntu 18.04では表示される。

<img width="729" alt="nand2tetris-bug-linux" src="https://user-images.githubusercontent.com/90051826/185860088-bf500e86-8b25-4133-ada8-022ae2cc2350.png">

対応策は仮想マシンや実機などにLinuxを入れてそこでnand2tetrisをやるか、ディスプレイの縦の長さが8cm以上のモニタを用意しそのモニタにHardwareSimulatorを表示させるか、[公式サイト](https://www.nand2tetris.org/software)でソースコードが公開されているのでそれを自力で修正するかだと思う。

## 書籍の記述
### 疑似コードの*（アスタリスク）の意味
日本語版書籍の8章の図8-5で遭遇した。

唐突にアスタリスクが使われていたので、その意味が分からなかった。
考えた結果、以下のような結論に至った。

例えば、書籍に出てくる次の疑似コードは
```
*ARG = pop()
```
次のようなコードと同じ意味だと思う。
```
RAM[RAM[ARG]] = pop()
// 日本語の意味：
// スタックからpopしてきた値をRAMのRAM[ARG]番地、つまりRAM[2]番地にセットする
```

一方、アスタリスクの付いていない場合を見ると、例えば、書籍に出てくる次のコードであれば、
```
SP = ARG+1
```
というものがあるが、これは次のコードと同じだと思う。
```
RAM[SP] = RAM[ARG]+1
// 日本語の意味：
// RAM[ARG]（実態はRAM[2]）に1を足した値をRAM[SP]（実態はRAM[0]）にセットする
```

## 7章のBasicTest.vmの動かし方
1. 作成したバーチャルマシンから生成されたアセンブリと同じディレクトリにBasicTest.tstとBasicTest.cmpをコピーしてくる
1. CPUEmulatorを開き、`Load Script`（紙のアイコン。ホバーするとLoad Scriptと表示される）をクリックして、BasicTest.tstを読み込む
1. `>>`のアイコンをクリックし、CPUEmulatorを走らせる
