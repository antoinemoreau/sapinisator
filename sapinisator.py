#! /usr/bin/env python3

import struct

class Point:
    def __init__(self, x, y ,z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return("Point[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]")

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __str__(self):
        return("Triangle[" + str(self.p1) + ", " + str(self.p2) + ", " + str(self.p3) + "]")

def read_stl(filename):
    triangles = []

    with open(filename, "rb") as f:
        head = f.read(80)
        nbtriangles = f.read(4)
        nbtriangles = struct.unpack("<I", nbtriangles)
        
        for tri in range(nbtriangles[0]):
            # on passe la normale du triangle
            f.read(12)

            points = []
            # récupération des points
            for i in range(3):
                x = struct.unpack(">f", f.read(4))
                y = struct.unpack(">f", f.read(4))
                z = struct.unpack(">f", f.read(4))
                points.append(Point(x[0], y[0], z[0]))

            triangles.append(Triangle(points[0], points[1], points[2]))

        for trian in triangles:
            print(trian)

        mot_de_controle = f.read(2)

        return triangles   

def main():
    read_stl("Schichtschwein_ohne_Logo.stl")

main()