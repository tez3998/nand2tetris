import os
import re
import sys

from CodeWriter import CodeWriter
from CommandType import CommandType
from Parser import Parser

def get_final_path_name(path: str) -> str:
    """
    与えられたパスの末尾のディレクトリかファイルのみを返す
    """
    return os.path.basename(p=os.path.normpath(path=path))


# TODO: できたら処理を1つのクラスにまとめることで、メインルーチンをすっきりさせたい
if __name__ == "__main__":
    path_to_file_or_dir: str = sys.argv[1] # VMファイルかVMファイルを含んだディレクトリまでのパス
    input_files: list[str] = []
    output_file_name: str = re.sub(pattern=".vm$", repl=".asm", string=get_final_path_name(path=path_to_file_or_dir))

    # 各ファイルまでのパスをリスト化
    if os.path.isdir(s=path_to_file_or_dir):
        path_to_dir: str = path_to_file_or_dir
        for file_candidate in os.listdir(path=path_to_dir):
            path: str = os.path.join(path_to_dir, file_candidate)
            if os.path.isfile(path=path):
                input_files.append(path)
    elif os.path.isfile(path=path_to_file_or_dir):
        input_files.append(path_to_file_or_dir)
    else:
        print("引数として、ファイルかディレクトリまでの有効なパスを指定してください\n")
        sys.exit(1)

    # アセンブリの生成を開始
    code_writer: CodeWriter = CodeWriter(output_file_name=output_file_name)
    code_writer.initSP()
    command_type: CommandType = CommandType()

    for input_file in input_files:
        parser: Parser = Parser(path_to_file=input_file)
        vm_file_name: str = get_final_path_name(path=input_file)
        code_writer.setFileName(filename=vm_file_name)
        while parser.hasMoreCommands():
            parser.advance()
            cmd_type: str = parser.commandType()
            if cmd_type == command_type.c_arithmetic:
                cmd: str = parser.arg1()
                code_writer.writeArithmetic(command=cmd)
            elif cmd_type == command_type.c_push:
                segment: str = parser.arg1()
                index: int = parser.arg2()
                code_writer.writePushPop(command="push", segment=segment, index=index)
            elif cmd_type == command_type.c_pop:
                segment: str = parser.arg1()
                index: int = parser.arg2()
                code_writer.writePushPop(command="pop", segment=segment, index=index)
            else:
                print("命令のタイプが不正です")
                sys.exit(1)
    
    # アセンブリの生成を終了
    code_writer.finishWriting()