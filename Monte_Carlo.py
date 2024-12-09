import random
import statistics
from disjoint_set import DisjointSet

# Network
edges_number = 30
nodes_number = 20
edges = (
    (1, 2), (1, 5), (1, 8), (2, 3), (2, 10), (3, 4), (3, 12), (4, 5), (4, 14), (5, 6),
    (6, 7), (6, 15), (7, 8), (7, 17), (8, 9), (9, 10), (9, 18), (10, 11), (11, 12), (11, 19),
    (12, 13), (13, 14), (13, 20), (14, 15), (15, 16), (16, 17), (16, 20), (17, 18), (18, 19), (19, 20)
)

# Terminals
T1 = 4
T2 = 10
T3 = 17

# Repetitions
M1 = 1000
M2 = 10000


# Generate randomized state vector representing current state of network
def generateStateVector(p):
    res = []
    for i in range(edges_number):
        res.append(random.random() < p)

    return res

# Make network model in terms of DSS
def generateNetwork(stateVector):
    ds = DisjointSet.from_iterable(range(1, nodes_number + 1))

    for i in range(0, edges_number):
        if stateVector[i]:
            ds.union(edges[i][0], edges[i][1])

    return ds

# Check network model connectivity
def checkConnectivity(ds):
    return ds.connected(T1, T2) and ds.connected(T2, T3)


# Main flow

# Create table for different reliabilities
p_range=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99)

print(f"{'p':>4} {f'M={M1}':>7} {f'M={M2}':>8}")
for p in p_range:
    a = []
    for i in (M1, M2):
        r = 0
        for j in range(i):
            if checkConnectivity(generateNetwork(generateStateVector(p))):
                r += 1
        a.append(r / i)
    print(f"{p:>4} {a[0]:>7} {a[1]:>8}")
print()

# Calculate relative standard deviation for given p
p = 0.9

e = []
for i in range(5):
    r = 0
    for j in range(M1):
        if (checkConnectivity(generateNetwork(generateStateVector(p)))):
            r += 1
    e.append(r / M1)

print("Five runs:", e)
print("Relative standard deviation:", statistics.stdev(e) / statistics.mean(e))
