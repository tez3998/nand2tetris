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
