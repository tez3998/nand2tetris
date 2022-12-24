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
* localまたはargumentの命令がVMEmulatorに入力されると、`Out of segment space in 1.`というエラーメッセージが出力され、その命令はなかったことにされる（おそらく、LCL（RAM[1]）やARG（RAM[2]）が0のままなのがいけないのだと思う）。しかし、そのような仕様は日本語版の書籍には書かれていなかったので、そのような機能をバーチャルマシンに付け足すべきかどうか分からなかった。
* THISやTHATに明示的にベースアドレスを指定していないにも関わらず、作成したバーチャルマシンで.vmファイルを.asmファイルに変換しCPUEmulatorでその.asmファイルを実行すると、あたかもTHISに3030がTHATに3040が設定されていたような挙動になる。しかし、そのような仕様も日本語版の書籍には書かれていなかったので、そのような機能を実装すべきか分からなかった。
