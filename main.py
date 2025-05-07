import turtle
import tkinter as tk

root = tk.Tk()
root.title("Turtle + Tkinter GUI")

label = tk.Label(root, text="Turtle çizimini başlatmak için butona basın.")
label.pack(pady=10)

canvas = tk.Canvas(master=root, width=400, height=400, bg="white")
canvas.pack()

screen = turtle.TurtleScreen(canvas)
t = turtle.RawTurtle(screen)
t.speed(1)

def draw_circle():
    t.clear()
    t.penup()
    t.goto(0, -100)
    t.pendown()
    t.circle(100)

def draw_square():
    t.clear()
    t.penup()
    t.goto(-50, -50)
    t.pendown()
    for _ in range(4):
        t.forward(100)
        t.left(90)

btn_circle = tk.Button(root, text="Daire Çiz", command=draw_circle)
btn_circle.pack(pady=5)

btn_square = tk.Button(root, text="Kare Çiz", command=draw_square)
btn_square.pack(pady=5)

root.mainloop()
