import sys
import itertools
import more_itertools
import re
#import math
#import collections
#import networkx as nx
#from matplotlib import pyplot as plt

def parseLine(line,n):
    print(n,line)
    r1,r2 = line.split(" ")
    f2 = list(map(int,r2.split(",")))
    return r1,f2

def parseFile(filename):
    rows = []
    with open(filename,"r") as f:
        for l, line in enumerate(f):
            rows.append(parseLine(line.rstrip(),l))
    return rows

def mult5(row, records):
    return ((row+"?")*4+row, records*5)

def test_mult5():
    assert(mult5(".#", [1])) == (".#?.#?.#?.#?.#", [1,1,1,1,1])

def arrangements5(row, records):
    return arrangements(*mult5(row,records))

def arrangements(row,records):
    return cpa(row,records,0,0,0)

cache = {}

# credits to jonathanpaulson
def cpa(row,records,iro,ire,n):
    cache.clear()
    return _cpa(row,records,iro,ire,n)

def _cpa(row,records,iro,ire,n):
    key = (iro,ire,n)
    if key in cache:
        return cache[key]

    if iro == len(row):
        if ire == len(records) and n == 0:
            return 1
        elif iro == len(row) and ire == len(records)-1 and n == records[ire]:
            return 1
        else:
            return 0

    result = 0
    c = row[iro]
    if (c == '.' or c == '?')  and n ==0:
        result += _cpa(row,records,iro+1,ire,0)
    elif (c == '.' or c == '?') and ire < len(records) and records[ire] == n:
        result += _cpa(row,records,iro+1,ire+1,0)

    if c == "#" or c == "?":
        result += _cpa(row,records,iro+1,ire,n+1)

    cache[key] = result
    return result

if __name__ == "__main__":
    rows = parseFile(sys.argv[1])
    for row,rec in rows:
        print(arrangements5(row,rec),row,rec)

    print(sum(map(lambda l: arrangements5(*l),rows)))

X = -1 # dummy value
def test_arrangement_quand_arrive_au_bout():
    # quand on a plus de bloc attendu et qu'on n'est pas en train de comnsommer un noueau blocc
    assert cpa("012",[X,X],3,2,0) == 1
    # quand il ne reste qu'un bloc attendu et qu'il est pile poile de la taille du bloc en cours
    assert cpa("012",[X,2],3,1,2) == 1

def test_arrangement_on_arrive_sur_un_h_quand_le_bloc_consomme_est_encore_trop_petit():
    assert cpa("012##." ,[X,2],4,1,1) == 1

def test_arrangement_a_la_fin_quand_le_bloc_consomme_est_encore_trop_petit():
    assert cpa("0X#",[X,2],3,1,1) == 0
    
def test_arrangement_quand_on_depasse_la_taille_du_bloc_attendu():
    assert cpa("012XXX67",[X,2],4,1,2) == 0
    
def test_arrangement_tout_est_consomme_et_il_ne_reste_que_des_points_a_la_fin():
    assert cpa("01." ,[X,X],2,2,0) == 1
    assert cpa("01..",[X,X],2,2,0) == 1

def test_arrangement_tout_est_consomme_et_il_ne_reste_que_des_points_d_interrrogation_a_la_fin():
    assert cpa("01?" ,[X,X],2,2,0) == 1
    assert cpa("01?.",[X,X],2,2,0) == 1

def test_arrangement_on_consomme__un_bloc_encore_trop_petit_et_il_ne_reste_que_des_points_d_interrrogation_a_la_fin():
    #assert cpa("01#?" ,[X,X],2,2,0) == 1
    pass

def test_arrangement_on_arrive_a_la_fin_d_un_bloc_et_on_tombe_sur_un_point():
    # quand on a consommé pile poile le nombre de h attendus
    assert cpa("012.##." ,[X,2],6,1,2) == 1
    # quand on a consommé plus de h qu'attendus
    assert cpa("012.##." ,[X,1],6,1,2) == 0
    # quand on a consommé moins de h qu'attendus
    assert cpa("012.##." ,[X,3],6,1,2) == 0

def test_arrangement_on_arrive_a_la_fin_d_un_bloc_et_on_tombe_sur_un_point_d_interrrogation():
    # quand on a consommé pile poile le nombre de h attendus
    assert cpa("012.##?" ,[X,2],6,1,2) == 1
    # quand on a consommé plus de h qu'attendus
    assert cpa("012.##?" ,[X,1],6,1,2) == 0
    # quand on a consommé moins de h qu'attendus
    assert cpa("012.##?" ,[X,3],6,1,2) == 1


def test_arrangements5_1():
    assert arrangements5("???.###", [1,1,3]) == 1
def test_arrangements5_2():
    assert arrangements5(".??..??...?##.", [1,1,3]) == 16384
def test_arrangements5_3():
    assert arrangements5("?#?#?#?#?#?#?#?", [1,3,1,6]) == 1
def test_arrangements5_4():
    assert arrangements5("????.#...#...", [4,1,1]) == 16
def test_arrangements5_5():
    assert arrangements5("????.######..#####.", [1,6,5]) == 2500
def test_arrangements5_6():
    assert arrangements5("?###????????", [3,2,1]) == 506250

