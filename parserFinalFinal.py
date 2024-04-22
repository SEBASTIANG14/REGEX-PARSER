import re
from sys import path_importer_cache

tokens_array = []

queries = [
    """SELECT ANOMBRE
FROM ALUMNOS,INSCRITOS,CARRER;AS
WHERE ALUMNOS.A#=INSCRITOS.A# AND ALUMNOS.C#=CARRERAS.C#
AND INSCRITOS.SEMESTRE='2010I'
AND CARRERAS.CNOMBRE='ISC'
AND ALUMNOS.GENERACION='2010'""",

    """SELECT *
FROM PROFESORES
WHERE EDAD >'45' AND GRADO=MAE' OR GRADO='DOC'""", #error en este querie, no marca lo que triene que marcar

    """SELECT ANOMBRE
FROM ALUMNOS,INSCRITOS,
WHERE ALUMNOS.A#=INSCRITOS.A# AND
INSCRITOS.SEMESTRE='2010I'""",

    """SELECT ANOMBRE
FROM ALUMNOS
WHERE A# IN(SELECT A#
FROM INSCRITOS
WHERE P# IN (SELECT P#
FROM PROFESORES
WHERE GRADO='MAE'))

AND C# IN (SELECT C#
FROM
WHERE CNOMBRE='ISC')""",

    """SELECT ANOMBRE
FROM ALUMNOS A,INSCRITOS I,CARRERAS C
WHERE A.A#=I.A# AND A.C#=C.C#
AND I.SEMESTRE='2010I' C.CNOMBRE='ITC'""",

    """SELECT A#,ANOMBRE
FROM ALUMNOS
WHERE C# IN (SELECT C#
FROM CARRERAS
WHERE SEMESTRES=9)  

AND A# (SELECT A#

FROM INSCRITOS""", #No identifica el error

    """SELECT ANOMBRE
FROM ALUMNOS,INSCRITOS,CARRERAS
WHERE ALUMNOS.A#=INSCRITOS.A# AND ALUMNOS.C#=CARRERAS.C#
AND INSCRITOS.SEMESTRE='2010I'
AND CARRERAS.CNOMBRE='ISC
AND ALUMNOS.GENERACION='2010'""",

    """SELECT ANOMBRE
FROM ALUMNOS,INSCRITOS,CARRERAS
WHERE ALUMNOS.A#=INSCRITOS.A# AND ALUMNOS.C#=CARRERAS.C#
AND INSCRITOS.SEMESTRE '2010I'
AND CARRERAS.CNOMBRE='ISC'
AND ALUMNOS.GENERACION='2010'""",
]

# Lista de palabras reservadas de MySQL
valores = {
    "d": {",": 50, ".": 51, "(": 52, ")": 53, "'": 54},
    "c_n": 61,
    "c_an": 62,
    "o": {"+": 70, "-": 71, "*": 72, "/": 73},
    "r": {"<": 8, ">": 8, "=": 8, ">=": 8, "<=": 8},
    "p_c": {
        "SELECT": 10,
        "FROM": 11,
        "WHERE": 12,
        "IN": 13,
        "AND": 14,
        "OR": 15,
        "CREATE": 16,
        "TABLE": 17,
        "NUMERIC": 18,
        "NOT": 19,
        "NULL": 20,
        "CONSTRAINT": 21,
        "KEY": 22,
        "PRIMARY": 23,
        "FOREIGN": 24,
        "REFERENCES": 25,
        "INSERT": 26,
        "INTO": 27,
        "VALUES": 28,
    },
}
palabras_reservadas_mysql = [
    "SELECT",
    "FROM",
    "WHERE",
    "AND",
    "OR",
    "NOT",
    "JOIN",
    "ON",
    "GROUP BY",
    "ORDER BY",
    "HAVING",
    "INSERT INTO",
    "VALUES",
    "UPDATE",
    "SET",
    "DELETE FROM",
    "CREATE TABLE",
    "ALTER TABLE",
    "DROP TABLE",
    "ADD COLUMN",
    "ALTER COLUMN",
    "ADD CONSTRAINT",
    "FOREIGN KEY",
    "REFERENCES",
    "PRIMARY KEY",
    "DEFAULT",
    "NULL",
    "UNIQUE",
    "INDEX",
    "AUTO_INCREMENT",
    "DATABASE",
    "TABLE",
    "CONSTRAINT",
    "IF EXISTS",
    "CASCADE",
    "RESTRICT",
    "INNER",
    "LEFT",
    "RIGHT",
    "FULL",
    "OUTER",
    "UNION",
    "DISTINCT",
    "ALL",
    "LIKE",
    "AS",
    "COUNT",
    "SUM",
    "AVG",
    "MIN",
    "MAX",
    "IN",
    "BETWEEN",
    "IS",
    "NULL",
    "AS",
    "CASE",
    "WHEN",
    "THEN",
    "ELSE",
    "END",
]

modulo_de_errores = {
    4: "IDENTIFICADOR",
    10: "SELECT",
    11: "FROM",
    12: "WHERE",
    13: "IN",
    14: "AND",
    15: "OR",
    16: "CREATE",
    17: "TABLE",
    18: "CHAR",
    19: "NUMERIC",
    20: "NOT",
    21: "NULL",
    22: "CONSTRAINT",
    23: "KEY",
    24: "PRIMARY",
    25: "FOREIGN",
    26: "REFERENCES",
    27: "INSERT",
    28: "INTO",
    29: "VALUES",
    50: ",",
    51: ".",
    52: "( o )",
    53: "( o )",
    54: "'",
    55: "'",
    61: "CONSTANTE (NUMERICA)",
    62: "CONSTANTE (ALFANUMERICA)",
    70: "+",
    71: "-",
    72: "*",
    73: "/",
    81: ">",
    82: "<",
    83: "=",
    84: ">=",
    85: "<=",
    8: "RELACIONAL",
}

# Crear la expresión regular para encontrar palabras reservadas
expresion_regular_mysql = (
    r"\b(?:" + "|".join(map(re.escape, palabras_reservadas_mysql)) + r")\b"
)


def encontrar_caracteres_invalidos_SQL(texto):
    caracteres_invalidos = re.findall(r"[^\w\s\'.,()=<>!&|+\-/*%]", texto)
    caracteres_invalidos = list(set(caracteres_invalidos))  # Eliminar duplicados
    return caracteres_invalidos


def imprimir_tabla_caracteres_invalidos(caracteres_invalidos, texto):
    print("\nTabla de Caracteres Inválidos:")
    print("Carácter   Línea")
    print("------------------")
    for caracter in caracteres_invalidos:
        lineas = [
            str(i) for i, linea in enumerate(texto.split("\n"), 1) if caracter in linea
        ]
        print(f"{caracter:<10} {', '.join(lineas)}")


def encontrar_elementos_sql(texto):
    # Palabras reservadas
    def encontrar_palabras_reservadas_SQL(texto):
        palabras_reservadas = re.findall(expresion_regular_mysql, texto.upper())
        return palabras_reservadas

    # Delimitadores
    def encontrar_delimitadores_SQL(texto):
        delimitadores = re.findall(r"[.,()\'\"]", texto)
        return delimitadores

    # Operadores relacionales
    def encontrar_operadores_relacionales_SQL(texto):
        operadores_relacionales = re.findall(r"<=|>=|<>|!=|=|<|>", texto)
        return operadores_relacionales

    def encontrar_nombres_variables_SQL(texto):
        # Buscar palabras que no estén entre comillas simples, no sean palabras reservadas y no se repitan
        nombres_variables = re.findall(
            r"\b(?!(?:"
            + "|".join(map(re.escape, palabras_reservadas_mysql))
            + r")\b)(?<![\'\"])\b([A-Za-z_][A-Za-z0-9_]*)\b",
            texto,
        )
        nombres_variables_sin_repeticiones = []
        for nombre_variable in nombres_variables:
            if nombre_variable not in nombres_variables_sin_repeticiones:
                nombres_variables_sin_repeticiones.append(nombre_variable)
        return nombres_variables_sin_repeticiones

    codigo_identificador = 401

    # Lista para almacenar las constantes encontradas
    constantes_encontradas = []

    # Imprimir la tabla para palabras reservadas, delimitadores, operadores relacionales, y constantes
    def tabla_lexica():
        # Inicializar el contador de token y línea
        num_token = 1
        num_linea = 1
        codigo_palabra_reservada = 10
        codigo_delimitador = 50
        codigo_operador_relacional = 83
        codigo_operador_aritmetico = 401

        # Contador de las tablas 2 y 3
        codigo_constante = 600
        print("No.  Línea  TOKEN         Tipo  Código")
        print("-----------------------------------------")

        # Dividir el texto en líneas y procesar cada línea
        for i, linea in enumerate(texto.split("\n")):
            # Dividir la línea en tokens usando expresiones regulares
            tokens = re.findall(
                r"[A-Za-z_]+|\d+\.?\d*|'.*?'|<=|>=|<>|!=|=|<|>|[.,()\*]", linea
            )

            linea = 0
            for token in tokens:
                linea += 1
                tipo = ""
                codigo = ""
                palabra_identificador = 0
                if token.strip().upper() in encontrar_palabras_reservadas_SQL(texto):
                    tipo = "1"
                    codigo = codigo_palabra_reservada
                    palabra_identificador = valores.get("p_c").get(token)
                    linea = i + 1
                    codigo_palabra_reservada += 1
                elif token in encontrar_delimitadores_SQL(texto):
                    tipo = "5"
                    codigo = codigo_delimitador
                    palabra_identificador = valores.get("d").get(token)
                    linea = i + 1
                    codigo_delimitador += 1
                elif token in encontrar_operadores_relacionales_SQL(texto):
                    tipo = "8"
                    codigo = codigo_operador_relacional
                    linea = i + 1
                    codigo_operador_relacional += 1
                    palabra_identificador = valores.get("r").get(token)
                elif token.startswith("'") and token.endswith("'"):
                    tipo = "6"
                    codigo = codigo_constante
                    linea = i + 1
                    codigo_constante += 1
                    token = token[1:-1]  # Quitar las comillas simples
                    constNumericos = "(?<=['\\ =]|[><]|=)\\d+(?=['|\\s|$])|\b\\d+\b"
                    es_numerico = re.fullmatch(constNumericos, token)
                    if es_numerico == True:
                        palabra_identificador = valores.get("c_n")
                    else:
                        palabra_identificador = valores.get("c_an")
                    constantes_encontradas.append((token, codigo, tipo))
                elif token == "*":  # Corregir la detección del token '*'
                    tipo = "4"
                    codigo = codigo_operador_aritmetico
                    palabra_identificador = 4
                elif token in encontrar_nombres_variables_SQL(texto):
                    tipo = "4"  # Cambiado a tipo 4 para los nombres de variables
                    linea = i + 1
                    codigo = codigo_operador_aritmetico
                    codigo_operador_aritmetico += 1
                    palabra_identificador = 4
                else:
                    tipo = "999"  # Cambiado a tipo 6 para los números
                    codigo = 999
                    linea = i + 1
                    palabra_identificador = 999
                tokens_array.append(
                    {
                        "num_token": num_token,
                        "num_linea": num_linea,
                        "token": token,
                        "tipo": tipo,
                        "codigo": codigo,
                        "id": palabra_identificador,
                        "linea": linea,
                    }
                )
                num_token += 1
            num_linea += 1

    tabla_lexica()

    # Encontrar caracteres inválidos
    caracteres_invalidos = encontrar_caracteres_invalidos_SQL(texto)
    if caracteres_invalidos:
        imprimir_tabla_caracteres_invalidos(caracteres_invalidos, texto)
    else:
        print("No se encontraron caracteres inválidos en el SQL.")


# Ejemplo de uso
texto_ejemplo = """
SELECT ANOMBRE
FROM ALUMNOS,INSCRITOS,
WHERE ALUMNOS.A#=INSCRITOS.A# AND
INSCRITOS.SEMESTRE='2010I'
"""

tabla_sintactica = {
    300: {10: [10, 301, 11, 306, 310]},
    301: {4: [302], 72: [72]},
    302: {4: [304, 303]},
    303: {11: [99], 50: [50, 302]},
    304: {4: [4, 305]},
    305: {
        8: [99],
        11: [99],
        13: [99],
        14: [99],
        15: [99],
        50: [99],
        51: [51, 4],
        53: [99],
        199: [99],
    },
    306: {4: [308, 307]},
    307: {12: [99], 50: [50, 306], 53: [99], 199: [99]},
    308: {4: [4, 309]},
    309: {4: [4], 12: [99], 50: [99], 53: [99], 199: [99]},
    310: {12: [12, 311], 53: [99], 199: [99]},
    311: {4: [313, 312]},
    312: {14: [317, 311], 15: [317, 311], 53: [99], 199: [99]},
    313: {4: [304, 314]},
    314: {8: [315, 316], 13: [13, 52, 300, 53]},
    315: {8: [8]},
    316: {4: [304], 54: [54, 318, 54], 61: [319], 62: [319]},
    317: {14: [14], 15: [15]},
    318: {62: [62]},
    319: {61: [61], 62: [62]},
}



# Manejar errores
def error(mensaje):
    print(f"ERROR: {mensaje}")


# Función principal del análisis
def analizar():
    apun = 0
    reglas = []
    reglas.append(199)
    reglas.append(300)
    x = reglas.pop()
    while x != 199:
        if apun == len(tokens_array):
            k = 199
        else:
            k = tokens_array[apun].get("id")
        if x < 300:
            if x == k:
                apun += 1  # Avanzar apuntador
            else:
                print("Se esperaba: ", x, "\n Se obtuvo", k)
                break
        else:
            # Suponiendo que 'X' y 'K' son placeholders para valores reales
            produccion = tabla_sintactica.get(x).get(k)
            if produccion != None:
                if produccion != 99 and es_saltable(produccion):
                    for regla in reversed(produccion):
                        reglas.append(regla)
            else:
                origen_error = tokens_array[apun].get("token")
                origen_previo_error = ""
                if apun != 0:
                    origen_previo_error = tokens_array[apun - 1].get("token")
                linea = tokens_array[apun].get("linea")
                print(
                    "ERROR ENTRE:",
                    "'",
                    origen_previo_error,
                    "'",
                    "Y:",
                    "'",
                    origen_error,
                    "'",
                    "EN LA LINEA: ",
                    linea - 1,
                )
                llaves = list(tabla_sintactica.get(x).keys())
                print("Se esperaban alguno de los siguientes: ")
                for llave in llaves:
                    if modulo_de_errores.get(llave) != None:
                        print("Se esperaba: ", modulo_de_errores.get(llave))
                break
        x = reglas.pop()


def es_saltable(reglas):
    for r in reglas:
        if r == 99:
            return False
    return True


# Ejemplo de ejecución

texto = """
SELECT *
FROM PROFESORES
WHERE EDAD >'45' AND GRADO='MAE' OR GRADO='DOC'"""
print(texto)
encontrar_elementos_sql(texto)
analizar()
