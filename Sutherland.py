import tkinter as tk

# Função para verificar se um ponto está dentro da janela de recorte
def dentro(p, borda, janela):
    x, y = p
    x_min, y_min, x_max, y_max = janela
    return (x >= x_min if borda == "esquerda" else
            x <= x_max if borda == "direita" else
            y >= y_min if borda == "topo" else
            y <= y_max)

# Função para calcular a interseção entre um segmento e uma borda da janela de recorte
def intersecao(p1, p2, borda, janela):
    x1, y1 = p1
    x2, y2 = p2
    x_min, y_min, x_max, y_max = janela
    
    if x1 == x2:
        if borda == "topo":
            return (x1, y_min)
        elif borda == "fundo":
            return (x1, y_max)
    if y1 == y2:
        if borda == "esquerda":
            return (x_min, y1)
        elif borda == "direita":
            return (x_max, y1)
    
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    
    if borda == "esquerda":
        return (x_min, m * x_min + b)
    elif borda == "direita":
        return (x_max, m * x_max + b)
    elif borda == "topo":
        return ((y_min - b) / m, y_min)
    elif borda == "fundo":
        return ((y_max - b) / m, y_max)
    
    return None

# Algoritmo de recorte de Sutherland-Hodgman
def recortar(poligono, janela):
    for borda in ["esquerda", "direita", "topo", "fundo"]:
        novo_poligono = []
        s = poligono[-1]  
        
        for p in poligono:
            s_dentro = dentro(s, borda, janela)
            p_dentro = dentro(p, borda, janela)
            
            if s_dentro and p_dentro:
                novo_poligono.append(p)
            elif s_dentro and not p_dentro:
                i = intersecao(s, p, borda, janela)
                if i:
                    novo_poligono.append(i)
            elif not s_dentro and p_dentro:
                i = intersecao(s, p, borda, janela)
                if i:
                    novo_poligono.append(i)
                novo_poligono.append(p)
            
            s = p  
        
        poligono = novo_poligono
    
    return poligono

# Função para desenhar os polígonos na interface gráfica
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

# Executa o recorte e exibe na interface
def executar_recorte():
    # poligonos = [[(3.5,0),(3.5,4),(6,4)]]
    # poligonos = [[(2.5, 0), (4.5, 0), (4.5, 3), (4,3), (4, 1.5), (3, 1.5), (3, 3), (2.5, 3)]]
    # poligonos = [[(3,3),(4,3), (4,4),(4.5,4),(4.5,6),(4,6),(4,7),(3,7),(3,6),(2.5,6),(2.5,4),(3,4)]]
    poligonos = [[(2.5,1.5),(3.5,2.5),(3,4),(1.75,4),(1.25,2.5)]]
    janela_recorte = (2, 2, 5, 5)
    
    canvas.delete("all") 
    
    for poligono in poligonos:
        recortado = recortar(poligono, janela_recorte)
        desenhar_poligonos(canvas, poligono, recortado, janela_recorte)

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Recorte de Polígonos - Sutherland-Hodgman")
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()
btn_recortar = tk.Button(root, text="Executar Recorte", command=executar_recorte)
btn_recortar.pack(pady=20)
root.mainloop()
