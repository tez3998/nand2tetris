import re
import sys
from io import TextIOWrapper

class CodeWriter:
    class AssemblyCommands:
        """
        一連のアセンブリ命令を保持するクラス
        """
        def __init__(self) -> None:
            self.__commands: str = ""


        def append(self, *commands: str):
            SYMBOL_PATTERN: str = "^\(.*\)$"
            INDENT: str = "    "

            for cmd in commands:
                if not re.match(pattern=SYMBOL_PATTERN, string=cmd): # 可読性向上のためのインデント
                    cmd = INDENT + cmd
                self.__commands += cmd + "\n"


        def get_commands(self) -> str:
            return self.__commands


        def clear(self) -> None:
            self.__commands = ""


    #
    # パブリックメソッド
    #
    def __init__(self, output_file_name: str) -> None:
        self.__output_file: TextIOWrapper = open(file=output_file_name, mode="w") # 出力されるアセンブリファイル
        self.__current_parsing_file_name: str = "" # 現在パースされているファイルの名前
        self.__current_function_name: str = "" # 現在パースされている関数の名前
        self.__asm_commands: CodeWriter.AssemblyCommands = CodeWriter.AssemblyCommands() # 書き込み前の一連のアセンブリコマンド
        self.__symbol_index: int = 0
        self.__return_address_index: int = 0


    def set_file_name(self, file_name: str) -> None:
        self.__current_parsing_file_name = file_name


    def write_init(self) -> None:
        STACK_SEGMENT_ADDRESS: str = 256
        self.__asm_commands.append(f"@{STACK_SEGMENT_ADDRESS}",
                                    "D=A",
                                    "@SP",
                                    "M=D")


    def write_arithmetic(self, command: str) -> None:
        if command == "add":
            self.__write_binary_function(operator="+")
        elif command == "sub":
            self.__write_binary_function(operator="-")
        elif command == "neg":
            self.__write_unary_function(operator="-")
        elif command == "eq":
            self.__write_comparison_operation(jump_command="JEQ")
        elif command == "gt":
            self.__write_comparison_operation(jump_command="JGT")
        elif command == "lt":
            self.__write_comparison_operation(jump_command="JLT")
        elif command == "and":
            self.__write_binary_function(operator="&")
        elif command == "or":
            self.__write_binary_function(operator="|")
        elif command == "not":
            self.__write_unary_function(operator="!")
        else:
            print(f"コマンド{command}は存在しません\n")
            sys.exit(1)


    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        POINTER_BASE_ADDRESS: int = 3
        TEMP_BASE_ADDRESS: int = 5

        if command == "push":
            if segment == "local":
                self.__indirect_push_to_stack(symbol="LCL", index=index)
            elif segment == "argument":
                self.__indirect_push_to_stack(symbol="ARG", index=index)
            elif segment == "this":
                self.__indirect_push_to_stack(symbol="THIS", index=index)
            elif segment == "that":
                self.__indirect_push_to_stack(symbol="THAT", index=index)
            elif segment == "pointer":
                address: int = POINTER_BASE_ADDRESS + index
                self.__asm_commands.append(f"@{str(address)}",
                                            "D=M")
                self.__push_to_stack()
            elif segment == "temp":
                address: int = TEMP_BASE_ADDRESS + index
                self.__asm_commands.append(f"@{str(address)}",
                                            "D=M")
                self.__push_to_stack()
            elif segment == "constant":
                self.__asm_commands.append(f"@{str(index)}",
                                            "D=A")
                self.__push_to_stack()
            elif segment == "static":
                self.__asm_commands.append(f"@{self.__current_parsing_file_name}.{str(index)}",
                                            "D=M")
                self.__push_to_stack()
            else:
                print(f"{segment}は存在しないセグメントです\n")
                sys.exit(1)
        elif command == "pop":
            if segment == "local":
                self.__indirect_pop_from_stack(symbol="LCL", index=index)
            elif segment == "argument":
                self.__indirect_pop_from_stack(symbol="ARG", index=index)
            elif segment == "this":
                self.__indirect_pop_from_stack(symbol="THIS", index=index)
            elif segment == "that":
                self.__indirect_pop_from_stack(symbol="THAT", index=index)
            elif segment == "pointer":
                address: int = POINTER_BASE_ADDRESS + index
                self.__pop_from_stack()
                self.__asm_commands.append(f"@{str(address)}",
                                            "M=D")
            elif segment == "temp":
                address: int = TEMP_BASE_ADDRESS + index
                self.__pop_from_stack()
                self.__asm_commands.append(f"@{str(address)}",
                                            "M=D")
            elif segment == "constant":
                print(f"セグメント{segment}に対する{command}はできません")
                sys.exit(1)
            elif segment == "static":
                self.__pop_from_stack()
                self.__asm_commands.append(f"@{self.__current_parsing_file_name}.{index}",
                                            "M=D")
            else:
                print(f"セグメント{segment}は存在しません\n")
                sys.exit(1)
        else:
            print(f"コマンド{command}は存在しません")
            sys.exit(1)
        self.__write()


    def write_label(self, label: str) -> None:
        self.__asm_commands.append(f"({self.__current_function_name}${label})")
        self.__write()


    def write_goto(self, label: str) -> None:
        self.__asm_commands.append(f"@{label}",
                                    "0;JMP")
        self.__write()


    def write_if(self, label: str) -> None:
        self.__pop_from_stack()
        self.__asm_commands.append(f"@{label}",
                                    "D;JEQ")
        self.__write()


    def write_call(self, function_name: str, num_args) -> None:
        RETURN_ADDRESS: str = f"RETURN_ADDRESS_{str(self.__return_address_index)}"
        self.__return_address_index += 1

        SYMBOLS: list[str] = [RETURN_ADDRESS, "LCL", "ARG", "THIS", "THAT"]
        NUM_SAVED_STATE: int = len(SYMBOLS)

        # 呼び出し側の状態の保存
        for symbol in SYMBOLS:
            self.__asm_commands.append(f"{symbol}",
                                        "D=M")
            self.__push_to_stack()
        # ARGのセット
        self.__asm_commands.append("@SP",
                                    "D=M")
        for _ in range(num_args + NUM_SAVED_STATE):
            self.__asm_commands.append("D=D-1")
        self.__asm_commands.append("@ARG",
                                    "M=D")
        # LCLのセット
        self.__asm_commands.append("@SP",
                                    "D=M",
                                    "@LCL",
                                    "M=D")
        # 関数呼び出し
        self.__asm_commands.append(f"@{function_name}",
                                    "0;JMP")
        # リターンアドレスラベルの記述
        self.__asm_commands.append(f"({RETURN_ADDRESS})")
        self.__write()


    def write_return(self) -> None:
        SYMBOLS: list[str] = ["THAT", "THIS", "ARG", "LCL"]
        NUM_SAVED_STATE: int = 5

        # LCLのセット
        self.__asm_commands.append("@LCL",
                                    "D=M",
                                    "@R13",
                                    "M=D")
        # リターンアドレスの退避
        for _ in range(NUM_SAVED_STATE):
            self.__asm_commands.append("D=D-1")
        self.__asm_commands.append("@R14",
                                    "M=D")
        # 戻り値のセット
        self.__pop_from_stack()
        self.__asm_commands.append("@ARG",
                                    "M=D")
        # スタックポインタのセット
        self.__asm_commands.append("D=D+1",
                                    "@SP",
                                    "M=D")
        # 保存していた呼び出し側の状態の復元
        self.__asm_commands.append("@LCL",
                                    "D=M")
        for symbol in SYMBOLS:
            self.__asm_commands.append("D=D-1",
                                        f"@{symbol}",
                                        "M=D")
        # リターン
        self.__asm_commands.append("@R13",
                                    "A=M",
                                    "0;JMP")
        self.__write()


    def write_function(self, function_name: str, num_locals: int) -> None:
        self.__asm_commands.append(f"({function_name})")
        for _ in range(num_locals):
            self.__asm_commands.append("D=0")
            self.__push_to_stack()
        self.__write()


    def write_infinite_loop(self) -> None:
        """
        アセンブリの終了を示す無限ループをファイルに書き込む。
        このメソッドは、一度だけ呼ばれることを想定している
        """
        self.__asm_commands.append("(END)",
                                    "@END",
                                    "0;JMP")
        self.__write()


    def close(self) -> None:
        self.__output_file.close()
    

    #
    # プライベートメソッド
    #
    def __write(self) -> None:
        self.__output_file.write(self.__asm_commands.get_commands())
        self.__asm_commands.clear()


    def __increase_sp(self) -> None:
        """
        スタックポインタを1だけ増加させる。
        ファイルへの書き込みは行わない
        """
        self.__asm_commands.append("@SP",
                                    "M=M+1")
    

    def __decrease_sp(self) -> None:
        """
        スタックポインタを1だけ減少させる。
        ファイルへの書き込みは行わない
        """
        self.__asm_commands.append("@SP",
                                    "M=M-1")
    

    def __push_to_stack(self) -> None:
        """
        レジスタDの値をスタックの最上部にセットする。
        ファイルへの書き込みは行わない
        """
        self.__asm_commands.append("@SP",
                                    "A=M",
                                    "M=D")
        self.__increase_sp()
    

    def __pop_from_stack(self) -> None:
        """
        スタックの最上部から値を取り出し、レジスタDにその値をセットする。
        ファイルへの書き込みは行わない
        """
        self.__decrease_sp()
        self.__asm_commands.append("@SP",
                                    "A=M",
                                    "D=M")
    

    def __write_unary_function(self, operator: str) -> None:
        """
        Hackアセンブリにデフォルトである1変数関数をファイルに記述する
        """
        self.__pop_from_stack()
        self.__asm_commands.append(f"D={operator}D")
        self.__push_to_stack()
        self.__write()


    def __write_binary_function(self, operator: str) -> None:
        """
        Hackアセンブリにデフォルトである2変数関数をファイルに記述する
        """
        self.__pop_from_stack()
        self.__asm_commands.append("@R13",
                                    "M=D")
        self.__pop_from_stack()
        self.__asm_commands.append("@R13",
                                    f"D=D{operator}M")
        self.__push_to_stack()
        self.__write()
    

    def __write_comparison_operation(self, jump_command: str) -> None:
        """
        比較演算をファイルに記述する
        """
        SYMBOL_TRUE: str = f"COMP_TRUE_{str(self.__symbol_index)}"
        SYMBOL_END: str = f"COMP_END_{str(self.__symbol_index)}"
        self.__symbol_index += 1

        self.__pop_from_stack()
        self.__asm_commands.append("@R13",
                                    "M=D")
        self.__pop_from_stack()
        self.__asm_commands.append("@R13",
                                    "D=D-M",
                                    f"@{SYMBOL_TRUE}",
                                    f"D;{jump_command}",
                                    "D=0")
        self.__push_to_stack()
        self.__asm_commands.append(f"@{SYMBOL_END}",
                                    "0;JMP",
                                    f"({SYMBOL_TRUE})",
                                    "D=-1"),
        self.__push_to_stack()
        self.__asm_commands.append(f"({SYMBOL_END})")
        self.__write()
    

    def __indirect_push_to_stack(self, symbol: str, index: int) -> None:
        """
        LCLやARG、THIS、THATを使った間接的な参照により、値をスタックの最上部にセットする。
        ファイルへの書き込みは行わない
        """
        self.__asm_commands.append(f"@{symbol}",
                                    "D=M",
                                    f"{str(index)}",
                                    "A=D+A",
                                    "D=M")
        self.__push_to_stack()
    

    def __indirect_pop_from_stack(self, symbol: str, index: int) -> None:
        """
        スタックの最上部の値をLCLやARG、THIS、THATを使った間接的な参照によりセットする。
        ファイルへの書き込みは行わない
        """
        self.__pop_from_stack()
        self.__asm_commands.append("@R13",
                                    "M=D", # スタックから取り出してきた値をR13に退避
                                    f"@{symbol}",
                                    "D=M",
                                    f"@{str(index)}",
                                    "D=D+A",
                                    "@R14", # 操作対象のアドレスをR14に退避
                                    "M=D",
                                    "@R13",
                                    "D=M",
                                    "@R14",
                                    "A=M",
                                    "M=D")