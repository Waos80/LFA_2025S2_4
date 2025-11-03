class Pila:
    def __init__(self) -> None:
        self.pila = []

    def agregar(self, valor) -> None:
        self.pila.append(valor)

    def top(self):
        if len(self.pila) <= 0:
            return None
        return self.pila[-1]

    def pop(self):
        if len(self.pila) <= 0:
            return None
        return self.pila.pop()
    
    def vacio(self) -> bool:
        return bool(len(self.pila))
    
    def __str__(self) -> str:
        return str(self.pila)