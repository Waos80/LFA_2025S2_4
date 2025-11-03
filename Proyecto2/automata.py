from collections import defaultdict
from estructuras import *

class AP:
    def __init__(self) -> None:
        self.estados: dict = defaultdict(tuple[list, bool])
        self.pila: Pila = Pila()
        
    def crearEstado(self, aceptacion = False) -> None:
        id_estado = len(self.estados)
        self.estados[id_estado] = ([], aceptacion)

    def crearEstados(self, estados = list[bool]) -> None:
        for aceptacion in estados:
            self.crearEstado(aceptacion)

    def crearTransicion(self, estado: int, x: str, s: str, q: int, y: str) -> None:
        if self.estados.get(estado) == None:
            return # Error no existe estado
        
        self.estados[estado][0].append((estado, x, s, q, y))

    def crearTransicion(self, estado: int, x: list[str], s: str, q: int, y: str) -> None:
        if self.estados.get(estado) == None:
            return # Error no existe estado
        
        if x == "":
            self.estados[estado][0].append((estado, x, s, q, y))
            return

        for i in x:
            self.estados[estado][0].append((estado, i, s, q, y))

    def crearTransiciones(self, estados: dict[int, list[tuple[list[str], str, int, str]]]) -> None:
        for estado in estados.keys():
            transiciones = estados[estado]
            for transicion in transiciones: 
                self.crearTransicion(estado, transicion[0], transicion[1], transicion[2], transicion[3])
        
    def evaluar(self, entrada: str) -> tuple[bool, str, int]:
        copia_entrada = entrada
        if len(self.estados) <= 0:
            return # Error: No hay estados
        
        estado = self.estados[0]
        cc = 0

        while True:
            hay_transicion = False

            if len(entrada) <= 0 and estado[1] and len(self.pila.pila) <= 0:
                return (True, "", cc)
            
            aux: dict = {transicion[1]: idx for idx, transicion in enumerate(estado[0])}
            
            indice_transicion = aux.get(entrada[0] if len(entrada) > 0 else entrada)
            if indice_transicion != None:
                transicion = estado[0][indice_transicion]
                hay_transicion = True

                if transicion[1] != "":
                    cc += 1

                if transicion[2] != "":
                    if self.pila.top() == transicion[2]:
                        self.pila.pop()
                    else:
                        error = ""
                        if len(copia_entrada) > 0 and cc <= 0:
                            error += copia_entrada[0]
                        elif len(copia_entrada) > 0 and cc > 0:
                            error += copia_entrada[cc - 1]
                        return (False, error, cc)
                
                if len(entrada) > 0 and transicion[1] != "":
                    entrada = entrada[1:]

                if transicion[4] != "":
                    self.pila.agregar(transicion[4])

                estado = self.estados[transicion[3]]

            elif aux.get("") != None:
                transicion = estado[0][aux.get("")]
                hay_transicion = True

                if transicion[2] != "":
                    if self.pila.top() == transicion[2]:
                        self.pila.pop()
                    else:
                        error = ""
                        if len(copia_entrada) > 0 and cc <= 0:
                            error += copia_entrada[0]
                        elif len(copia_entrada) > 0 and cc > 0:
                            error += copia_entrada[cc - 1]
                        return (False, entrada, cc)
                
                if transicion[4] != "":
                    self.pila.agregar(transicion[4])

                estado = self.estados[transicion[3]]

            if not hay_transicion:
                for item in aux.items():
                    l = len(item[0])
                    if l > 1 and entrada[0:l] == item[0]:
                        transicion = estado[0][item[1]]

                        hay_transicion = True
                        entrada = entrada[l:]

                        if transicion[2] != "":
                            if self.pila.top() == transicion[2]:
                                self.pila.pop()
                            else:
                                error = ""
                                if len(copia_entrada) > 0 and cc <= 0:
                                    error += copia_entrada[0]
                                elif len(copia_entrada) > 0 and cc > 0:
                                    error += copia_entrada[cc - 1]
                                return (False, error, cc)

                        if transicion[4] != "":
                            self.pila.agregar(transicion[4])

                        estado = self.estados[transicion[3]]
                        cc += l
                        break

        
            if not hay_transicion:
                error = ""
                if len(copia_entrada) > 0 and cc <= 0:
                    error += copia_entrada[0]
                elif len(copia_entrada) > 0 and cc > 0:
                    error += copia_entrada[cc]
                return (False, error, cc + 1)
            
    
        
    
class AFD(AP):
    def __init__(self) -> None:
        super().__init__()
    
    def crearTransicion(self, estado: int, x: list[str], q: int) -> None:
        if self.estados.get(estado) == None:
            return # Error no existe estado
        
        if x == "":
            self.estados[estado][0].append((estado, x, "", q, ""))
            
            return

        for i in x:
            self.estados[estado][0].append((estado, i, "", q, ""))

    def crearTransiciones(self, estados: dict[int, list[tuple[list[str], int]]]) -> None:
        for estado in estados.keys():
            transiciones = estados[estado]
            for transicion in transiciones: 
                self.crearTransicion(estado, transicion[0], transicion[1])

    def evaluar(self, entrada):
        return self.evaluar(entrada)
    
    def evaluarPorTokens(self, entrada: str, tabla: dict[int, str]) -> list:
        tokens: list = []
        copia_entrada = entrada
        if len(self.estados) <= 0:
            return # Error: No hay estados
        
        estado = self.estados[0]
        ultimo_estado = 0
        linea = 1
        caracter_linea = 0
        inicio = 0
        fin = 0

        while len(entrada) > 0:
            hay_transicion = False


            aux: dict = {transicion[1]: idx for idx, transicion in enumerate(estado[0])}
            indice_transicion = aux.get(entrada[0] if len(entrada) > 0 else entrada)

            if estado[1] and indice_transicion == None:
                tokens.append((tabla[ultimo_estado], copia_entrada[inicio:fin], caracter_linea, linea))

                inicio = fin
                ultimo_estado = 0
                estado = self.estados[0]

                aux: dict = {transicion[1]: idx for idx, transicion in enumerate(estado[0])}
                indice_transicion = aux.get(entrada[0] if len(entrada) > 0 else entrada)
            
            if entrada[0] == "\n" or entrada[0] == "\r":
                linea += 1
                entrada = entrada[1:]
                inicio += 1
                fin += 1
                caracter_linea = 0
                continue
            
            if entrada[0] == " ":
                entrada = entrada[1:]
                inicio += 1
                fin += 1
                caracter_linea += 1
                continue

            if indice_transicion != None:
                transicion = estado[0][indice_transicion]
                hay_transicion = True

                if transicion[1] != "":
                    fin += 1
                    caracter_linea += 1
                
                if len(entrada) > 0 and transicion[1] != "":
                    entrada = entrada[1:]

                ultimo_estado = transicion[3]
                estado = self.estados[transicion[3]]
                

            elif aux.get("") != None:
                transicion = estado[0][aux.get("")]
                hay_transicion = True

                ultimo_estado = transicion[3]
                estado = self.estados[transicion[3]]

            if not hay_transicion:
                for item in aux.items():
                    l = len(item[0])
                    if l > 1 and entrada[0:l] == item[0]:
                        transicion = estado[0][item[1]]

                        hay_transicion = True
                        entrada = entrada[l:]

                        ultimo_estado = transicion[3]
                        estado = self.estados[transicion[3]]
                        fin += l
                        caracter_linea += l
                        break

            if not hay_transicion:
                error = ""
                error += copia_entrada[fin]

                tokens.append(("error", error, caracter_linea, linea))
                fin += 1
                caracter_linea += 1
                inicio = fin
                ultimo_estado = 0
                
                estado = self.estados[0]
                entrada = entrada[1:]

        aux: dict = {transicion[1]: idx for idx, transicion in enumerate(estado[0])}
        indice_transicion = aux.get(entrada[0] if len(entrada) > 0 else entrada)
        if estado[1] and indice_transicion == None:
            tokens.append((tabla[ultimo_estado], copia_entrada[inicio:fin], fin, linea))

            inicio = fin
            ultimo_estado = 0
            estado = self.estados[0]

            aux: dict = {transicion[1]: idx for idx, transicion in enumerate(estado[0])}
            indice_transicion = aux.get(entrada[0] if len(entrada) > 0 else entrada)

        elif not estado[1] and len(tokens) <= 0:
            error = ""
            error += copia_entrada[fin - 1]

            tokens.append(("error", error, caracter_linea, linea))

        

        return tokens