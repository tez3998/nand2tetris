import re
from io import TextIOWrapper

class CodeWriter:
    class Asm_Command:
        """
        ファイルに書き込む一連のアセンブリコマンドを保持するクラス
        """
        def __init__(self) -> None:
            self.__commands = "" # 書き込み前の一連のアセンブリコマンド
        

        def clear(self) -> None:
            """
            保持していた一連のアセンブリコマンドを削除する
            """
            self.__commands = ""
        

        def append(self, *commands: str):
            """
            保持するアセンブリコマンドを増やす。
            *commandsはアセンブリコマンドのリスト
            """
            for cmd in commands:
                if not re.match(pattern="^\(.*\)$", string=cmd): # アセンブリの読みやすさのために、疑似コマンド以外は字下げ
                    cmd = "    " + cmd
                self.__commands += cmd + "\n"
        

        def get_commands(self) -> str:
            """
            現在保持している一連のアセンブリコマンドを削除する
            """
            return self.__commands


    def __init__(self, output_file_name: str) -> None:
        self.__file_name = "" # .vmファイルの名前から最後の".vm"を除いた部分
        self.__output_file: TextIOWrapper = open(file=output_file_name, mode="w") # 出力するアセンブリファイル
        self.__asm_commands: CodeWriter.Asm_Command = CodeWriter.Asm_Command() # 一連のアセンブリコマンドを保持するためのオブジェクト
        self.__symbol_index: int = 0 # ジャンプ命令の時に使うシンボルをアセンブリファイル中で一意にするためのインデックス。新しいシンボルを生成する毎に1ずつインクリメントさせる
    

    def __del__(self):
        self.__output_file.close()
    
    
    def __write_asm_command(self):
        """
        Asm_Commandオブジェクトに溜まった一連のコマンドをアセンブリファイルに書き込む。
        書き込みが完了したら、Asm_Commandオブジェクトが保持している一連のコマンドをAsm_Commandオブジェクトから削除する。
        """
        self.__output_file.write(self.__asm_commands.get_commands())
        self.__asm_commands.clear()


    def __increase_sp(self) -> None:
        """
        スタックポインタを1だけ増加させる
        """
        self.__asm_commands.append("@SP",
                                    "M=M+1")


    def __decrease_sp(self) -> None:
        """
        スタックポインタを1だけ減少させる
        """
        self.__asm_commands.append("@SP",
                                    "M=M-1")
    

    def __push_to_stack(self) -> None:
        """
        値をレジスタDからスタックにpushする
        """
        self.__asm_commands.append("@SP",
                                    "A=M",
                                    "M=D")
        self.__increase_sp()


    def __pop_from_stack(self) -> None:
        """
        値をスタックからレジスタDにpopする
        """
        self.__decrease_sp()
        self.__asm_commands.append("@SP",
                                    "A=M",
                                    "D=M")
    

    def __write_1_args_default_arithmetic(self, operator: str) -> None:
        """
        Hackアセンブリ言語にデフォルトである、1変数関数を出力ファイルに書き込む
        """
        self.__pop_from_stack()
        self.__asm_commands.append(f"D={operator}D")
        self.__push_to_stack()
        self.__write_asm_command()


    def __write_2_args_default_arithmetic(self, operator: str) -> None:
        """
        Hackアセンブリ言語にデフォルトである、2変数関数を出力ファイルに書き込む。
        operatorは2変数関数の演算子。
        """
        self.__pop_from_stack()
        self.__asm_commands.append("@R13",
                                    "M=D")
        self.__pop_from_stack()
        self.__asm_commands.append("@R13",
                                    f"D=D{operator}M")
        self.__push_to_stack()
        self.__write_asm_command()
    

    def __write_2_args_arithmetic(self, jump_command: str) -> None:
        """
        Hackアセンブリ言語にデフォルトでない、2変数関数を出力ファイルに書き込む。
        jump_commnadはJEQのようなアセンブリ命令のjump領域に対応する。
        jump_commandが真になるときはスタックに-1をプッシュし、偽になるときはスタックに0をプッシュする
        """
        symbol_true: str = "TRUE" + str(self.__symbol_index)
        symbol_end: str = "END" + str(self.__symbol_index)

        self.__pop_from_stack()
        self.__asm_commands.append("@R13",
                                    "M=D")
        self.__pop_from_stack()
        self.__asm_commands.append("@R13",
                                    "D=D-M",
                                    f"@{symbol_true}",
                                    f"D;{jump_command}",
                                    "D=0")
        self.__push_to_stack()
        self.__asm_commands.append(f"@{symbol_end}",
                                    "0;JMP",
                                    f"({symbol_true})",
                                    "D=-1")
        self.__push_to_stack()
        self.__asm_commands.append(f"({symbol_end})")
        self.__write_asm_command()

        self.__symbol_index += 1


    def initSP(self) -> None:
        """
        SPに初期値を設定する。
        """
        self.__asm_commands.append("@256",
                                    "D=A",
                                    "@SP",
                                    "M=D")
        self.__write_asm_command()


    def finishWriting(self) -> None:
        """
        アセンブリの終了を示す無限ループを追加する
        """
        self.__asm_commands.append("(END)",
                                    "@END",
                                    "0;JMP")
        self.__write_asm_command()


    def setFileName(self, filename: str) -> None:
        """
        現在処理しているVMファイルの名前をCodeWriterに知らせる。
        名前にはXxx.vmのように、.vmという拡張子が含まれていることの想定している
        """
        file_extension_pattern: str = ".vm"
        self.__file_name = re.sub(pattern=file_extension_pattern, repl="", string=filename)


    def writeArithmetic(self, command: str) -> None:
        """
        算術命令を出力ファイルに書き込む。
        commandはaddなどのVM言語の算術命令に対応している。
        """
        if command == "add":
            self.__write_2_args_default_arithmetic(operator="+")
        elif command == "sub":
            self.__write_2_args_default_arithmetic(operator="-")
        elif command == "neg":
            self.__write_1_args_default_arithmetic(operator="-")
        elif command == "eq":
            self.__write_2_args_arithmetic(jump_command="JEQ")
        elif command == "gt":
            self.__write_2_args_arithmetic(jump_command="JGT")
        elif command == "lt":
            self.__write_2_args_arithmetic(jump_command="JLT")
        elif command == "and":
            self.__write_2_args_default_arithmetic(operator="&")
        elif command == "or":
            self.__write_2_args_default_arithmetic(operator="|")
        elif command == "not":
            self.__write_1_args_default_arithmetic(operator="!")


    # TODO: 記述に重複がある部分は関数などにまとめる
    def writePushPop(self, command: str, segment: str, index: int) -> None:
        """
        push命令とpop命令を出力ファイルに書き込む。
        commandはVM命令のpushまたはpopに、segmentはVMのメモリセグメントに、indexは各ベースアドレスからのアドレスに対応している。
        """
        if command == "push":
            if segment == "local":
                self.__asm_commands.append("@LCL",
                                            "D=M",
                                            f"@{index}",
                                            "A=D+A",
                                            "D=M")
            elif segment == "argument":
                self.__asm_commands.append("@ARG",
                                            "D=A",
                                            f"@{index}",
                                            "A=D+A",
                                            "D=M")
            elif segment == "this":
                self.__asm_commands.append("@THIS",
                                            "D=M",
                                            f"@{index}",
                                            "A=D+A",
                                            "D=M")
            elif segment == "that":
                self.__asm_commands.append("@THAT",
                                            "D=M",
                                            f"@{index}",
                                            "A=D+A",
                                            "D=M")
            elif segment == "pointer":
                address: int = 3 + index # 3はTHISのアドレス
                self.__asm_commands.append(f"@{address}",
                                            "D=M")
            elif segment == "temp":
                address: int = 5 + index # 5はtempセグメントの最小のアドレス
                self.__asm_commands.append(f"@{address}",
                                            "D=M")
            elif segment == "constant":
                self.__asm_commands.append(f"@{index}",
                                            "D=A")
            elif segment == "static":
                self.__asm_commands.append(f"@{self.__file_name}.{index}",
                                            "D=M")
            self.__push_to_stack()
        elif command == "pop":
            self.__pop_from_stack()
            if segment == "local":
                self.__asm_commands.append("@R13",
                                            "M=D", # スタックから取り出してきた値をR13に退避
                                            "@LCL",
                                            "D=M",
                                            f"@{index}",
                                            "D=D+A",
                                            "@R14",
                                            "M=D", # 操作対象のアドレスをR14に退避
                                            "@R13",
                                            "D=M",
                                            "@R14",
                                            "A=M",
                                            "M=D")
            elif segment == "argument":
                self.__asm_commands.append("@R13",
                                            "M=D", # スタックから取り出してきた値をR13に退避
                                            "@ARG",
                                            "D=M",
                                            f"@{index}",
                                            "D=D+A",
                                            "@R14",
                                            "M=D", # 操作対象のアドレスをR14に退避
                                            "@R13",
                                            "D=M",
                                            "@R14",
                                            "A=M",
                                            "M=D")
            elif segment == "this":
                self.__asm_commands.append("@R13",
                                            "M=D", # スタックから取り出してきた値をR13に退避
                                            "@THIS",
                                            "D=M",
                                            f"@{index}",
                                            "D=D+A",
                                            "@R14",
                                            "M=D", # 操作対象のアドレスをR14に退避
                                            "@R13",
                                            "D=M",
                                            "@R14",
                                            "A=M",
                                            "M=D")
            elif segment == "that":
                self.__asm_commands.append("@R13",
                                            "M=D", # スタックから取り出してきた値をR13に退避
                                            "@THAT",
                                            "D=M",
                                            f"@{index}",
                                            "D=D+A",
                                            "@R14",
                                            "M=D", # 操作対象のアドレスをR14に退避
                                            "@R13",
                                            "D=M",
                                            "@R14",
                                            "A=M",
                                            "M=D")
            elif segment == "pointer":
                address: int = 3 + index # 3はTHISのアドレス
                self.__asm_commands.append(f"@{address}",
                                            "M=D")
            elif segment == "temp":
                address: int = 5 + index # 5はtempセグメントの最小のアドレス
                self.__asm_commands.append(f"@{address}",
                                            "M=D")
            elif segment == "constant":
                pass # constantでpopは多分ないと思う
            elif segment == "static":
                self.__asm_commands.append(f"@{self.__file_name}.{index}",
                                            "M=D")
        self.__write_asm_command()