import gmpy2 as gmp
import secrets


def genKey(size=4096):
    p = gmp.next_prime(secrets.randbits(int(size/2)))
    q = p
    while p == q:
        q = gmp.next_prime(secrets.randbits(int(size/2)))

    n = p * q
    m = gmp.lcm(p-1, q-1)

    e = gmp.mpz(65537)
    d = gmp.invert(e, m)

    return {"n": n, "e": e, "d": d}


def encrypt(num, exp, mod):
    return gmp.powmod(gmp.mpz(num, 16), exp, mod).digits(16)


def decrypt(num, exp, mod):
    return encrypt(num, exp, mod)
