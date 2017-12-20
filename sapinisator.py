#! /usr/bin/env python3

import struct

class Point:
    def __init__(self, x, y ,z):
        self.x = x
        self.y = y
        self.z = z

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

def read_stl(filename):
    with open(filename, "rb") as f:
        head = f.read(80)
        nbtriangles = f.read(4)
        print(nbtriangles)
        nbtriangles = struct.unpack("<I", nbtriangles)
        print(nbtriangles)
       
def main():
    read_stl("Schichtschwein_ohne_Logo.stl")