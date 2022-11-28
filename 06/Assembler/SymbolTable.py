class SymbolTable:
    def __init__(self) -> None:
        # シンボルテーブル
        self.__table: dict[str, int] = {
            "R0": 0, # 以下、仮想レジスタ
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SP": 0, # 以下、定義済みポインタ
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4, # 日本語版の書籍にはTHATはないが必要
            "SCREEN": 16384, # 以下、入出力ポインタ
            "KBD": 24576
        }

    def addEntry(self, symbol: str, address: int) -> None:
        self.__table[symbol] = address

    def contains(self, symbol: str) -> bool:
        if self.__table.get(symbol) == None:
            return False
        else:
            return True

    def getAddress(self, symbol: str) -> int:
        return self.__table[symbol]