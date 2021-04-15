import numpy as np
import os
from copy import deepcopy

from random import randint
from utils import *

# from sys import argv
import argparse


np.seterr(all="warn")

warn_flg = False
debug_lvl = 3

DEBUG = 0
VERBOSE = 1
INFO = 2
WARN = 3
ERROR = 4

def _message(level, *args):
    global debug_lvl
    if level >= debug_lvl: print(*args)

def debug(*args):
    _message(DEBUG  , "DEBUG:  " ,*args)

def verb(*args):
    _message(VERBOSE, "VERBOSE: " ,*args)

def info(*args):
    _message(INFO, "INFO: " ,*args)

def warn(*args):
    _message(WARN   , "WARN:    " ,*args)

def error(*args):
    _message(ERROR  , "ERROR:   " ,*args)




def reduce_mat(A):
    A = deepcopy(A)
    c = 0
    total_c = 0
    verb(f"A: \n{A}")
    deleteted_col_indexs = []
    while c < rows(A) and c < cols(A):
        debug(f"-----------------------------total_c: {total_c}")
        
        if A[c][c] == 0:
            if get_non_zero_index(A[c]) is None:
                A = np.delete(A, c, 0)
                debug(f"&@# delete row {c}\n{A}")
                verb(f"\nsketch del row {c}\n{scetch_entrys(A)}")
                continue
            elif get_non_zero_index(col(A,c)[c:]) is None:
                A = np.delete(A, c, 1)
                deleteted_col_indexs.append(total_c)
                debug(f"&@# delete col {c}\n{A}")
                verb(f"\nsketch del col {c}\n{scetch_entrys(A)}")
                total_c += 1
                continue
            else:
                nzi = c + get_non_zero_index(col(A,c)[c:])
                A = swap_row(A, c, nzi)
                verb(f"\n<-> swap {c},{nzi}")
                debug(A)
                verb(f"\nsketch swap\n{scetch_entrys(A)}")
                total_c += 1
            


        scm = lcm_ignor_z(col(A, c))
        if scm <= 0:
            error("Numpy Overflow on lcm")
            global warn_flg
            warn_flg = True
        debug(f"col(A,{c}) {col(A,c)}")
        for r in range(rows(A)):
            if(col(A,c)[r] != 0):
                A[r] *= scm//(col(A,c)[r])

        debug(f"\n*** multiply{scm}\n{A}")
        verb(f"\nsketch mul\n{scetch_entrys(A)}")
        
        
        for r in range(rows(A)):
            if r != c:
                if(col(A,c)[r] != 0):
                    A[r] -= row(A, c)
        debug(f"\n--- subtract\n{A}")
        verb(f"\nsketch substrac\n{scetch_entrys(A)}")
        

        for r in range(rows(A)):
            debug(f"{r} A[r]: {A[r]}")
            debug(f"{r} gcd: {gcd_ignor_z(A[r])}")
            A[r] = A[r]/(gcd_ignor_z(A[r]))
        debug("\n::: devide\n", A)
        verb(f"\nsketch div\n{scetch_entrys(A)}")

        c += 1
    

    A = A[:c]
    debug(f"retduced: \n{A}")
    verb(f"\nsketch retduced\n{scetch_entrys(A)}")
    debug(f"\n deleted_cols: {deleteted_col_indexs}")
        
    return A, deleteted_col_indexs


def solve_int_gen(A, lower, upper):    
    red_A, deleted_cols = reduce_mat(A)
    info("Instanciated solution generator")

    while True:
        A = deepcopy(red_A)
        
        A_front = np.array([A[i][i] for i in range(rows(A))], dtype=np.int64) # Diagonale
        A_back = A[:,rows(A):]

        debug("A Back (shape): ",A_back.shape)
        debug("A Back :\n ",A_back)
        if A_back.shape[1] == 0:
            yield np.array([ (randint(lower, upper) if i in deleted_cols else 0)
                             for i in range(len(deleted_cols) + cols(A))
                           ], dtype=np.int64)
            continue
        

        back_vec = np.array([randint(lower, upper) for _ in range(cols(A_back))],dtype=np.int64)
        verb("back_vec init:", back_vec)
        front_vec = np.array([0 for _ in range(len(A_front))], dtype=np.int64)

        for i,f in enumerate(A_front):
            acc = np.dot(np.transpose(back_vec), A_back[i])
            verb(f"{i} acc: {acc}")

            if acc == 0:
                front_vec[i] = 0
            else:
                scm = lcm_ignor_z([acc, f])
                verb(f"{i} scm: ", scm)

                back_fac  = int(scm/acc)
                front_fac = int(scm/f)
                
                back_vec  = back_vec  * back_fac
                front_vec = front_vec * back_fac
                front_vec[i] = -front_fac
            
            debug(f"{i} front_vec:\n  {front_vec}")
            debug(f"{i} back_vec:\n  {back_vec}")

        ret = np.concatenate((front_vec, back_vec))
        ggt = int(gcd_ignor_z(ret))
        verb("pure ret:\n", ret)
        
        ret_lst = []
        r_c = 0
        debug(f"cols(A) + len(deleted_cols) {cols(A) + len(deleted_cols)}")
        for i in range(cols(A) + len(deleted_cols)):
            if i in deleted_cols:
                ret_lst.append(randint(lower,upper))
            else:
                ret_lst.append(ret[r_c])
                r_c += 1

        ret = np.array(ret_lst, dtype=np.int64)
        verb("hole ret")

        yield ret


def qualety_check(test, delta, zeros_ok=False):
    n, r, s, t, l, u, b, c, As, Bs, feasables = test
    info("\n\n\n:::BEIGN: check Test:::")
    info(f"n: {n}, r: {r}, s: {s}, t: {t}\n")
    info(f"l:\n{l}\n")
    info(f"u:\n{u}\n")
    info(f"b:\n{b}\n")
    info(f"c:\n{c}\n")
    for i in range(len(As)):
        info(f"A_{i}:\n{As[i]}\n")
    for i in range(len(Bs)):
        info(f"B_{i}:\n{Bs[i]}\n")
    info("----------------\nFEASABLES:")
    for f in feasables:
        info(f)
    info("____________________________________")

    hole_mat = hole_matrix(As, Bs)

    for f in feasables:
        if (b != np.dot(hole_mat, f)).any():
            error("Discarded feasabilety violated")
            exit()
            return False
    
    for f in feasables:
        if not np.logical_and.reduce(f <= u):
            warn("Discarded bounds violated")
            return False
        if not np.logical_and.reduce(l <= f):
            warn("Discarded bounds violated")
            return False
    
    if np.maximum.reduce(np.maximum.reduce(abs(hole_mat))) > delta:
        warn("Discarted: delta")
        return False

    if not zeros_ok:
        flag = False
        for B in Bs:
            if  np.maximum.reduce(np.maximum.reduce(abs(B))) != 0:
                flag = True
        if not flag:
            warn("Discarded: Bs zero")
            return False

    global warn_flg
    if warn_flg:
        warn("Discarded warn flag set")

    info(":::END: check Test::: (passed)\n\n\n")
    return True


def new_test(inp):
    n = inp.n
    r = inp.r
    s = inp.s
    t = inp.t


    tfs = [
        np.array([randint(inp.min_bounds, inp.max_bounds) for _ in range(n*t)], dtype=np.int64)
        for _ in range(inp.f_num)
    ]

    # Make As
    lin_sys = np.array([tfs[i]-tfs[(i+1)%len(tfs)] for i in range(len(tfs))], dtype=np.int64)
    solsAs = solve_int_gen(lin_sys, inp.min_mat, inp.max_mat)
    As_on_block = np.array([next(solsAs) for _ in range(r)], dtype=np.int64)
    As = []
    for i in range(n):
        beg = i*t
        end = beg + t 
        As.append(As_on_block[:, beg: end])
        debug(f"A split{i}: {beg};{end}\n {As_on_block[:, beg: end]}")


    # Make Bs
    Bs = []
    for i in range(n):
        beg = i*t
        end = beg + t 
        constrained_lin_sys = lin_sys[:, beg: end]
        solsB = solve_int_gen(constrained_lin_sys, inp.min_mat, inp.max_mat)
        debug (f"const lin:\n {constrained_lin_sys}\n")
        Bs.append(np.array([next(solsB) for _ in range(s)], dtype=np.int64))
        debug(f"B_{i}: {beg};{end}\n {Bs[-1]}")
    
    # make Vectors
    c = np.array([randint(inp.min_c, inp.max_c) for _ in range(n*t)], dtype=np.int64)
    b = np.dot(hole_matrix(As, Bs), tfs[0])
    u = np.maximum.reduce(tfs) + np.array([1 for _ in range(n*t)])
    l = np.minimum.reduce(tfs) - np.array([1 for _ in range(n*t)])


    return n, r, s, t, l, u, b, c, As, Bs, tfs


def hole_matrix(As, Bs):
    n = len(As)
    t = cols(As[0])
    s = rows(Bs[0])
    hole_mat = np.concatenate(As, 1)
    debug(f"hole_mat\n{hole_mat}")
    for i, B in enumerate(Bs):
        debug(f"\nB:\n{B}")
        extB = B

        befB = np.array([[0 for _ in range(i*t)] for _ in range(s)], dtype=np.int64)
        if befB.shape[1] != 0:
            extB = np.concatenate((befB,extB),1)

        aftB = np.array([[0 for _ in range((n-i-1)*t)] for _ in range(s)], dtype=np.int64)
        if aftB.shape[1] != 0:
            extB = np.concatenate((extB,aftB),1)
        debug(f"ext_b\n {extB}")
        
        hole_mat = np.concatenate((hole_mat, extB), 0)
        debug(f"hole_mat\n{hole_mat}")
    return hole_mat


def write_test_case(full_path, test):
    n, r, s, t, l, u, b, c, As, Bs, _ = test

    dir_path = "\\".join(full_path.split("\\")[:-1])
    if not os.path.isdir(dir_path):
        os.makedirs (dir_path)
    
    with open(full_path, "w") as file:
        file.write(f"{n} {r} {s} {t}\n")
        debug("write: ", f"{n} {r} {s} {t}\n")
        file.write(' '.join([str(e) for e in l]) + "\n")
        debug("write: ", ' '.join([str(e) for e in l]) + "\n")
        file.write(" ".join([str(e) for e in u]) + "\n")
        debug("write: ", " ".join([str(e) for e in u]) + "\n")
        file.write(' '.join([str(e) for e in b]) + '\n')
        debug("write: ", ' '.join([str(e) for e in b]) + '\n')
        file.write(" ".join([str(e) for e in c]) + "\n")
        debug("write: ", " ".join([str(e) for e in c]) + "\n")
        for A in As:
            file.write(" ".join([str(e) for e in np.concatenate(A,0)] )+ "\n")
            debug("write: ", " ".join([str(e) for e in np.concatenate(A,0)] )+ "\n")
        for B in Bs:
            file.write(" ".join([str(e) for e in np.concatenate(B,0)] )+ "\n")
            debug("write: ", " ".join([str(e) for e in np.concatenate(B,0)] )+ "\n")
    info(f"Matrix:\n {hole_matrix(As, Bs)} ")
    info("Test written to: ", full_path)
        


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="Number of Blocks", type=int)
    parser.add_argument("r", help="Height of A matricies", type=int)
    parser.add_argument("s", help="Height of B matricies", type=int)
    parser.add_argument("t", help="Width of A and B matricies", type=int)

    parser.add_argument("min_mat", help="Possible random values for matrix entrys", type=int)
    parser.add_argument("max_mat", help="Possible random values for matrix entrys", type=int)

    parser.add_argument("--min_bounds", help="Limits the bound entrys", type=int
                        , default=-4)
    parser.add_argument("--max_bounds", help="Limits the bound entrys", type=int
                        , default=4)

    parser.add_argument("--min_c", help="Limits the c entrys", type=int
                        , default=-10)
    parser.add_argument("--max_c", help="Limits the c entrys", type=int
                        , default=10)

    parser.add_argument("--delta", help="Limits the entrys of the As and Bs", type=int
                       , default=20)
    
    parser.add_argument("path", help="This will be used as prefix where to store the cases", type=str)
    parser.add_argument("--postfix", help="Postfix for case files"
                        , type=str
                        , default=".in")

    parser.add_argument("cases", help="Number of cases to be generated"
                       , type=int)
    parser.add_argument("--f_num", help="The number of preset feasables that will be set to generate cases"
                       , type=int
                       , default=3)

    parser.add_argument("--zeros_ok", help="Its ok when all Bs are zero"
                       , type=int
                       , default=0)

    parser.add_argument("--debug", help="Debuglevel"
                       , type=int
                       , default=3)

    inp = parser.parse_args()
    
    global debug_lvl
    debug_lvl = inp.debug

    test_cases_written = 0
    test_case_num = inp.cases

    while test_cases_written < test_case_num:
        global warn_flg
        warn_flg = False
        # try:
        info(f"Try generating. Test cases left to generate {test_case_num - test_cases_written}")
        test = new_test(inp)
        # except Exception as e:
        #     error("Test generating failed with error: ", e)
        # else:
        if qualety_check(test, inp.delta, inp.zeros_ok != 0):
            file_path = inp.path + str(test_cases_written) + inp.postfix
            write_test_case(file_path, test)
            test_cases_written +=1
            



main()

