from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable
from CommandType import CommandType

from io import TextIOWrapper
import sys

class Assembler:
    def __init__(self, path_to_asm_file: str, output_file_name: str) -> None:
        """
        path_to_asm_fileはアセンブルする.asmファイルまでのパス。
        output_file_nameは出力される.hackファイルの名前。
        """
        self.__output_file: TextIOWrapper = open(file=output_file_name, mode="w") # 出力されるファイル
        self.__parser: Parser = Parser(path_to_asm_file=path_to_asm_file)
        self.__code: Code = Code()
        self.__symbol_table: SymbolTable = SymbolTable()
        self.__command_type: CommandType = CommandType()
        self.__rom_address_index: int = 0 # ROMのアドレスのインデックス。L命令をROMのアドレスに置き換えるときに使われる
        self.__ram_address_index: int = 16 # RAMのアドレスのインデックス。変数をRAMのアドレスに置き換えるときに使われる。
    
    def __del__(self) -> None:
        self.__output_file.close()
    
    def __assemble_a_command(self) -> str:
        """
        A命令をアセンブルした16bitのバイナリ文字列を返す。
        """
        value: str = self.__parser.symbol()
        value_str_decimal: str = ""
        if not str.isdecimal(value):
            if not self.__symbol_table.contains(symbol=value):
                self.__symbol_table.addEntry(symbol=value, address=self.__ram_address_index)
                self.__ram_address_index += 1
            value_str_decimal = self.__symbol_table.getAddress(symbol=value)
        else:
            value_str_decimal = value
        value_int: int = int(value_str_decimal)
        value_str_binary: str = format(value_int, "015b") # 15桁の2進数文字列
        
        return "0" + value_str_binary

    def __assemble_c_command(self) -> str:
        """
        C命令をアセンブルした16bitのバイナリ文字列を返す。
        """
        comp = self.__parser.comp()
        dest = self.__parser.dest()
        jump = self.__parser.jump()

        comp_binary: str = self.__code.comp(mnemonic=comp)
        dest_binary: str = self.__code.dest(mnemonic=dest)
        jump_binary: str = self.__code.jump(mnemonic=jump)

        return "111" + comp_binary + dest_binary + jump_binary

    def assemble(self) -> None:
        # L命令をそのL命令に続く命令のアドレスに対応づけていく
        while self.__parser.hasMoreCommands():
            self.__parser.advance()
            current_command_type: str = self.__parser.commandType()
            if not (current_command_type == self.__command_type.l):
                self.__rom_address_index += 1
                continue
            symbol: str = self.__parser.symbol()
            self.__symbol_table.addEntry(symbol=symbol, address=self.__rom_address_index)

        self.__parser.returnToBeginning()

        # 命令をバイナリに変換していく
        while self.__parser.hasMoreCommands():
            self.__parser.advance()
            binary_command: str = ""
            current_command_type: str = self.__parser.commandType()
            if current_command_type == self.__command_type.a:
                binary_command = self.__assemble_a_command()
            elif current_command_type == self.__command_type.c:
                binary_command = self.__assemble_c_command()
            else:
                continue
            self.__output_file.write(binary_command + "\n")

if __name__ == "__main__":
    path_to_asm_file = sys.argv[1] # 入力ファイルまでのパス
    output_file_name = sys.argv[2] # 出力ファイルの名前

    assembler: Assembler = Assembler(path_to_asm_file=path_to_asm_file, output_file_name=output_file_name)
    assembler.assemble()