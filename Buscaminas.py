import random
import os

def crear_matriz(filas, columnas, valor):
    return [[valor for _ in range(columnas)] for _ in range(filas)]

def imprimir_matriz(matriz):
    print("\n" + "+" + "---+" * len(matriz[0]))
    for fila in matriz:
        print("|", end="")
        for c in fila:
            print(f" {c} |", end="")
        print("\n" + "+" + "---+" * len(fila))
        
def ubicar_minas(matriz, total, filas, columnas):
    ubicaciones = []
    colocadas = 0
    while colocadas < total:
        f = random.randint(0, filas - 1)
        c = random.randint(0, columnas - 1)
        if matriz[f][c] != 9:
            matriz[f][c] = 9
            ubicaciones.append((f, c))
            colocadas += 1
    return matriz, ubicaciones

def asignar_pistas(matriz, filas, columnas):
    for f in range(filas):
        for c in range(columnas):
            if matriz[f][c] == 9:
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nf, nc = f + df, c + dc
                        if 0 <= nf < filas and 0 <= nc < columnas:
                            if matriz[nf][nc] != 9:
                                matriz[nf][nc] += 1
    return matriz

def descubrir_zonas(cubierto, visible, f, c, filas, columnas, marca):
    pendientes = [(f, c)]
    while pendientes:
        f, c = pendientes.pop()
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nf, nc = f + df, c + dc
                if 0 <= nf < filas and 0 <= nc < columnas:
                    if visible[nf][nc] == marca and cubierto[nf][nc] == 0:
                        visible[nf][nc] = 0
                        if (nf, nc) not in pendientes:
                            pendientes.append((nf, nc))
                    elif visible[nf][nc] == marca:
                        visible[nf][nc] = cubierto[nf][nc]
    return visible

def tablero_resuelto(tablero, filas, columnas, marca):
    for f in range(filas):
        for c in range(columnas):
            if tablero[f][c] == marca:
                return False
    return True

def pantalla_inicio():
    os.system("cls" if os.name == "nt" else "clear")
    print("========== BUSCAMINAS ==========")
    print("  Controles:")
    print("    w/s/a/d -> mover")
    print("    m       -> mostrar")
    print("    b       -> marcar mina")
    print("    v       -> desmarcar")
    print("================================")
    input("Pulsa Enter para comenzar...")

def pedir_entrada():
    return input("\nElige acción (w/s/a/d, m, b, v): ").strip().lower()

def limpiar_ceros(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 0:
                matriz[i][j] = " "
    return matriz

# ==== CONFIGURACIÓN ====

filas, columnas = 12, 16
total_minas = 15
marca_usuario = "-"
marcadas = []

visible = crear_matriz(filas, columnas, marca_usuario)
oculto = crear_matriz(filas, columnas, 0)
oculto, posiciones_minas = ubicar_minas(oculto, total_minas, filas, columnas)
oculto = asignar_pistas(oculto, filas, columnas)

pantalla_inicio()

yf = random.randint(2, filas - 3)
xf = random.randint(2, columnas - 3)
anterior = visible[yf][xf]
visible[yf][xf] = "x"

jugando = True
ganaste = False

while jugando:
    os.system("cls" if os.name == "nt" else "clear")
    imprimir_matriz(visible)
    orden = pedir_entrada()

    if orden == "w" and yf > 0:
        visible[yf][xf] = anterior
        yf -= 1
        anterior = visible[yf][xf]
        visible[yf][xf] = "x"

    elif orden == "s" and yf < filas - 1:
        visible[yf][xf] = anterior
        yf += 1
        anterior = visible[yf][xf]
        visible[yf][xf] = "x"

    elif orden == "a" and xf > 0:
        visible[yf][xf] = anterior
        xf -= 1
        anterior = visible[yf][xf]
        visible[yf][xf] = "x"

    elif orden == "d" and xf < columnas - 1:
        visible[yf][xf] = anterior
        xf += 1
        anterior = visible[yf][xf]
        visible[yf][xf] = "x"

    elif orden == "b":
        if anterior == marca_usuario:
            visible[yf][xf] = "#"
            anterior = "#"
            if (yf, xf) not in marcadas:
                marcadas.append((yf, xf))

    elif orden == "v":
        if anterior == "#":
            visible[yf][xf] = marca_usuario
            anterior = marca_usuario
            if (yf, xf) in marcadas:
                marcadas.remove((yf, xf))

    elif orden == "m":
        if oculto[yf][xf] == 9:
            visible[yf][xf] = "@"
            jugando = False
        elif oculto[yf][xf] > 0:
            visible[yf][xf] = oculto[yf][xf]
            anterior = visible[yf][xf]
        elif oculto[yf][xf] == 0:
            visible[yf][xf] = 0
            visible = descubrir_zonas(oculto, visible, yf, xf, filas, columnas, marca_usuario)
            visible = limpiar_ceros(visible)
            anterior = visible[yf][xf]

    if tablero_resuelto(visible, filas, columnas, marca_usuario) and \
       sorted(marcadas) == sorted(posiciones_minas) and \
       anterior != marca_usuario:
        ganaste = True
        jugando = False

# ==== RESULTADO FINAL ====
os.system("cls" if os.name == "nt" else "clear")
imprimir_matriz(visible)

if ganaste:
    print("\n ¡Felicidades, has ganado! ")
else:
    print("\n Has perdido, tocaste una mina. ")

input("\nPulsa Enter para salir...")
