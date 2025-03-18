import tkinter as tk

# Função para desenhar o polígono original e o polígono recortado em uma interface gráfica.
def desenhar_poligonos(canvas, original, recortado, janela_recorte):
    x_min, y_min, x_max, y_max = janela_recorte
    canvas.create_rectangle(x_min * 50, y_min * 50, x_max * 50, y_max * 50, outline="green")
    
    if original:
        for i in range(len(original)):
            x1, y1 = original[i]
            x2, y2 = original[(i + 1) % len(original)]
            canvas.create_line(x1 * 50, y1 * 50, x2 * 50, y2 * 50, fill="red")
    
    if recortado:
        for i in range(len(recortado)):
            x1, y1 = recortado[i]
            x2, y2 = recortado[(i + 1) % len(recortado)]
            canvas.create_line(x1 * 50, y1 * 50, x2 * 50, y2 * 50, fill="blue")

# Algoritmo de recorte de Sutherland-Hodgman
def recortar(poligono, janela):
    x_min, y_min, x_max, y_max = janela
    
    def dentro(p, borda):
        x, y = p
        return (x >= x_min if borda == "esquerda" else
                x <= x_max if borda == "direita" else
                y >= y_min if borda == "topo" else
                y <= y_max)
    
    def intersecao(p1, p2, borda):
        x1, y1 = p1
        x2, y2 = p2
        
        if x1 == x2:
            if borda == "topo":
                x = x1
                y = y_min
            elif borda == "fundo":
                x = x1
                y = y_max
            return (x, y)

        if y1 == y2:
            if borda == "esquerda":
                x = x_min 
                y = y1 
            elif borda == "direita":
                x = x_max
                y = y1
            return (x, y)

        m = (y2 - y1) / (x2 - x1) 
        b = y1 - m * x1 

        if borda == "esquerda":
            x = x_min
            y = m * x + b
        elif borda == "direita":
            x = x_max
            y = m * x + b
        elif borda == "topo":
            y = y_min
            x = (y - b) / m
        elif borda == "fundo":
            y = y_max
            x = (y - b) / m

        return (x, y)


    
    for borda in ["esquerda", "direita", "topo", "fundo"]:
        novo_poligono = []
        for i in range(len(poligono)):
            atual, anterior = poligono[i], poligono[i - 1]
            if dentro(atual, borda) != dentro(anterior, borda):
                novo_poligono.append(intersecao(anterior, atual, borda))
            if dentro(atual, borda):
                novo_poligono.append(atual)
        poligono = novo_poligono
    return poligono

def executar_recorte():
    poligonos = [
        # [(3.5,0),(3.5,4),(6,4)]
        # [(2.5, 0), (4.5, 0), (4.5, 3), (4,3), (4, 1.5), (3, 1.5), (3, 3), (2.5, 3)]
        # [(3,3),(4,3), (4,4),(4.5,4),(4.5,6),(4,6),(4,7),(3,7),(3,6),(2.5,6),(2.5,4),(3,4)]
        # [(2.5,1.5),(3.5,2.5),(3,4),(1.75,4),(1.25,2.5)]
    ]
    janela_recorte = (2, 2, 5, 5)
    
    canvas.delete("all") 
    
    for poligono in poligonos:
        recortado = recortar(poligono, janela_recorte)
        desenhar_poligonos(canvas, poligono, recortado, janela_recorte)

root = tk.Tk()
root.title("Recorte de Polígonos - Sutherland-Hodgman")
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()
btn_recortar = tk.Button(root, text="Executar Recorte", command=executar_recorte)
btn_recortar.pack(pady=20)
root.mainloop()
