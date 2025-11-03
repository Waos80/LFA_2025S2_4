import analisis
from GUI import SepararPorOperacion

def LeerArchivo(ruta: str) -> str:
    info = ""
    with open(ruta, "r") as f:
        info = f.read()

    return info


if __name__ == "__main__":
    digito = list("0123456789")
    OP = ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "POTENCIA", "RAIZ", "INVERSO", "MOD"]
    OPN = ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION"]
    OP2 = ["POTENCIA", "RAIZ", "MOD"]
    OP1 = ["INVERSO"]
    
    automata = analisis.AFD()
    automata.crearEstados(
        [
         False, False, False, True, False,
         False, False, False, False, False,
         False, False, False, True, True,
         True, True, True, True, True,
        ]
    )

    automata.crearTransiciones({
        0: [
            (['<'], 1),
            (['-'], 2),
            (digito, 3),
        ],
        1: [
            (["Operacion= "], 4),
            (['/'], 5),
            (["Numero"], 6)
        ],
        2: [
            (digito, 3)
        ],
        3: [
            (digito, 3),
            (['.'], 7)
        ],
        4: [
            (OPN, 8),
            (OP2, 9),
            (OP1, 10)
        ],
        5: [
            (["Operacion"], 11),
            (["Numero"], 12)
        ],
        6: [
            (['>'], 13)
        ],
        7: [
            (digito, 14)
        ],
        8: [
            (['>'], 15)
        ]
        ,
        9: [
            (['>'], 16)
        ]
        ,
        10: [
            (['>'], 17)
        ],
        11: [
            (['>'], 18)
        ],
        12: [
            (['>'], 19)
        ],
        14: [
            (digito, 14)
        ]
    })

    info = LeerArchivo("./Entrada1.txt")
    tabla = {
        3: "numero",
        13: "an",
        14: "numero",
        15: "aopn",
        16: "aop2",
        17: "aop1",
        18: "co",
        19: "cn"
    }

    l = analisis.Lexico(automata, tabla)
    
    l.ProcesarEntrada(info)
    #print(l.tokens)
    operaciones = SepararPorOperacion(l.tokens)
    for operacion in operaciones:
        TokensAOperacion(operacion.copy())
        CalcularOperaciones(operacion.copy())
