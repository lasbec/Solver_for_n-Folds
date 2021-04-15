import numpy as np

np.seterr(all='warn')

def row(self, i):
    return self[i]

def col(self, i):
    return self[:,i]

def cols(self):
    return self.shape[1]

def rows(self):
    return self.shape[0]

def non_zero_entrys(A):
    count = 0
    for e in A:
        if e != 0:
            count += 1
    return count

def get_non_zero_index(A):
    for i in range(len(A)):
        if A[i] != 0:
            return i

def lcm_ignor_z(A):
    no_zs = np.array([e for e in A if e != 0], dtype=np.int64)
    return np.lcm.reduce(no_zs)

def gcd_ignor_z(A):
    no_zs = np.array([e for e in A if e != 0], dtype=np.int64)
    if no_zs != []:
        return np.gcd.reduce(no_zs)
    return 1


def scetch_entrys(A):
    if len(A.shape) == 1:
        return np.array([1 if e != 0 else e for e in A], dtype=np.int64)
    else:
        return np.array([scetch_entrys(r) for r in A], dtype=np.int64)

def swap_row(A, i, j):
    A = A.copy()
    A[[i,j]] = A[[j,i]]
    return A