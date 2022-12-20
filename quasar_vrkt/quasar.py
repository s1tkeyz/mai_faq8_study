import math

G = 6.67 * 10**(-11)
M = 5.97 * 10**(24)
R = 6371000

dt = 1

t0 = 144
t1 = 315
t2 = 578
t3 = 615

m0 = 30000
m1 = 1500

def g(h):
    return (G * M) / (R + h)**2

def theta(t):
    if t < 16:
        return math.pi / 2
    elif (t >= 16) and (t <= 40):
        return (math.pi / 2) - ((t - 16) * math.pi / 90)
    elif(t > 40) and (t <= t0):
        return -math.pi / 6
    else:
        return math.pi / 2


def main()
    m = m0 + m1
    for t in range(0, 1200, dt):


if __name__ == '__main__':
    pass