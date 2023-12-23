import random
from math import *
import twocodes


def generate_code(K, eps, phi):
    P = []
    eps2 = eps
    index = 0
    while (phi * eps * K) >= 1:
        for i in range(1, ceil(phi * eps * K)):
            sampleSize = ceil(1 / eps)
            P += [random.sample(range(K+index), min(sampleSize, min(K + floor(K * phi * eps), K + index - 1)))]
            index += 1
        eps *= eps2
    return P

def encode(K, P, w):
    for i in P:
        s = sum([int(w[j]) for j in i])
        newBit = s % 2
        w += str(newBit)
    return w

def decode(K, P, y):
    unknown = [j for j, x in enumerate(y) if x == "?"]
    while len(unknown) != 0:
        changed = False
        for i in unknown:
            partitions = [x for x in P if i in x]
            for k in partitions:
                ind = int(P.index(k))
                if len([y[x] for x in k+[K+ind] if y[x] == "?"]) > 1:
                    continue
                s = sum([int(y[x]) for x in k+[K+ind] if y[x] != "?"])
                bit = s % 2
                y = y[0:i] + str(bit) + y[i + 1:]
                changed = True
                break
        unknown = [j for j, x in enumerate(y) if x == "?"]
        if len(unknown) > 0 and not changed:
            if "?" in y[0:K]:
                return None
            else:
                return y[0:K]
    return y[0:K]

def transmit(x, eps):
    x2 = ""
    for i in range(len(x)):
        if random.random() <= eps:
            x2 += "?"
        else:
            x2 += x[i]
    return x2



def testComplete(n, K, eps, phi):
    count = 0
    for i in range(n):
        w = ""
        for k in range(K):
            w += str(0) if random.random() < 0.5 else str(1)
        P = generate_code(K, eps, phi)
        encoded = encode(K, P, w)
        trans = transmit(encoded, eps)
        resp = decode(K, P, trans)
        if resp == w:
            count += 1
    return count / n
def testProf(n, eps, phi):
    K = [256,2048]
    P = [twocodes.P256,twocodes.P2048]
    count = 0
    r = []
    for k in range(len(K)):
        for i in range(n):
            w = ""
            for j in range(K[k]):
                w += str(0) if random.random() < 0.5 else str(1)
            encoded = encode(K[k], P[k], w)
            trans = transmit(encoded, eps)
            resp = decode(K[k], P[k], trans)
            if resp == w:
                count += 1
        r += [count/n]
        count=0
    return r
# print(testComplete(200,1024,0.1,10))
# print(testProf(200, 0.1, 4))