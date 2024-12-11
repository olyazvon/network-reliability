import random
import statistics
from disjoint_set import DisjointSet
from math import comb

# Network
edges_number = 30
nodes_number = 20
edges = (
    (1, 2), (1, 5), (1, 8), (2, 3), (2, 10), (3, 4), (3, 12), (4, 5), (4, 14), (5, 6),
    (6, 7), (6, 15), (7, 8), (7, 17), (8, 9), (9, 10), (9, 18), (10, 11), (11, 12), (11, 19),
    (12, 13), (13, 14), (13, 20), (14, 15), (15, 16), (16, 17), (16, 20), (17, 18), (18, 19), (19, 20)
)

# Terminals:
T1 = 4
T2 = 10
T3 = 17

def checkConnectivity(ds):
    return ds.connected(T1, T2) and ds.connected(T2, T3)

def generateConstructionSpectrum(M):
    res = [0] * edges_number
    tmpEdges = list(edges)
    for m in range(M):
        random.shuffle(tmpEdges)
        ds = DisjointSet.from_iterable(range(1, nodes_number + 1))
        for i in range(edges_number):
            ds.union(tmpEdges[i][0], tmpEdges[i][1])
            if checkConnectivity(ds):
                res[i] += 1
                break
    return [i / M for i in res]

def generateDestructionSpectrum(M):
    return generateConstructionSpectrum(M)[::-1]

def binomialProbability(n, k, p):
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

def calculateReliability(dSpectrum, p):
    cumulativeSpectrum = [sum(dSpectrum[0:i + 1]) for i in range(len(dSpectrum))]
    res = 0
    for i in range(1, len(dSpectrum) + 1):
        res += binomialProbability(edges_number, i, 1 - p) * cumulativeSpectrum[i - 1]
    return 1 - res


print(generateDestructionSpectrum(10000))
print(calculateReliability(generateDestructionSpectrum(10000), 0.5))
