import tkinter as tk
from tkinter import simpledialog

def estatica():
    calificaciones = [0] * 5  # Equivalente a: int calificaciones[] = new int[5];
    
    root = tk.Tk()
    root.withdraw()
    
    for i in range(5):  # Equivalente a: for(int i = 0; i < 5; i++)
        entrada = simpledialog.askstring("Input", "Captura la calificación")
        if entrada is not None:
            calificaciones[i] = int(entrada)
    
    for i in range(5):  # Equivalente a: for(int i = 0; i < 5; i++)
        print("La calificación " + str(i+1) + " es: " + str(calificaciones[i]))
   
def dinamica():
    Fruta = []
    Fruta.append("Manzana")
    Fruta.append("Pera")
    Fruta.append("Uvas")
    Fruta.append("Bananas")
    print(Fruta)
    Fruta.remove(Fruta[1])
    Fruta.remove(Fruta[0])
    Fruta.append("sandia")
    print(Fruta)

if __name__ == "__main__":
    estatica()  
    dinamica()   