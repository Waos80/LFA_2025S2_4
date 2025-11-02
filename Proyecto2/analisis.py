from collections import defaultdict
from automata import AFD

class Lexico:
    def __init__(self, automata: AFD, tabla: dict[int, str]):
        self.tokens: list[tuple[str, str, int, int]] = []
        self.automata: AFD = automata
        self.tabla: dict[int, str] = tabla

    def ProcesarEntrada(self, entrada: str) -> None:
        self.tokens = self.automata.evaluarPorTokens(entrada, self.tabla)
