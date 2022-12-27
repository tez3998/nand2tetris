# 動作環境
* Python 3.10.6

# バーチャルマシンの動かし方
1. Pythonスクリプトのあるディレクトリへ移動
```powershell
cd VMtranslator
```

2. 以下のように、バーチャルマシンを実行する
```powershell
python VMtranslator.py .vmファイルまたは.vmファイルを含むディレクトリへのパス（相対パスでもOKなはず）
```

例（パスはOSがWindowsの場合）
```powershell
python .\VMtranslator.py ..\StackArithmetic\StackTest\StackTest.vm
```

3. 今いるディレクトリに.asmファイルが作成されるので確認

# 保留にしたところ
## BasicTest.vmの動作をVMEmulatorと同じにすること
以下が分からなかったので、このテストを保留にした。
* セグメントがlocalまたはargumentである命令がVMEmulatorに入力されると、`Out of segment space in .1`などというエラーメッセージが出力され、その命令はなかったことにされた。しかし、そのような仕様は日本語版の書籍には書かれていなかったので、そのような機能をバーチャルマシンに付け足すべきかどうか分からなかった。
* セグメントがpointerである命令でTHISやTHATに明示的にベースアドレスを指定していないにも関わらず、作成したバーチャルマシンで.vmファイルを.asmファイルに変換しCPUEmulatorでその.asmファイルを実行したところ、あたかもTHISに3030がTHATに3040が設定されていたような挙動になった。これはCPUEmulatorの挙動を1命令ごとに追っていけば分かると思うが、日本語書籍にそのような仕様はなかったし、なにしろ面倒だったため、なぜこうなるかは分からないままである。
