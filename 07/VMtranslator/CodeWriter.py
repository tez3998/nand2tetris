from io import TextIOWrapper

class CodeWriter:
    class Asm_Command:
        """
        ファイルに書き込む一連のアセンブリコマンドを保持するクラス
        """
        def __init__(self) -> None:
            self.__commands = ""
        

        def clear(self) -> None:
            self.__commands = ""
        

        def append(self, *commands: str):
            for cmd in commands:
                self.__commands += cmd
        

        def get_commands(self) -> str:
            return self.__commands


    def __init__(self, output_file_name: str) -> None:
        self.__file_name = ""
        self.__output_file: TextIOWrapper = open(file=output_file_name, mode="w") # 出力するアセンブリファイル
        self.__asm_commands: CodeWriter.Asm_Command = CodeWriter.Asm_Command()
        self.__symbol_index: int = 0 # ジャンプ命令の時に使うシンボルをアセンブリファイル中で一意にするためのインデックス。新しいシンボルを生成する毎に1ずつインクリメントさせる
    
    
    def __write_asm_command(self):
        """
        Asm_Commandオブジェクトに溜まった一連のコマンドをアセンブリファイルに書き込む。
        書き込みが完了したら、Asm_Commandオブジェクトが保持している一連のコマンドをAsm_Commandオブジェクトから削除する。
        """
        self.__output_file.write(self.__asm_commands.get_commands())
        self.__asm_commands.clear()


    def __increase_sp(self) -> None:
        self.__asm_commands.append("@SP\n",
                                    "D=A\n",
                                    "M=D+1\n")


    def __decrease_sp(self) -> None:
        self.__asm_commands.append("@SP\n",
                                    "D=A\n",
                                    "M=D-1\n")
    

    def __push(self) -> None:
        """
        値をレジスタDからスタックにpushする
        """
        self.__asm_commands.append("@SP\n",
                                    "M=D\n")
        self.__increase_sp()


    def __pop(self) -> None:
        """
        値をスタックからレジスタDにpopする
        """
        self.__decrease_sp()
        self.__asm_commands.append("@SP\n",
                                    "D=M\n")
    

    def __write_1_args_default_arithmetic(self, operator: str) -> None:
        """
        Hackアセンブリ言語にデフォルトである、1変数関数を出力ファイルに書き込む
        """
        self.__pop()
        self.__asm_commands.append(f"D={operator}D\n")
        self.__push()
        self.__write_asm_command()


    def __write_2_args_default_arithmetic(self, operator: str) -> None:
        """
        Hackアセンブリ言語にデフォルトである、2変数関数を出力ファイルに書き込む
        """
        self.__pop()
        self.__asm_commands.append("@R13\n",
                                    "M=D\n")
        self.__pop()
        self.__asm_commands.append("@R13\n",
                                    f"D=D{operator}M\n")
        self.__push()
        self.__write_asm_command()
    

    def __write_2_args_arithmetic(self, jump_command: str) -> None:
        symbol_true: str = "TRUE" + str(self.__symbol_index)
        symbol_end: str = "END" + str(self.__symbol_index)

        self.__pop()
        self.__asm_commands.append("@R13\n",
                                    "M=D\n")
        self.__pop()
        self.__asm_commands.append("D=D-M\n",
                                    f"@{symbol_true}\n",
                                    f"D;{jump_command}\n",
                                    "D=0\n")
        self.__push()
        self.__asm_commands.append(f"@{symbol_end}\n",
                                    "0;JMP\n",
                                    f"({symbol_true})\n",
                                    "D=-1\n")
        self.__push()
        self.__asm_commands.append(f"({symbol_end})\n")
        self.__write_asm_command()

        self.__symbol_index += 1


    def setFileName(self, filename: str) -> None:
        self.__file_name = filename


    # TODO: 2変数の演算など同じところは関数にまとめる
    def writeArithmetic(self, command: str) -> None:
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


    def writePushPop(self, command: str, segment: str, index: int) -> None:
        if segment == "local":
            pass
        elif segment == "argument":
            pass
        elif segment == "this":
            pass
        elif segment == "that":
            pass
        elif segment == "pointer":
            pass
        elif segment == "temp":
            pass
        elif segment == "constant":
            pass
        elif segment == "static":
            pass