class SymbolTable:
    def __init__(self) -> None:
        # シンボルテーブル
        self.__table: dict[str, int] = {}

    def addEntry(self, symbol: str, address: int) -> None:
        self.__table[symbol] = address

    def contains(self, symbol: str) -> bool:
        if self.__table.get(symbol) == None:
            return False
        else:
            return True

    def getAddress(self, symbol: str) -> int:
        return self.__table[symbol]