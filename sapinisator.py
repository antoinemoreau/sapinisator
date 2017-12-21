#! /usr/bin/env python3

import struct
from math import fabs, sin
import sys

class Point:
    def __init__(self, x, y ,z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return("Point[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]")

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y, self.z-other.z)

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)

class Triangle:
    def __init__(self, points):
        self.points = points

    def __str__(self):
        return("Triangle[" + str(self.points[0]) + ", " + str(self.points[1]) + ", " + str(self.points[2]) + "]")

def read_stl(filename):
    triangles = []

    with open(filename, "rb") as f:
        head = f.read(80)
        nbtriangles = f.read(4)
        nbtriangles = struct.unpack("<I", nbtriangles)
        
        #Récupération des triangles
        for tri in range(nbtriangles[0]):
            # on passe la normale du triangle
            f.read(12)

            points = []
            # récupération des points
            for i in range(3):
                x = struct.unpack("<f", f.read(4))
                y = struct.unpack("<f", f.read(4))
                z = struct.unpack("<f", f.read(4))
                points.append(Point(x[0], y[0], z[0]))

            triangles.append(Triangle(points))
            mot_de_controle = f.read(2)

        return triangles

def sapin(x, s):
    return x * fabs(sin(s * x)) / 100

def moyenne(points):
    moyenne = Point(0, 0, 0)
    nb_points = len(points)
    for p in points:
        moyenne.x += p.x / nb_points
        moyenne.y += p.y / nb_points
        moyenne.z += p.z / nb_points
    return moyenne

def agrandissement(p, facteur):
    return Point((p.x)*facteur, (p.y)*facteur, (p.z))


def sapinisation(triangles):
    triangles_sapinise = triangles
    ensemble_points = []

    for t in triangles:
        for p in t.points:
            ensemble_points.append(p)
    
    c = moyenne(ensemble_points)

    # On sapinise chaque point
    for nbt,t in enumerate(triangles):
        for nbp,p in enumerate(t.points):
            coeff = sapin(p.z, 100)
            triangles_sapinise[nbt].points[nbp] = agrandissement(p - c, coeff) + c

    return triangles_sapinise

def stl_entete(source, dest):
     with open(source, "rb") as s:
         head = s.read(84)
     with open(dest, "wb") as d:
         d.write(head)

def stl_triangle(dest, triangle):
    with open(dest, "ab") as d:
        d.write(struct.pack("<f", 0))
        d.write(struct.pack("<f", 0))
        d.write(struct.pack("<f", 0))
        d.write(struct.pack("<f", triangle.points[0].x))
        d.write(struct.pack("<f", triangle.points[0].y))
        d.write(struct.pack("<f", triangle.points[0].z))
        d.write(struct.pack("<f", triangle.points[1].x))
        d.write(struct.pack("<f", triangle.points[1].y))
        d.write(struct.pack("<f", triangle.points[1].z))
        d.write(struct.pack("<f", triangle.points[2].x))
        d.write(struct.pack("<f", triangle.points[2].y))
        d.write(struct.pack("<f", triangle.points[2].z))
        d.write(struct.pack("<h", 0))

def main():
    if len(sys.argv) != 3:
        print("Invalid arguments.")
        print("Usage : sapinisator.py source_file.stl destination_file.stl")
    else:
        source = sys.argv[1]
        dest = sys.argv[2]
        triangles = read_stl(source)
        triangles = sapinisation(triangles)
        stl_entete(source, dest)
        for t in triangles:
            stl_triangle(dest, t)

main()