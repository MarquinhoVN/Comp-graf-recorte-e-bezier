import numpy as np
import tkinter as tk
from tkinter import Canvas

#Calcula o polinômio de Bernstein para um dado valor de t
def polinomio_bernstein(n, i, t):
    return (np.math.comb(n, i)) * (t ** i) * ((1 - t) ** (n - i))

#Gera os pontos da curva de Bézier paramétrica com base nos pontos de controle
def curva_bezier_parametrica(pontos_controle, num_pontos=50):
    n = len(pontos_controle) - 1
    t_values = np.linspace(0, 1, num_pontos)
    curva = np.zeros((num_pontos, 2))
    
    for i in range(n + 1):
        curva += np.array(pontos_controle[i]) * polinomio_bernstein(n, i, t_values)[:, np.newaxis]
    return curva

#Desenha a curva de Bézier e os pontos de controle.
def desenhar_curva(metodo):
    canvas.delete("all")
    if len(pontos_controle) >= 2:
        curva = metodo(pontos_controle)
        for i in range(len(curva) - 1):
            x1, y1 = curva[i] * escala
            x2, y2 = curva[i + 1] * escala
            canvas.create_line(x1, y1, x2, y2, fill='blue')
    for x, y in pontos_controle:
        canvas.create_oval(x * escala - 5, y * escala - 5, x * escala + 5, y * escala + 5, fill='red', tags='ponto')

#Adiciona um novo ponto de controle na posição do clique e desenha a curva.
def ao_clicar(event):
    pontos_controle.append((event.x / escala, event.y / escala))
    for x, y in pontos_controle:
        canvas.create_oval(x * escala - 5, y * escala - 5, x * escala + 5, y * escala + 5, fill='red', tags='ponto')
    desenhar_curva(curva_bezier_parametrica)
        

root = tk.Tk()
root.title("Curva de Bézier")
escala = 100
canvas = Canvas(root, width=500, height=500, bg='white')
canvas.pack()

pontos_controle = []

canvas.bind("<Button-1>", ao_clicar)
root.mainloop()
