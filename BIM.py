import random
import statistics
from disjoint_set import DisjointSet
from math import comb


# Network
edges_number = 30
nodes_number = 20
edges = (
    (1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11),
    (11, 12), (12, 13), (13, 14), (14, 15), (15, 6), (16, 17), (17, 18), (18, 19), (19, 20), (20, 16),
    (15, 16), (7, 17), (9, 18), (11, 19), (13, 20), (1, 8), (2, 10), (3, 12), (4, 14), (5, 6)
)

# Terminals:
T1 = 4
T2 = 10
T3 = 17

# Edge reliability
p_range=(0.4, 0.5, 0.6, 0.7, 0.8, 0.9)


# Check network model connectivity
def checkConnectivity(ds):
    return ds.connected(T1, T2) and ds.connected(T2, T3)



def calcSpectra(M):
    Z = [[0]*edges_number for i in range(edges_number)]
    Y = [0] * edges_number
    shuffledEdges = list(edges)

    for m in range(M):
        random.shuffle(shuffledEdges)
        ds = DisjointSet.from_iterable(range(1, nodes_number + 1))

        for r in range(1, edges_number + 1):
            ds.union(shuffledEdges[r-1][0], shuffledEdges[r-1][1])

            if checkConnectivity(ds):
                Y[r-1] += 1
                for j in range(1, edges_number + 1):
                    if edges[j-1] in shuffledEdges[:r]:
                        Z[r-1][j-1] += 1

    return [y/M for y in Y], [[zz/M for zz in z] for z in Z]

    

def calcBim(Y, Z, p):
    bim = [0] * edges_number
    q = 1 - p
    n = edges_number

    for j in range(1, edges_number + 1):
        for i in range(1, edges_number + 1):
            bim[j-1] += comb(n, i) * ((Z[i-1][j-1] * p**(i-1) * q**(n - i)) - ((Y[i-1] - Z[i-1][j-1]) * p**i * q**(n-i-1)))
            
    return bim



# 1, 2
print("\n#1")
cumulativeCS_1000, bimSpectrum_1000 = calcSpectra(1000)
cumulativeCS_10000, bimSpectrum_10000 = calcSpectra(10000)
print("Cumulative Destruction Spectra:")
print(" i M=1000 M=10000")
for i in range(edges_number - 1, -1, -1):
    print(f"{30 - i:>2} {cumulativeCS_1000[i]:>6} {cumulativeCS_10000[i]:>7}")



# 3
print("\n#3")

from precalculated import precalculated_BIM, precalculated_CCS

bimSpecSum = []
for n, i in enumerate(zip(*precalculated_BIM)):
    bimSpecSum.append((n+1, sum(i)))

# print("Groups by importance:")
# print("\t1: 17, 9, 3, 27, 4, 22, 10, 29, 16")
# print("\t2: 2, 23")
# print("\t3: 7, 5, 9, 30, 6, 1, 8, 11, 24, 21, 14, 28, 18, 26")
# print("\t4: 20, 13, 25, 19, 12, 15")


# Automatic clusterisation
from sklearn.cluster import KMeans
import numpy as np

num_groups = 4
edge_numbers = [i[0] for i in bimSpecSum]
data = np.array([i[1] for i in bimSpecSum])
data = data.reshape(-1, 1)

kmeans = KMeans(n_clusters=num_groups, random_state=42)
kmeans.fit(data)
cluster_labels = kmeans.labels_

clusters = [[] for _ in range(num_groups)]
for value, label, cluster in zip(data.flatten(), edge_numbers, cluster_labels):
    clusters[cluster].append((value, label))

sorted_clusters = sorted(clusters, key=lambda x: -np.mean([pair[0] for pair in x]))

print("Groups by importance:")
for i, cluster_data in enumerate(sorted_clusters):
    print(f"Group {i + 1} (mean: {np.mean([i[0] for i in cluster_data]):.3f}): {[i[1] for i in cluster_data]}")



a, b, c, d = [[i[0] for i in sorted(bimSpecSum, key=lambda x:x[1], reverse=True)][i] for i in [0,1,-1,-2]]

print("\nBIM Spectra for selected edges:")
print("            b e s t                w o r s t        ")
print(f"      edge {a:<2}     edge {b:<2}     edge {c:<2}     edge {d:<2}")
print(" i  1000 10000  1000 10000  1000 10000  1000 10000")

for i, line_1000, line_10000 in zip(range(1, edges_number+1), bimSpectrum_1000, bimSpectrum_10000):
    print(f"{i:>2}  ", end="")
    for row in (a, b, c, d):
        print(f"{line_1000[row-1]:>.2f} {line_10000[row-1]:>.3f}  ", end="")
    print()



# 4
print("\n#4")

print("BIMs and Gain in Reliability:")
print("                b e s t                        w o r s t        ")
print(" p   ", end="")
for i in a, b, c, d:
    print(f"{f'BIM({i})':7}", "BIM*dp  ", end="")
print()
for p in p_range:
    bim = calcBim(cumulativeCS_10000, bimSpectrum_10000, p)
    print(f"{p:>2}", end="")
    for i in a, b, c, d:
        if bim[i-1] >= 0:
            print(f"  {bim[i-1]:>.5f} {bim[i-1]*(1-p):>.4f}", end="")
        else:
            print(f"  {bim[i-1]:>.4f} {bim[i-1]*(1-p):>.3f}", end="")

    print()



#5
print("\n#5")

###############
# Monte Carlo #
###############

def generateStateVector(p, fail_edge=0, reliable_edge=0):
    res = []
    for i in range(edges_number):
        if i == fail_edge - 1:
            res.append(False)
        elif i == reliable_edge - 1:
            res.append(True)
        else:
            res.append(random.random() < p)

    return res

def generateNetwork(stateVector):
    ds = DisjointSet.from_iterable(range(1, nodes_number + 1))

    for i in range(0, edges_number):
        if stateVector[i]:
            ds.union(edges[i][0], edges[i][1])

    return ds

def calcReliabilityMonteCarlo(p, repetitions, fail_edge=0, reliable_edge=0):
    r = 0
    for j in range(repetitions):
        if checkConnectivity(generateNetwork(generateStateVector(p, fail_edge, reliable_edge))):
            r += 1
    return r/repetitions

def calcBIMcmc(p, repetitions, edge):
    return calcReliabilityMonteCarlo(p, repetitions, 0, edge) - calcReliabilityMonteCarlo(p, repetitions, edge, 0)



print("Gain in Reliability by means of CMC:")
print("             b e s t               w o r s t        ")
print(" p   ", end="")
for i in a, b, c, d:
    print(f"{f'BIM({i})*dp':>10}  ", end="")
print()

for p in p_range:
    print(f"{p:>2}", end="")
    for i in a, b, c, d:
        print(f"{(1-p)*calcBIMcmc(p, 10000, i):12.4f}", end="")
    print()
