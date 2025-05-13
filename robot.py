import turtle
import tkinter as tk
from tkinter import messagebox
import math

# Sabit uzunluklar
link_lengths = [60, 60, 60]

# Ana pencere
root = tk.Tk()
root.title("6 Eksenli Robot Kol - 2D Projeksiyon")

# Ana çerçeve (yatay bölünmüş)
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Sol panel (ayarlar ve girişler)
left_panel = tk.Frame(main_frame, padx=10, pady=10)
left_panel.pack(side="left", fill="y")

# Sağ panel (çizim)
right_panel = tk.Frame(main_frame)
right_panel.pack(side="right", fill="both", expand=True)

# Açı giriş kutuları (2 satırda 3'erli)
angle_entries = []
angle_frame = tk.LabelFrame(left_panel, text="Açı Girişleri", padx=5, pady=5)
angle_frame.pack(pady=10)

for i in range(6):
    frame = tk.Frame(angle_frame)
    frame.grid(row=i // 3, column=i % 3, padx=5, pady=2)
    tk.Label(frame, text=f"Açı {i + 1}").pack()
    entry = tk.Entry(frame, width=6)
    entry.pack()
    angle_entries.append(entry)

# Bakış açısı seçimi
view_frame = tk.LabelFrame(left_panel, text="Bakış Açısı", padx=5, pady=5)
view_frame.pack(pady=10)

view_var = tk.StringVar(value="xy")
tk.Radiobutton(view_frame, text="X-Y Düzlemi", variable=view_var, value="xy").pack(anchor="w")
tk.Radiobutton(view_frame, text="X-Z Düzlemi", variable=view_var, value="xz").pack(anchor="w")

# Çizim butonu
tk.Button(left_panel, text="Robotu Çiz", command=lambda: draw_robot_arm()).pack(pady=10)

# Konum etiketi
position_label = tk.Label(left_panel, text="Uç Efektör Konumu: ", justify="left")
position_label.pack(pady=10)

# Sağ panelde canvas ve turtle
canvas = tk.Canvas(right_panel, width=700, height=600, bg="white")
canvas.pack(padx=10, pady=10, expand=True)
screen = turtle.TurtleScreen(canvas)
screen.tracer(0)
t = turtle.RawTurtle(screen)
t.hideturtle()
t.speed(0)

# Robot çizim fonksiyonu
def draw_robot_arm():
    try:
        angles = [float(entry.get()) for entry in angle_entries]
    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm açıları doğru girin!")
        return

    t.clear()
    t.penup()
    t.goto(0, 0)
    t.setheading(90)
    t.pendown()

    # Düzlem başlığı
    t.penup()
    t.goto(-250, 260)
    t.pendown()
    düzlem_text = "X-Y DÜZLEMİ" if view_var.get() == "xy" else "X-Z DÜZLEMİ"
    t.write(f"Düzlem: {düzlem_text}", font=("Arial", 14, "bold"))

    t.penup()
    t.goto(0, 0)
    t.setheading(90)
    t.pendown()

    # Sadece eklem açıları: omuz, dirsek, bilek
    active_angles = [angles[1], angles[2], angles[4]]
    total_angle = 90
    x, y = 0, 0

    for i in range(3):
        total_angle += active_angles[i]
        rad = math.radians(total_angle)
        dx = link_lengths[i] * math.cos(rad)
        dy = link_lengths[i] * math.sin(rad)
        x += dx
        y += dy
        t.setheading(total_angle)
        t.forward(link_lengths[i])

    # Uç efektör konumu işaretle
    t.penup()
    t.goto(x, y)
    t.dot(6, "red")
    t.write(f"({round(x)}, {round(y)})", font=("Arial", 10))

    # Label güncelle
    düzlem = "X-Y" if view_var.get() == "xy" else "X-Z"
    position_label.config(text=f"Uç Efektör Konumu ({düzlem}): X = {round(x)}, Y/Z = {round(y)}")

    # Ekranı güncelle
    screen.update()

# Başlat
root.mainloop()
