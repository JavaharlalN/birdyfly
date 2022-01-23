from numba import njit, prange
import random
from numpy import full
from sprites import im

def createLeaf(w, h):
    seed = random.choice(fib)
    c = complex((random.random() - 0.5) * 0.6, (random.random() - 0.5) * 0.6)
    spi = im.new(mode="RGB", size=(w, h), color=(0, 0, 255))
    spip = spi.load()
    for x in prange(w):
        for y in prange(h):
            z = complex((x - w / 2) / (w * 0.4), (y - w / 2) / (w * 0.4))
            z = (((z * z + c) ** 2 + c) ** 2 + c) ** 2 + c
            if abs(z) < 2:
                k = Noise(x / w, y / h, 5, seed, 0.99) + 0.5
                spip[x, y] = (int(30 * k), int(17 * k) * 15, 0)
    return spip

# def createLeaf(w, h):
#     seed = random.choice(fib)
#     c = complex((random.random() - 0.5) * 0.6, (random.random() - 0.5) * 0.6)
#     return get_spip(w, h, c, seed)


# @njit(fastmath=True, parallel=True)
# def get_spip(w, h, c, seed):
#     spip = [[(0, 0, 255)] * h] * w
#     for x in prange(w):
#         for y in prange(h):
#             z = complex((x - w / 2) / (w * 0.4), (y - w / 2) / (w * 0.4))
#             z = (((z * z + c) ** 2 + c) ** 2 + c) ** 2 + c
#             if abs(z) < 2:
#                 k = Noise(x / w, y / h, 5, seed, 0.99) + 0.5
#                 spip[x][y] = (int(30 * k), int(17 * k) * 15, 0)
#     return spip


@njit(fastmath=True)
def random_gradient(x, y, seed=1836311903):
    v = ((x * seed) ^ (y * 2971215073) + 4807526976) % 1023
    v = v % 3
    if v == 0:
        return [1, 0]
    elif v == 1:
        return [-1, 0]
    elif v == 2:
        return [0, 1]
    return [0, -1]

@njit(fastmath=True)
def q_curve(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

@njit(fastmath=True)
def lerp(a, b, t):
    return a + (b - a) * t

@njit(fastmath=True)
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

@njit(fastmath=True)
def simple_noise(fx, fy, seed=0):
    left = int(fx)
    top  = int(fy)
    p1x = fx - left
    p1y = fy - top

    v1 = random_gradient(left, top, seed)
    v2 = random_gradient(left + 1, top, seed)
    v3 = random_gradient(left, top + 1, seed)
    v4 = random_gradient(left + 1, top + 1, seed)

    d1 = [p1x, p1y]
    d2 = [p1x - 1, p1y]
    d3 = [p1x, p1y - 1]
    d4 = [p1x - 1, p1y - 1]

    tx1 = dot(d1, v1)
    tx2 = dot(d2, v2)
    bx1 = dot(d3, v3)
    bx2 = dot(d4, v4)

    p1x = q_curve(p1x)
    p1y = q_curve(p1y)

    tx = lerp(tx1, tx2, p1x)
    bx = lerp(bx1, bx2, p1x)
    return lerp(tx, bx, p1y)


@njit(fastmath=True)
def Noise(fx, fy, octaves, seed=1, amp=0.5):
    amplitude = 1
    max = 0
    result = 0

    while (octaves > 0):
        max += amplitude
        result += simple_noise(fx, fy, seed) * amplitude
        amplitude *= amp
        fx *= 2
        fy *= 2
        octaves -= 1

    return result / max


fib = (
    2, 3, 5,
    8, 13, 21,
    34, 55, 89,
    144, 233, 377,
    610, 987, 1597,
    2584, 4181, 6765,
    10946, 17711, 28657,
    46368, 75025, 121393,
    196418, 317811, 514229,
    832040, 1346269, 2178309,
    3524578, 5702887, 9227465,
    14930352, 24157817, 39088169,
    63245986, 102334155, 165580141,
    267914296, 433494437, 701408733,
    1134903170, 1836311903, 2971215073,
    4807526976, 7778742049, 12586269025,
    20365011074, 32951280099, 53316291173,
    86267571272, 139583862445, 225851433717,
    365435296162, 591286729879, 956722026041,
    1548008755920, 2504730781961, 4052739537881,
    6557470319842, 10610209857723, 17167680177565,
    27777890035288, 44945570212853, 72723460248141,
    117669030460994, 190392490709135, 308061521170129,
    498454011879264, 806515533049393, 1304969544928657,
    2111485077978050, 3416454622906707, 5527939700884757,
    8944394323791464, 14472334024676221, 23416728348467685,
    37889062373143906, 61305790721611591, 99194853094755497,
    160500643816367088, 259695496911122585, 420196140727489673,
    679891637638612258, 1100087778366101931, 1779979416004714189,
    2880067194370816120, 4660046610375530309, 7540113804746346429
)