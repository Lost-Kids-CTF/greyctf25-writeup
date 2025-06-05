from pwn import *
import json
from Cryptodome.Util.number import long_to_bytes, bytes_to_long

conn = remote("challs.nusgreyhats.org", 33301)
conn.recvline()
line = conn.recvline().decode()
p, g, y = list(map(int, line.strip().split(" ")))
k = int(conn.recvline().decode()[3:])
conn.recvuntil(b"> ")

def check(r: int, s: int):
    conn.sendline(b"1")
    conn.recvuntil(b": ")
    m = 137457664979133345092444721504268416885
    message = json.dumps({"m": m, "r": r, "s": s})
    conn.sendline(message.encode())
    result = conn.recvall()
    print(result)

def get_s(m: int):
    conn.sendline(b"2")
    conn.recvuntil(b": ")
    message = json.dumps({"m": m})
    conn.sendline(message.encode())
    s = int(conn.recvline().decode().strip().split(" ")[-1])
    return s

def find_x(m: int, s: int):
    sha = hashlib.sha256()
    sha.update(long_to_bytes(m))
    h = bytes_to_long(sha.digest())
    bracket = k * s % (p - 1)
    xr = (h - bracket) % (p - 1)
    # x = pow(r, -1, p - 1) * xr % (p - 1)
    x = solve_b(xr, r, p - 1)[0]
    return x

from math import gcd

def modinv(a, m):
    # Extended Euclidean Algorithm
    r0, r1 = a, m
    s0, s1 = 1, 0
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if r0 != 1:
        raise ValueError("Inverse doesn't exist")
    return s0 % m

def solve_b(a, c, p):
    d = gcd(c, p)
    if a % d != 0:
        return None  # No solution

    a_, c_, p_ = a // d, c // d, p // d
    try:
        c_inv = modinv(c_, p_)
    except ValueError:
        return None  # No inverse in reduced mod

    b0 = (a_ * c_inv) % p_
    solutions = [(b0 + k * p_) % p for k in range(d)]
    return solutions

r = pow(g, k , p)
h = 53524684929349800298924214995892606404300698151436239266694889122682528590455

m = 123
s = get_s(m)
x = find_x(m, s)

s = (h - x * r) * pow(k, -1, p - 1) % (p - 1)

check(r, s)
