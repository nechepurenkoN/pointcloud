from math import sin, cos, radians
import numpy as np
from enum import Enum, auto
import sys

class Direction(Enum):
    X = auto()
    Y = auto()
    Z = auto()

mtrx = {
    Direction.X: lambda angle_: np.array([
        [1, 0, 0],
        [0, cos(angle_), -sin(angle_)],
        [0, sin(angle_), cos(angle_)]
    ]),
    Direction.Y: lambda angle_: np.array([
        [cos(angle_), 0, -sin(angle_)],
        [0, 1, 0],
        [sin(angle_), 0, cos(angle_)]
    ]),
    Direction.Z: lambda angle_: np.array([
        [cos(angle_), -sin(angle_), 0],
        [sin(angle_), cos(angle_), 0],
        [0, 0, 1]
    ])
}

def get_rotate_matrix(direction, angle):
    """ Returns np.array to rotate above direction axis by angle degrees """

    angle = radians(angle)
    return mtrx[direction](angle)



class PointCloud:
    """ Container for point cloud data"""

    def __init__(self, file_path):
        try:
            with open(file_path, "r") as f:
                self.__len = int(f.readline())
                self.__title = f.readline()
                self.__data = []
                for i in range(self.__len):
                    tok, x, y, z = f.readline().strip().split()
                    x, y, z = map(double, (x, y, z))
                    self.__data.append((np.array(x,y,z), tok))
        except Exception as e:
            raise e

    def rotate(self, matrix):
        for i in range(self.__len):
            self.__data[i][0] = matrix.dot(self.__data[i][0])

    def __repr__(self):


    def rotate_x(self, angle=45):
        r_matrix = get_rotate_matrix(Direction.X, angle)
        self.rotate(r_matrix)

    def rotate_y(self, angle=45):
        r_matrix = get_rotate_matrix(Direction.Y, angle)
        self.rotate(r_matrix)

    def rotate_z(self, angle=45):
        r_matrix = get_rotate_matrix(Direction.Z, angle)
        self.rotate(r_matrix)

    


def main():
    try:
        data = PointCloud(sys.argv[1])
    except Exception as e:
        print(f"Error: {e}")
    if len(sys.argv) < 3:
        pass


if __name__ == "__main__":
    main()
