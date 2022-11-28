from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable
from CommandType import CommandType

from io import TextIOWrapper
import sys

class Assembler:
    def __init__(self, path_to_asm_file: str, output_file_name: str) -> None:
        self.__output_file: TextIOWrapper = open(file=output_file_name, mode="w")
        self.__parser: Parser = Parser(path_to_asm_file=path_to_asm_file)
        self.__code: Code = Code()
        #self.__symbol_table: SymbolTable = SymbolTable()
        self.__command_type: CommandType = CommandType()
    
    def __del__(self) -> None:
        self.__output_file.close()
    
    def __assemble_a_command(self) -> str:
        value_str_decimal: str = self.__parser.symbol()
        value_int: int = int(value_str_decimal)
        value_str_binary: str = format(value_int, "015b") # 15桁の2進数文字列
        
        return "0" + value_str_binary

    def __assemble_c_command(self) -> str:
        comp = self.__parser.comp()
        dest = self.__parser.dest()
        jump = self.__parser.jump()

        comp_binary: str = self.__code.comp(mnemonic=comp)
        dest_binary: str = self.__code.dest(mnemonic=dest)
        jump_binary: str = self.__code.jump(mnemonic=jump)

        return "111" + comp_binary + dest_binary + jump_binary

    def assemble(self) -> None:
        while self.__parser.hasMoreCommands():
            self.__parser.advance()
            binary_command: str = ""
            current_command_type: str = self.__parser.commandType()
            if current_command_type == self.__command_type.a:
                binary_command = self.__assemble_a_command()
            elif current_command_type == self.__command_type.c:
                binary_command = self.__assemble_c_command()
            self.__output_file.write(binary_command + "\n")

if __name__ == "__main__":
    path_to_asm_file = sys.argv[1] # 入力ファイルまでのパス
    output_file_name = sys.argv[2] # 出力ファイルの名前

    assembler: Assembler = Assembler(path_to_asm_file=path_to_asm_file, output_file_name=output_file_name)
    assembler.assemble()