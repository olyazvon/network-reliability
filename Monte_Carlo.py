import random
import statistics
from disjoint_set import DisjointSet
edges_number = 30
nodes_number = 20
r=0
M1=1000
M2=10000
edges = (
(1, 2), (1, 5), (1, 8), (2, 3), (2, 10), (3, 4), (3, 12), (4, 5), (4, 14), (5, 6), (6, 7), (6, 15), (7, 8), (7, 17),
(8, 9), (9, 10), (9, 18),
(10, 11), (11, 12), (11, 19), (12, 13), (13, 14), (13, 20), (14, 15), (15, 16), (16, 17), (16, 20), (17, 18), (18, 19),
(19, 20))

#Terminals:
T1 = 4
T2 = 10
T3 = 17

def generateStateVector(p):
    res = []
    for i in range(1, nodes_number+1):
        res.append(random.random() < p)

    return res

def generateNetwork(stateVector):
    ds = DisjointSet.from_iterable(range(1, nodes_number+1))

    for i in range(1, nodes_number+1):
        if stateVector[i - 1]:
            ds.union(edges[i][0], edges[i][1])

    return ds

def checkConnectivity(ds):
    return ds.connected(T1, T2) and ds.connected(T2, T3)

#
# print(checkConnectivity(generateNetwork(generateStateVector(0.9))))
def generate(p):
    ds = DisjointSet.from_iterable(range(1, nodes_number+1))

    for edge in edges:
        if random.random() < p:
            ds.union(edge[0], edge[1])

        return ds


def checkConnectivity(ds):
    return ds.connected(T1, T2) and ds.connected(T2, T3)

p_range=(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99)

for p in p_range:
    a = []
    for i in (M1,M2):
        r = 0
        for j in range(i):
            if checkConnectivity(generateNetwork(generateStateVector(p))):
                r=r+1
        a.append(r/i)
    print(p,a)


#part e
e=[]
for i in range(1,6):
    if (checkConnectivity(generateNetwork(generateStateVector(0.9)))):
        e.append(1)
    else:
        e.append(0)
print(e)
print(statistics.stdev(e)/statistics.mean(e))
