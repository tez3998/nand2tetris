# 動作環境
* Python 3.10.6

# バーチャルマシンの動かし方
1. Pythonスクリプトのあるディレクトリへ移動
```powershell
cd VMtranslator
```

2. 以下のように、バーチャルマシンを実行する
```powershell
python VMtranslator.py Sys.vmファイルまたはSys.vmファイルを含むディレクトリへのパス（相対パスでもOKなはず）
```

例（パスはOSがWindowsの場合）
```powershell
python .\VMtranslator.py ..\FunctionCalls\StaticsTest
```

3. 今いるディレクトリに.asmファイルが作成されるので確認

# 不明点
## ブートストラップコードが想定していないテスト
仕様ではSys.initという名前の関数を呼び出すことでプログラムが開始することになっているため、そのようなブートストラップコードが生成されるようにバーチャルマシンを実装した。
そのため、Sys.vmファイルがないとテストを動かすことができなかった（ブートストラップコードを取り除けばテストをパスすることはできた）。

## ブートストラップコードによる初期設定と異なる初期設定を想定しているテスト
仕様ではプログラムのはじめにSPに256を設定するようなブートストラップコードをアセンブリに書くことになっているため、バーチャルマシンもそのように実装した。
そのため、.tstファイルでSPに256以外を設定するようなテストだと、出力結果が異なってしまった。