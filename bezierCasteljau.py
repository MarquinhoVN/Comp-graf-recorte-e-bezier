import tkinter as tk
import math
from tkinter import Canvas

# Função para calcular a curva de Bézier usando o algoritmo de Casteljau
def algoritmo_casteljau(x1, y1, x2, y2, x3, y3, x4, y4, conjunto_pixels):
    xm01, ym01 = (x1 + x2) / 2, (y1 + y2) / 2
    xm12, ym12 = (x2 + x3) / 2, (y2 + y3) / 2
    xm23, ym23 = (x3 + x4) / 2, (y3 + y4) / 2
    xm012, ym012 = (xm01 + xm12) / 2, (ym01 + ym12) / 2
    xm123, ym123 = (xm12 + xm23) / 2, (ym12 + ym23) / 2
    xm0123, ym0123 = (xm012 + xm123) / 2, (ym012 + ym123) / 2

    conjunto_pixels.add((round(xm0123), round(ym0123)))

    if math.sqrt((xm012 - xm123) ** 2 + (ym012 - ym123) ** 2) < 0.01:
        return
    else:
        algoritmo_casteljau(x1, y1, xm01, ym01, xm012, ym012, xm0123, ym0123, conjunto_pixels)
        algoritmo_casteljau(xm0123, ym0123, xm123, ym123, xm23, ym23, x4, y4, conjunto_pixels)

# Função para desenhar a curva no canvas
def desenhar_curva(canvas, pontos_controle):
    conjunto_pixels = set()

    x1, y1 = pontos_controle[0]
    x2, y2 = pontos_controle[1]
    x3, y3 = pontos_controle[2]
    x4, y4 = pontos_controle[3]
    
    algoritmo_casteljau(x1, y1, x2, y2, x3, y3, x4, y4, conjunto_pixels)

    for i in range(len(pontos_controle) - 1):
        x1, y1 = pontos_controle[i]
        x2, y2 = pontos_controle[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill='green', dash=(4, 2))

    for (x, y) in pontos_controle:
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')


    for (x, y) in conjunto_pixels:
        canvas.create_line(x - 1, y - 1, x + 1, y + 1, fill='blue')


root = tk.Tk()
root.title("Curva de Bézier")


canvas = Canvas(root, width=500, height=500, bg="white")
canvas.pack()

pontos_controle = [
    (50, 400), 
    (150, 50),  
    (350, 50),  
    (450, 400)  
]

# Desenhar a curva
desenhar_curva(canvas, pontos_controle)

# Iniciar a interface gráfica
root.mainloop()


