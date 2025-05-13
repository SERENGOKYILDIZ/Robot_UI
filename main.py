import turtle
import tkinter as tk
from tkinter import messagebox
import math
from sympy import symbols
import numpy as np

from every_location import EveryLocation

# Sabit uzunluklar
L1 = 20
L2 = 30
L3 = 40
d6 = 20

# Değişken açılar
t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0
t6 = 0

# Uç İşlevci Konumları
px = 0
py = 0
pz = 0

# Uç İşlevci Yönelimleri
R60 = [0, 0, 1,
       0, -1, 0,
       1, 0, 0]

# Yazılım Değişkenleri
Duzlem_Mod = 0 # 0=ön, 1=yan
angles = [0, 0, 0, 0, 0, 0]

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
angle_frame = tk.LabelFrame(left_panel, text="İleri Kinematik Açı Girişleri", padx=5, pady=5)
angle_frame.pack(pady=10)

for i in range(6):
    frame = tk.Frame(angle_frame)
    frame.grid(row=i // 3, column=i % 3, padx=5, pady=2)
    tk.Label(frame, text=f"Açı {i + 1}").pack()
    entry = tk.Entry(frame, width=6)
    entry.insert(0, "0")
    entry.pack()
    angle_entries.append(entry)

# Konum giriş kutuları (1 satırda 3'erli)
location_entries = []
location_frame = tk.LabelFrame(left_panel, text="Ters Kinematik Uç İşlevci Girişleri", padx=5, pady=5)
location_frame.pack(pady=10)
locs = ["X", "Y", "Z"]

for i in range(3):
    frame = tk.Frame(location_frame)
    frame.grid(row=i // 3, column=i % 3, padx=5, pady=2)
    tk.Label(frame, text=f"P{locs[i]}").pack()
    entry = tk.Entry(frame, width=6)
    entry.insert(0, "0")
    entry.pack()
    location_entries.append(entry)

# Konum giriş kutuları (1 satırda 3'erli)
rotation_entries = []
rotation_frame = tk.LabelFrame(left_panel, text="Ters Kinematik Yönelim Matrisi", padx=5, pady=5)
rotation_frame.pack(pady=10)
for i in range(9):
    frame = tk.Frame(rotation_frame)
    frame.grid(row=i // 3, column=i % 3, padx=1, pady=1)
    tk.Label(frame).pack()
    entry = tk.Entry(frame, width=6)
    entry.insert(0, "0")
    entry.pack()
    rotation_entries.append(entry)

# Bakış açısı seçimi
view_frame = tk.LabelFrame(left_panel, text="Bakış Açısı", padx=5, pady=5)
view_frame.pack(pady=10)

view_var = tk.StringVar(value="on")
tk.Radiobutton(view_frame, text="Ön Düzlemi", variable=view_var, value="on").pack(anchor="w")
tk.Radiobutton(view_frame, text="Yan Düzlemi", variable=view_var, value="yan").pack(anchor="w")

# Kinematik seçimi
kinematic_frame = tk.LabelFrame(left_panel, text="Kinematik Açısı", padx=5, pady=6)
kinematic_frame.pack(pady=10)

kinematic_var = tk.StringVar(value="forward")

def changed_kinematics():
    var = kinematic_var.get()
    if var == "forward":
        for entry in angle_entries:
            entry.config(state="normal")
        for entry in location_entries:
            entry.config(state="disabled")
        for entry in rotation_entries:
            entry.config(state="disabled")
    elif var == "inverse":
        for entry in angle_entries:
            entry.config(state="disabled")
        for entry in location_entries:
            entry.config(state="normal")
        for entry in rotation_entries:
            entry.config(state="normal")

changed_kinematics()

tk.Radiobutton(kinematic_frame, text="İleri Kinematik", variable=kinematic_var, value="forward", command=changed_kinematics).pack(anchor="w")
tk.Radiobutton(kinematic_frame, text="Ters Kinematik", variable=kinematic_var, value="inverse", command=changed_kinematics).pack(anchor="w")

# Çizim butonu
tk.Button(left_panel, text="Robotu Çiz", command=lambda: robot()).pack(pady=10)

# Sağ panelde canvas ve turtle
canvas = tk.Canvas(right_panel, width=500, height=600, bg="white")
canvas.pack(padx=10, pady=10, expand=True)
screen = turtle.TurtleScreen(canvas)
screen.tracer(0)
t = turtle.RawTurtle(screen)
t.hideturtle()
t.speed(0)

def draw_robot():
    t.clear()
    t.penup()
    t.goto(0, 0)
    t.setheading(90)
    t.pendown()

    if view_var.get() == "on":
        duzlem_Mod = 0
    else:
        duzlem_Mod = 1

    # İleri Kinematik başlığı
    t.penup()
    t.goto(-200, 160)
    t.pendown()
    my_str=""
    if kinematic_var.get() == "forward":
        my_str = "İLERİ KİNEMATİK"
    else:
        my_str = "TERS KİNEMATİK"
    if duzlem_Mod == 0:
        my_str += f" - ÖN DÜZLEM"
    else:
        my_str += f" - YAN DÜZLEM"
    t.write(my_str, font=("Arial", 14, "bold"))

    t.penup()
    t.goto(0, 0)
    t.setheading(0)
    t.pendown()

    loc = EveryLocation(angles)
    locations = []
    locations = loc.get_locations()
    # print(locations)

    PX = round(locations[5][0])
    PY = round(locations[5][1])
    PZ = round(locations[5][2])

    # # # # # # # # # # # # # # # # # # # # # # # #
    if(duzlem_Mod == 0): ###################### Ön (x ve z kullan)
        t.dot(6, "blue")
        for location in locations:
            draw_line(location[0], location[2])
        t.dot(6, "blue")
    else:  #################################### Yan (y ve z kullan)
        t.dot(6, "blue")
        for location in locations:
            draw_line(location[1], location[2])
        t.dot(6, "blue")
    # # # # # # # # # # # # # # # # # # # # # # # #

    # Uç efektör konumu işaretle
    t.write(f"({PX}, {PY}, {PZ})", font=("Arial", 10))

    # Ekranı güncelle
    screen.update()

def draw_line(x, y):
    t.pendown()
    t.goto(x, y)
    t.setheading(0)
    t.dot(6, "red")
    t.penup()

def forward_kinematics():
    try:
        t1 = float(angle_entries[0].get())
        t2 = float(angle_entries[1].get())
        t3 = float(angle_entries[2].get())
        t4 = float(angle_entries[3].get())
        t5 = float(angle_entries[4].get())
        t6 = float(angle_entries[5].get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm açıları doğru girin!")
        return

    angles[0] = t1
    angles[1] = t2
    angles[2] = t3
    angles[3] = t4
    angles[4] = t5
    angles[5] = t6

    draw_robot()

def inverse_kinematics():
    try:
        px = float(location_entries[0].get())
        py = float(location_entries[1].get())
        pz = float(location_entries[2].get())

        for num in range(9):
            R60[num] = float(rotation_entries[num].get())

    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm açıları doğru girin!")
        return

    z1 = R60[2]
    z2 = R60[5]
    z3 = R60[8]

    wx = px - d6 * z1
    wy = py - d6 * z2
    wz = pz - d6 * z3

    t1 = math.atan2(wy, wx)

    a = L3
    b = L2
    c = wx * math.cos(t1) + wy * math.sin(t1)
    d = wz - L1
    cost3 = (c ** 2 + d ** 2 - a ** 2 - b ** 2) / (2 * a * b)
    sint3 = math.sqrt(1 - cost3 ** 2)
    t3 = math.atan2(sint3, cost3)

    r = a * cost3 + b
    s = a * sint3
    t2 = math.atan2(r * d - s * c, r * c + s * d)

    T10 = np.array([
        [np.cos(t1), -np.sin(t1), 0, 0],
        [np.sin(t1),  np.cos(t1), 0, 0],
        [0,           0,          1, L1],
        [0,           0,          0, 1]
    ])
    T21 = np.array([
        [np.cos(t2), -np.sin(t2), 0, 0],
        [0,          0,          -1, 0],
        [np.sin(t2), np.cos(t2),  0, 0],
        [0,          0,           0, 1]
    ])
    T32 = np.array([
        [np.cos(t3 + np.pi/2), -np.sin(t3 + np.pi/2), 0, L2],
        [np.sin(t3 + np.pi/2),  np.cos(t3 + np.pi/2), 0, 0],
        [0,                    0,                    1, 0],
        [0,                    0,                    0, 1]
    ])
    T43 = np.array([
        [1, 0,  0,  0],
        [0, 0, -1, -L3],
        [0, 1,  0,  0],
        [0, 0,  0,  1]
    ])
    T40 = T10 @ T21 @ T32 @ T43
    R4_0 = T40[:3, :3]
    R6_0 = np.array(R60).reshape((3, 3))
    R4_6 = R4_0.T @ R6_0

    a_t5 = R4_6[2, 2]
    t5 = math.atan2(math.sqrt(1 - a_t5 ** 2), a_t5)
    t4 = math.atan2(-R4_6[1, 2], -R4_6[0, 2])
    t6 = math.atan2(-R4_6[2, 1], R4_6[2, 0])

    print(f"t1 : {math.degrees(t1):.2f}°")
    print(f"t2 : {math.degrees(t2):.2f}°")
    print(f"t3 : {math.degrees(t3):.2f}°")
    print(f"t4 : {math.degrees(t4):.2f}°")
    print(f"t5 : {math.degrees(t5):.2f}°")
    print(f"t6 : {math.degrees(t6):.2f}°")

    t1 = math.degrees(t1)
    t2 = math.degrees(t2)
    t3 = math.degrees(t3)
    t4 = math.degrees(t4)
    t5 = math.degrees(t5)
    t6 = math.degrees(t6)

    angles[0] = t1
    angles[1] = t2
    angles[2] = t3
    angles[3] = t4
    angles[4] = t5
    angles[5] = t6

    draw_robot()

def robot():
    if kinematic_var.get() == "forward":
        forward_kinematics()
    else:
        inverse_kinematics()

# Başlat
root.mainloop()
# t1 : 143.13°
# t2 : -8.53°
# t3 : 67.98°
# t4 : -138.95°
# t5 : 113.99°
# t6 : 19.50°