class Code:
    def __init__(self) -> None:
        # destのニーモニックとビットの対応表
        self.__dest_table: dict[str, str] = {
            "null": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }

        # compのニーモニックとビットの対応表
        self.__comp_table: dict[str, str] = {
            "0": "0101010", # 以下、a=0のとき
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M": "1110000", # 以下、a=1のとき
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }

        # jumpのニーモニックとビットの対応表
        self.__jump_table: dict[str, str] = {
            "null": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }

    def dest(self, mnemonic: str) -> str:
        """
        mnemonicはdest部分のニーモニック。
        ニーモニックに対応した3bitのバイナリ文字列を返す。
        """
        return self.__dest_table[mnemonic]

    def comp(self, mnemonic: str) -> str:
        """
        mnemonicはcomp部分のニーモニック。
        ニーモニックに対応した7bitのバイナリ文字列を返す。
        """
        return self.__comp_table[mnemonic]

    def jump(self, mnemonic: str) -> str:
        """
        mnemonicはjump部分のニーモニック。
        ニーモニックに対応した3bitのバイナリ文字列を返す。
        """
        return self.__jump_table[mnemonic]