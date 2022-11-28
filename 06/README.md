# 動作環境
* Python 3.10.6

# アセンブラの動かし方
1. Assemblerディレクトリに移動する
```powershell
cd Assembler
```
2. 以下のように引数を指定して実行する
```powershell
python Assembler.py .asmファイルまでのパス 出力される.hackファイルの名前
```
例（Windowsのパスの場合）
```powershell
python Assembler.py C:\nand2tetris\projects\06\rect\Rect.asm Rect.hack
```
3. Assembler.pyと同じディレクトリに.hackファイルが生成されるので確認する
