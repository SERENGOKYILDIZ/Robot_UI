import turtle
import tkinter as tk
from tkinter import messagebox

# Ana pencere
root = tk.Tk()
root.title("Tek Çizgi Çizimi")

# Uzunluk girişi
tk.Label(root, text="Uzunluk:").pack()
entry_length = tk.Entry(root)
entry_length.pack()

# Açı girişi
tk.Label(root, text="Açı (derece):").pack()
entry_angle = tk.Entry(root)
entry_angle.pack()

# Canvas (turtle için)
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack(pady=10)

# turtle ekranı ve turtle nesnesi
screen = turtle.TurtleScreen(canvas)
t = turtle.RawTurtle(screen)
t.speed(1)

# Çizim fonksiyonu
def draw_line():
    try:
        length = float(entry_length.get())
        angle = float(entry_angle.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")
        return

    t.clear()
    t.penup()
    t.goto(0, 0)
    t.setheading(angle)  # Açıyı ayarla
    t.pendown()
    t.forward(length)

# Buton
tk.Button(root, text="Çiz", command=draw_line).pack(pady=5)

# Main loop
root.mainloop()
