from automata import AFD
from analisis import Lexico
from operaciones import *
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import re
import ast
from bs4 import BeautifulSoup
from graphviz import Digraph

def extraer_expresiones(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    expresiones = []
    for p in soup.find_all('p'):
        texto = p.get_text()
        match = re.search(r'([\d\.\+\-\*/\^\(\)% ]+)=', texto)
        if match:
            expresiones.append(match.group(1).strip())
    return expresiones

def parsear_expresion(expr):
    expr = expr.replace('^', '**')  # Python usa ** para potencia
    try:
        return ast.parse(expr, mode='eval').body
    except Exception as e:
        print(f"Error al parsear: {expr} → {e}")
        return None

def hijos_nodo(node):
    if isinstance(node, ast.BinOp):
        return [node.left, node.right]
    elif isinstance(node, ast.UnaryOp):
        return [node.operand]
    elif isinstance(node, ast.Call):
        return node.args
    return []

def generar_diagramas(html_path):
    expresiones = extraer_expresiones(html_path)
    for i, expr in enumerate(expresiones, start=1):
        ast_root = parsear_expresion(expr)
        dot = Digraph(comment=f'Operacion {i}')
        dibujar_arbol_ast(ast_root, dot)
        dot.render(f'arbol_operacion_{i}', format='png', cleanup=True)
        print(f'Arbol generado para Operación {i}: {expr}')

def operador(op):
    return {
        ast.Add: 'Suma',
        ast.Sub: 'Resta',
        ast.Mult: 'Multiplicación',
        ast.Div: 'División',
        ast.Pow: 'Potencia',
        ast.Mod: 'Módulo',
        ast.USub: 'Negativo'
    }.get(type(op), type(op).__name__)

def tipo_nodo(node):
    if isinstance(node, ast.BinOp):
        return operador(node.op)
    elif isinstance(node, ast.UnaryOp):
        return operador(node.op)
    elif isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.Constant):
        return str(node.value)
    elif isinstance(node, ast.Expr):
        return tipo_nodo(node.value)
    elif isinstance(node, ast.Call):
        return 'función'
    else:
        return type(node).__name__

def dibujar_arbol_ast(node, dot, parent=None):
    if node is None:
        return
    label = tipo_nodo(node)
    nodo_id = str(id(node))
    dot.node(nodo_id, label)
    if parent:
        dot.edge(parent, nodo_id)

    for hijo in hijos_nodo(node):
        dibujar_arbol_ast(hijo, dot, nodo_id)

def LeerArchivo(ruta: str) -> str:
    info = ""
    with open(ruta, "r", newline="") as f:
        info = f.read()

    return info[:-1]

def HayError(lexico: Lexico) -> bool:
    for token in lexico.tokens:
        if token[0] == "error":
            return True
    return False
    


def GenerarResultados(lexico: Lexico) -> None:

    operaciones = ObtenerOperaciones(lexico.tokens)
    resultados = CalcularOperaciones(lexico.tokens)

    if len(operaciones) != len(resultados):
        #Pensar en un error
        pass

    with open("Resultados.html", "w", newline="\n") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang='es'>\n")
        f.write("<head>\n")
        f.write("<meta charset='UTF-8'>\n")
        f.write("<title>Reporte de Resultados</title>\n")
        f.write("<style>\n")
        f.write("body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }\n")
        f.write("</style>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("<h4>Operaciones</h4>\n")

        for i in range(len(operaciones)):
            f.write("<div>\n")
            f.write(f"<p>Operacion Numero {i + 1}:</p>\n")
            f.write(f"<p>{operaciones[i]} = {resultados[i]}</p>\n")
            f.write("</div>\n")
        f.write("</body>\n")
    
    generar_diagramas('Resultados.html')


def GenerarReporteErrores(lexico: Lexico) -> None:
    nerror = 0
    with open("Errores.html", "w", newline="\n") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang='es'>\n")
        f.write("<head>\n")
        f.write("<meta charset='UTF-8'>\n")
        f.write("<title>Reporte de Errores</title>\n")
        f.write("<style>\n")
        f.write("body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }\n")
        f.write("table { border-collapse: collapse; width: 100%; background-color: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); }\n")
        f.write("caption { font-size: 1.5em; margin: 10px 0; font-weight: bold; color: #333; }\n")
        f.write("th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }\n")
        f.write("th { background-color: #6a0dad; color: white; }\n")
        f.write("table { border: 2px solid #6a0dad; }\n")
        f.write("tr:nth-child(even) { background-color: #f2f2f2; }\n")
        f.write("tr:hover { background-color: #e0e0e0; }\n")
        f.write("</style>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("<table>\n")
        f.write("<caption>Reporte de Errores</caption>\n")
        f.write("<tr>\n")
        f.write("<th>No.</th>\n")
        f.write("<th>Lexema</th>\n")
        f.write("<th>Tipo</th>\n")
        f.write("<th>Caracter</th>\n")
        f.write("<th>Fila</th>\n")
        f.write("</tr>\n")
        for token in lexico.tokens:
            if token[0] == "error":
                nerror += 1
                f.write("<tr>\n")
                f.write(f"<td>{nerror}</td>\n")
                f.write(f"<td>{token[1]}</td>\n")
                f.write(f"<td>{token[0]}</td>\n")
                f.write(f"<td>{token[2]}</td>\n")
                f.write(f"<td>{token[3]}</td>\n")
                f.write("</tr>\n")
        f.write("</table>\n")
        f.write("</body>\n")
        f.write("</html>\n")
    f.close()

# Función para abrir archivo
def abrir_archivo() -> None:
    global ruta_archivo
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ruta_archivo:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
            texto.delete("1.0", tk.END)
            texto.insert(tk.END, contenido)

# Función para guardar cambios
def guardar_archivo() -> None:
    global ruta_archivo
    if ruta_archivo == None:
        messagebox.showerror("Archivo", "Antes de guardar, debe de abrir un archivo para sobreescribir.")
        ruta_archivo = filedialog.askopenfilename(filetypes = [("Text files", "*.txt")])
    else:
        with open(ruta_archivo, "w", encoding="utf-8", newline="") as f:
            f.write(texto.get("1.0", tk.END))
        messagebox.showinfo("Guardado", "Cambios guardados correctamente.")

# Función para guardar como nuevo archivo
def guardar_como() -> None:
    nueva_ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if nueva_ruta:
        with open(nueva_ruta, "w", encoding="utf-8", newline="") as f:
            f.write(texto.get("1.0", tk.END))
        messagebox.showinfo("Guardado", "Archivo guardado como nuevo.")
        global ruta_archivo
        ruta_archivo = nueva_ruta

def manuales() -> None:
    try:
        os.startfile("Manual Técnico y de Usuario - Proyecto 2 LFYA.pdf")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el PDF:\n{e}")

def ayuda() -> None:
    global ruta_archivo
    ruta_archivo = "Datos.txt"
    with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
            texto.delete("1.0", tk.END)
            texto.insert(tk.END, contenido)

def analizar():
    global ruta_archivo
    error = False
    if ruta_archivo == None:
        guardar_como()
        if ruta_archivo == None:
            return
    info = LeerArchivo(ruta_archivo)

    digito = list("0123456789")
    OP = ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "POTENCIA", "RAIZ", "INVERSO", "MOD"]
    OPN = ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION"]
    OP2 = ["POTENCIA", "RAIZ", "MOD"]
    OP1 = ["INVERSO"]
        
    automata = AFD()
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

    l = Lexico(automata, tabla)
    l.ProcesarEntrada(info)
    tokens = l.tokens
    for token in tokens:
        if token[0] == "error":
            error = True
            break

    if error:
        messagebox.showerror("Ejecución","Se encontraron errores en el archivo de entrada, se registraran las operaciones validas en 'Resultados.html'.\nArchivo 'Errores.html' generado.")
        GenerarReporteErrores(l)
    else:
        messagebox.showinfo("Ejecución","No se encontraron errores en el archivo de entrada. \nArchivo 'Resultados.html generado.")
    GenerarResultados(l)

if __name__ == "__main__":

    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Editor de Archivos")
    ventana.geometry("943x630")
    ventana.resizable(False, False)
    ventana.configure(bg = "#ADADAD")

    # Variable para guardar la ruta del archivo actual
    ruta_archivo = None

    # Frame superior con botones principales
    frame_superior = tk.Frame(ventana)
    frame_superior.configure(bg = "#ADADAD")
    frame_superior.pack(side="top", fill="x", padx=15, pady=5)

    btn_Open = tk.Button(frame_superior, text="Abrir", command=abrir_archivo, height = 3, width = 20, font = ("Comic Sans MS", 10), bg = "#BDBDBD", activebackground = "#969696", relief = "ridge", bd = 6)
    btn_Open.pack(side="left", padx=4)

    btn_Save = tk.Button(frame_superior, text="Guardar", command=guardar_archivo, height = 3, width = 20, font = ("Comic Sans MS", 10), bg = "#BDBDBD", activebackground = "#969696", relief = "ridge", bd = 6)
    btn_Save.pack(side="left", padx=4)

    btn_SaveAs = tk.Button(frame_superior, text="Guardar Como", command=guardar_como, height = 3, width = 20, font = ("Comic Sans MS", 10), bg = "#BDBDBD", activebackground = "#969696", relief = "ridge", bd = 6)
    btn_SaveAs.pack(side="left", padx=4)

    btn_Analyze = tk.Button(frame_superior, text="Analizar", command = analizar, height = 3, width = 20, font = ("Comic Sans MS", 10), bg = "#BDBDBD", activebackground = "#969696", relief = "ridge", bd = 6)
    btn_Analyze.pack(side="left", padx=4)

    # Área de texto editable
    frame_texto = tk.Frame(ventana)
    frame_texto.configure(bg = "#ADADAD")
    frame_texto.pack(side = "left", padx= 10, pady= 10)
    scroll_vertical = tk.Scrollbar(frame_texto)
    scroll_vertical.pack(side= "right", fill= "y")
    texto = tk.Text(frame_texto, wrap= "word", font= ("Arial", 12), height= 30, width= 81, yscrollcommand= scroll_vertical.set, fg = "#000000")
    texto.pack(side = "left")
    texto.configure(bg = "#F2F2F2")
    scroll_vertical.config(command = texto.yview)

    # Frame lateral derecho con botones sin funcionalidad por ahora
    frame_lateral = tk.Frame(ventana)
    frame_lateral.configure(bg = "#ADADAD")
    frame_lateral.pack(side="right", fill="y", padx=10, pady=10)

    btn_UserManual = tk.Button(frame_lateral, text="Manual de Usuario", command = manuales, height = 3, width = 20, font = ("Comic Sans MS", 10), bg = "#BDBDBD", activebackground = "#969696", relief = "ridge", bd = 6)
    btn_UserManual.pack(pady = 5)

    btn_TecnicManual = tk.Button(frame_lateral, text="Manual Técnico", command = manuales, height = 3, width = 20, font = ("Comic Sans MS", 10), bg = "#BDBDBD", activebackground = "#969696", relief = "ridge", bd = 6)
    btn_TecnicManual.pack(pady = 5)

    btn_Help = tk.Button(frame_lateral, text="Ayuda", command = ayuda, height = 3, width = 20, font = ("Comic Sans MS", 10), bg = "#BDBDBD", activebackground = "#969696", relief = "ridge", bd = 6)
    btn_Help.pack(pady = 5)

    # Ejecutar la interfaz
    ventana.mainloop()

