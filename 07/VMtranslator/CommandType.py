class CommandType:
    def __init__(self) -> None:
        self.c_arithmetic: str = "C_ARITHMETIC"
        self.c_push: str = "C_PUSH"
        self.c_pop: str = "C_POP"
        self.c_label: str = "C_LABEL" # 以下、この章では不要
        self.c_goto: str = "C_GOTO"
        self.c_if: str = "C_IF"
        self.c_function: str = "C_FUNCTION"
        self.c_return: str = "C_RETURN"
        self.c_call: str = "C_CALL"