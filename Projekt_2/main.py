import time
from math import sin
import numpy as np


def jacobi(A, b):
    time0 = time.time()
    x = vec_zeros(len(A[0]))
    D = diag(A)
    R = A - diagflat(D)
    k = 0
    while True:
        x = (b - dot_product(R, x)) / D
        res = dot_product(A, x) - b
        if np.linalg.norm(res) < pow(10, -9):
            break
        k = k + 1
    print("Jacobi's method")
    print('time:', time.time()-time0)
    print('iterations:', k)
    return x, k


def gauss_seidel(A, b):
    time0 = time.time()
    k = 0
    L = np.tril(A)
    U = A - L
    x = vec_zeros(len(A[0]))
    while True:
        x = dot_product(np.linalg.inv(L), b - dot_product(U, x))
        res = dot_product(A, x) - b
        if np.linalg.norm(res) < pow(10, -9):
            break
        k += 1
    print("Gauss-cd pr   method")
    print("time:", time.time()-time0)
    print("iterations:", k)
    return x, k


def lu_factorization():
    pass


def vec_zeros(length):
    vec = []
    for _ in range(length):
        vec.append(0)
    return vec


def matrix_zeros(x, y):
    matrix = []
    for _ in range(y):
        row = []
        for _ in range(x):
            row.append(int(0))
        matrix.append(row)
    return matrix


def dot_product(A, B):
    # A - m*n matrix
    # B - vector n ints
    m = len(A)
    n = len(A[0])
    k = 1

    C = vec_zeros(m)

    for i in range(m):
        for l in range(n):
            C[i] += A[i][l] * B[l]
    return C


def diag(A):
    # A n*n matrix
    diag = []
    for i in range(len(A)):
        diag.append(A[i][i])
    return diag


def diagflat(vector):
    A = matrix_zeros(len(vector), len(vector))
    for i in range(len(vector)):
        A[i][i] = vector[i]
    return A


class Matrix:
    def __init__(self, index):
        self.read_index(index)
        self.create_default_matrixes()

    def create_default_matrixes(self):
        self.A = []
        self.B = []
        for i in range(self.N):
            row = []
            for j in range(self.N):
                if i == j:
                    row.append(int(5 + self.e))
                elif i - 2 <= j <= i + 2:
                    row.append(int(-1))
                else:
                    row.append(int(0))
            self.A.append(row)
            self.B.append(sin(i * (self.f + 1)))

    def read_index(self, index):
        self.f = int(index%10)
        index /= 10
        self.e = int(index%10)
        index /= 10
        self.d = int(index%10)
        index /= 10
        self.c = int(index%10)
        index /= 10
        self.b = int(index%10)
        index /= 10
        self.a = int(index)
        self.N = int(9 * self.c * self.d)

    def print_matrix(self):
        for row in self.A:
            print(row)


if __name__ == "__main__":
    matrix = Matrix(171619)
