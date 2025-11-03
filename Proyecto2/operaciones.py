def SepararPorOperacion(tokens: list) -> list[list]:
    tokens_operaciones = []
    tokens_operacion = []

    operacion_valida = True

    nivel = 0

    tmp: list = tokens

    i = 0
    for token in tmp:
        es_nueva_operacion: bool = token[0] == "aopn" or token[0] == "aop2" or token[0] == "aop1"

        if token[0] == "error":
            operacion_valida = False
            tokens_operacion.clear()

        if es_nueva_operacion:
            nivel += 1
            tokens_operacion.append(token)

        if token[0] == "numero":
            tokens_operacion.append(token)

        if token[0] == "co":
            nivel -= 1 
            tokens_operacion.append(token)
            if nivel <= 0:
                if operacion_valida:
                    tokens_operaciones.append(tokens_operacion.copy())
                tokens_operacion.clear()
                operacion_valida = True

        tmp = tmp[1:]
        i += 1

    return tokens_operaciones


def TokensAOperacion(tokens: list) -> str:
    operacion = ""
    operadores = {
        "SUMA": "+",
        "RESTA": "-",
        "MULTIPLICACION": "*",
        "DIVISION": "/",
        "POTENCIA": "^",
        "RAIZ": "√",
        "INVERSO": "1/",
        "MOD": "%"
    }

    niveles = 0
    primer_operando = True
    es_ultima_operacion = True
    ultima_operacion = 0
    cierre_ultima_operacion = 0

    for token in tokens:
            es_operacion: bool = token[0] == "aopn" or token[0] == "aop2" or token[0] == "aop1"
            if es_operacion:
                niveles += 1

    siguiente_izquierda = False
    while niveles > 0:
        izquierda = False
        es_ultima_operacion = True
        for i in range(len(tokens)):
            token = tokens[i]
            es_operacion: bool = token[0] == "aopn" or token[0] == "aop2" or token[0] == "aop1"

            if es_operacion:
                ultima_operacion = i

            if token[0] == "co" and es_ultima_operacion:
                cierre_ultima_operacion = i
                es_ultima_operacion = False

        if ultima_operacion > 0:
            izquierda = tokens[ultima_operacion - 1][0] == "numero"

        nivel = tokens[ultima_operacion:cierre_ultima_operacion + 1]

        operador = ""

        for token in nivel:
            es_operacion: bool = token[0] == "aopn" or token[0] == "aop2" or token[0] == "aop1"
            if es_operacion:
                tipo_operacion: str = token[1]
                tipo_operacion = tipo_operacion.replace(">", "")
                tipo_operacion = tipo_operacion[tipo_operacion.find(" ") + 1:]
                operador = operadores[tipo_operacion]

                if operador == "1/":
                    operacion = operador + operacion
                    break

            if token[0] == "numero":
                if primer_operando:
                    operacion += token[1] 
                    primer_operando = False
                else:
                    if siguiente_izquierda:
                        operacion = token[1] + " " + operador + " " + operacion
                    else:
                        operacion += " " + operador + " " + token[1]


        if niveles > 1:
            operacion = "(" + operacion
            operacion += ")"

        siguiente_izquierda = izquierda

        inferior = tokens[:ultima_operacion]
        superior = tokens[cierre_ultima_operacion + 1:]
        tokens = inferior + superior
        niveles -= 1

    return operacion

def CalcularOperacion(tokens: list) -> float:
    operacion = ""
    operadores = {
        "SUMA": "+",
        "RESTA": "-",
        "MULTIPLICACION": "*",
        "DIVISION": "/",
        "POTENCIA": "**",
        "RAIZ": "**1/",
        "INVERSO": "1/",
        "MOD": "%"
    }

    niveles = 0
    primer_operando = True
    es_ultima_operacion = True
    ultima_operacion = 0
    cierre_ultima_operacion = 0

    for token in tokens:
        es_operacion: bool = token[0] == "aopn" or token[0] == "aop2" or token[0] == "aop1"
        if es_operacion:
            niveles += 1

    siguiente_izquierda = False
    while niveles > 0:
        izquierda = False
        es_ultima_operacion = True
        for i in range(len(tokens)):
            token = tokens[i]
            es_operacion: bool = token[0] == "aopn" or token[0] == "aop2" or token[0] == "aop1"

            if es_operacion:
                ultima_operacion = i

            if token[0] == "co" and es_ultima_operacion:
                cierre_ultima_operacion = i
                es_ultima_operacion = False

        if ultima_operacion > 0:
            izquierda = tokens[ultima_operacion - 1][0] == "numero"

        nivel = tokens[ultima_operacion:cierre_ultima_operacion + 1]

        operador = ""

        for token in nivel:
            es_operacion: bool = token[0] == "aopn" or token[0] == "aop2" or token[0] == "aop1"
            if es_operacion:
                tipo_operacion: str = token[1]
                tipo_operacion = tipo_operacion.replace(">", "")
                tipo_operacion = tipo_operacion[tipo_operacion.find(" ") + 1:]
                operador = operadores[tipo_operacion]

                if operador == "1/":
                    operacion = operador + operacion
                    break


            if token[0] == "numero":
                if primer_operando:
                    if operador == "**1/":
                        operacion += "**(1/" + token[1] + ")"
                    else:
                        operacion += token[1] 
                    primer_operando = False
                else:
                    if operador == "**1/":
                        operacion = token[1] + operacion
                    else:
                        if siguiente_izquierda:
                            operacion = token[1] + " " + operador + " " + operacion
                        else:
                            operacion += " " + operador + " " + token[1]


        if niveles > 1:
            operacion = "(" + operacion
            operacion += ")"

        siguiente_izquierda = izquierda

        inferior = tokens[:ultima_operacion]
        superior = tokens[cierre_ultima_operacion + 1:]
        tokens = inferior + superior
        niveles -= 1

    return eval(operacion)

def ObtenerOperaciones(tokens: list) -> list[str]:
    ecuaciones = []
    operaciones = SepararPorOperacion(tokens.copy())
    for operacion in operaciones:
        ecuaciones.append(TokensAOperacion(operacion.copy()))

    return ecuaciones

def CalcularOperaciones(tokens: list) -> list[float]:
    resultados: list[float] = []
    operaciones = SepararPorOperacion(tokens.copy())
    for operacion in operaciones:
        resultados.append(CalcularOperacion(operacion.copy()))

    return resultados