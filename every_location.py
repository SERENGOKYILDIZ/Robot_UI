import math

import numpy as np

# Sabit uzunluklar (L1, L2, L3 ve d6)
L1 = 20
L2 = 30
L3 = 40
d6 = 20  # Uç efektörün mesafesi

class EveryLocation:
    def __init__(self, angles):
        self.locations = []
        self.t1 = np.radians(angles[0])
        self.t2 = np.radians(angles[1])
        self.t3 = np.radians(angles[2])
        self.t4 = np.radians(angles[3])
        self.t5 = np.radians(angles[4])
        self.t6 = np.radians(angles[5])

    def get_locations(self):
        # Dönüşüm matrislerini tanımla
        def T10(t1, L1):
            return np.array([
                [np.cos(t1), -np.sin(t1), 0, 0],
                [np.sin(t1), np.cos(t1), 0, 0],
                [0, 0, 1, L1],
                [0, 0, 0, 1]
            ])

        def T21(t2):
            return np.array([
                [np.cos(t2), -np.sin(t2), 0, 0],
                [0, 0, -1, 0],
                [np.sin(t2), np.cos(t2), 0, 0],
                [0, 0, 0, 1]
            ])

        def T32(t3, L2):
            return np.array([
                [np.cos(t3 + np.pi/2), -np.sin(t3 + np.pi/2), 0, L2],
                [np.sin(t3 + np.pi/2), np.cos(t3 + np.pi/2), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])

        def T43(t4, L3):
            return np.array([
                [np.cos(t4), -np.sin(t4), 0, 0],
                [0, 0, -1, -L3],
                [np.sin(t4), np.cos(t4), 0, 0],
                [0, 0, 0, 1]
            ])

        def T54(t5):
            return np.array([
                [np.cos(t5), -np.sin(t5), 0, 0],
                [0, 0, -1, 0],
                [np.sin(t5), np.cos(t5), 0, 0],
                [0, 0, 0, 1]
            ])

        def T65(t6):
            return np.array([
                [np.cos(t6), -np.sin(t6), 0, 0],
                [0, 0, 1, 0],
                [-np.sin(t6), -np.cos(t6), 0, 0],
                [0, 0, 0, 1]
            ])

        # Dönüşüm matrislerini sırayla çarp
        T01 = T10(self.t1, L1)
        T12 = np.dot(T01, T21(self.t2))
        T23 = np.dot(T12, T32(self.t3, L2))
        T34 = np.dot(T23, T43(self.t4, L3))
        T45 = np.dot(T34, T54(self.t5))
        T56 = np.dot(T45, T65(self.t6))

        # Her bir eklemin konumunu hesapla
        # Eklem 1 (T01 ile)
        position1 = T01 @ np.array([0, 0, 0, 1])

        # Eklem 2 (T12 ile)
        position2 = T12 @ np.array([0, 0, 0, 1])

        # Eklem 3 (T23 ile)
        position3 = T23 @ np.array([0, 0, 0, 1])

        # Eklem 4 (T34 ile)
        position4 = T34 @ np.array([0, 0, 0, 1])

        # Eklem 5 (T45 ile)
        position5 = T45 @ np.array([0, 0, 0, 1])

        # Eklem 6 (T56 ile, uç efektör)
        position6 = T56 @ np.array([0, 0, 0, 1])

        # Uç işlevci (end-effector) için yönelim ve konum hesaplama
        wx = T56[0, 3]  # x konumu
        wy = T56[1, 3]  # y konumu
        wz = T56[2, 3]  # z konumu

        zx = T56[0, 2]  # x yönelimi
        zy = T56[1, 2]  # y yönelimi
        zz = T56[2, 2]  # z yönelimi

        # d6 mesafesini ekleyerek yeni konumu hesapla
        px = round(wx + d6 * zx)
        py = round(wy + d6 * zy)
        pz = round(wz + d6 * zz)

        # Sonuçları yazdır
        # print("Pozisyon 1:", position1[:3])
        # print("Pozisyon 2:", position2[:3])
        # print("Pozisyon 3:", position3[:3])
        # print("Pozisyon 4:", position4[:3])
        # print("Pozisyon 5:", position5[:3])
        # print("Pozisyon 6 (uç efektör):", (px, py, pz))

        self.locations.append(position1[:3].tolist())
        self.locations.append(position2[:3].tolist())
        self.locations.append(position3[:3].tolist())
        self.locations.append(position4[:3].tolist())
        self.locations.append(position5[:3].tolist())
        self.locations.append([px, py, pz])

        # print(f"Dizi halinde\n{self.locations}")

        return self.locations
#
# angles = [0, 0, 0, 0, 0, 0]
# loc = EveryLocation(angles)
# deneme = loc.get_locations()
# print(deneme)