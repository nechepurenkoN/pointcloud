from math import sin, cos, radians
import numpy as np
from enum import Enum, auto
import sys
import time
import hashlib
import argparse


class Direction(Enum):
    X = auto()
    Y = auto()
    Z = auto()


class PointCloud:
    """ Container for point cloud data"""

    __mtrx = {  # map from rotation axis to matrix
        Direction.X: lambda angle_: np.array([
            [1, 0, 0],
            [0, cos(angle_), -sin(angle_)],
            [0, sin(angle_), cos(angle_)]
        ]),
        Direction.Y: lambda angle_: np.array([
            [cos(angle_), 0, sin(angle_)],
            [0, 1, 0],
            [-sin(angle_), 0, cos(angle_)]
        ]),
        Direction.Z: lambda angle_: np.array([
            [cos(angle_), -sin(angle_), 0],
            [sin(angle_), cos(angle_), 0],
            [0, 0, 1]
        ])
    }

    def __get_rotation_matrix(self, direction, angle):
        """ Returns np.array to rotate above direction axis by angle degrees """

        angle = radians(angle)
        return self.__mtrx[direction](angle)

    def __init__(self, file_path):
        try:
            with open(file_path, "r") as f:
                self.__file_path = file_path
                self.__len = int(f.readline().strip())
                self.__title = f.readline().strip()
                self.__data = []
                for i in range(self.__len):
                    tok, x, y, z = f.readline().strip().split()
                    x, y, z = map(float, (x, y, z))
                    self.__data.append([np.array([x, y, z]), tok])
        except Exception as e:
            raise e

    def __rotate(self, matrix):
        for i in range(self.__len):
            self.__data[i][0] = matrix.dot(self.__data[i][0])

    def __repr__(self):
        return "\n".join(str((arr for arr, tok in self.__data)))

    def __iter__(self):
        return (arr for arr, tok in self.__data)

    def rotate_x(self, angle=45):
        r_matrix = self.__get_rotation_matrix(Direction.X, angle)
        self.__rotate(r_matrix)

    def rotate_y(self, angle=45):
        r_matrix = self.__get_rotation_matrix(Direction.Y, angle)
        self.__rotate(r_matrix)

    def rotate_z(self, angle=45):
        r_matrix = self.__get_rotation_matrix(Direction.Z, angle)
        self.__rotate(r_matrix)

    def save(self):
        hash_ = hashlib.sha1()
        hash_.update(str(time.time()).encode("utf-8"))
        filename = f"{self.__file_path}_{hash_.hexdigest()[:10]}.xyz"
        try:
            with open(filename, "w") as f:
                f.write(str(self.__len) + "\n")
                f.write(self.__title + "\n")
                for el in self.__data:
                    str_ = " "*(3-len(el[1]) if len(el[1])
                                < 3 else 0) + el[1] + " "
                    str_ += f"{el[0][0]:14.5f} {el[0][1]:14.5f} {el[0][2]:14.5f}"
                    f.write(str_ + "\n")

        except Exception as e:
            print(f"Save error: {e}")


def main():
    try:
        data = PointCloud(sys.argv[1])
    except Exception as e:
        print(f"Cannot make point cloud object: {e}")
        
    if len(sys.argv) < 3:
        data.rotate_x(45)
        data.rotate_y(45)
        data.rotate_z(45)
    else:
        sys.argv.remove(sys.argv[1])
        parser = argparse.ArgumentParser()
        parser.add_argument("-x", dest="x")
        parser.add_argument("-y", dest="y")
        parser.add_argument("-z", dest="z")
        results = parser.parse_args()

        if results.x is not None:
            data.rotate_x(float(results.x))
        if results.y is not None:
            data.rotate_y(float(results.y))
        if results.z is not None:
            data.rotate_z(float(results.z))

    try:
        data.save()
    except Exception as e:
        print(f"File saving error: {e}")


if __name__ == "__main__":
    main()
