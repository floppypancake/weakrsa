
#!/usr/bin/python3

from math import gcd, sqrt
import random

factorization_cache = {}

def is_perfect_square(n):
    # a perfect sqaure would be cool; without typing out a paragraph, let's just say it simplifies identifying the factors of n
    root = int(sqrt(n))
    return root * root == n

def pollards_rho(n):
    # shoutout pollard, prime numbers no longer scare me :)
    if n % 2 == 0:
        return 2
    x = random.randint(1, n-1)
    y = x
    c = random.randint(1, n-1)
    g = 1
    while g == 1:
        x = (x*x + c) % n
        y = (y*y + c) % n
        y = (y*y + c) % n
        g = gcd(abs(x-y), n)
    return g

def factorize_optimized(n):
    # memoization and error handling
    if not isinstance(n, int) or n < 1:
        raise ValueError("Input must be a positive integer.")

    # check cache
    if n in factorization_cache:
        return factorization_cache[n]

    # small little buggers
    if n < 2:
        return (n, 1)

    # modulus is such a weird word; why does everything come from Latin?
    if n % 2 == 0:
        factor = 2
        while n % factor == 0:
            n //= factor
        factorization_cache[n] = (n, factor)
        return (n, factor)

    a = int(sqrt(n))

    # check for perfect sqaure
    if is_perfect_square(n):
        factorization_cache[n] = (a, a)
        return (a, a)

    # i just wanted it to be easy, but sadly it was too difficult
    factor = pollards_rho(n)
    if factor != n:
        factorization_cache[n] = (factor, n // factor)
        return (factor, n // factor)

    # pollard wasn't good enough, let's try something else
    while True:
        a += 1
        b2 = a * a - n
        if is_perfect_square(b2):
            b = int(sqrt(b2))
            factorization_cache[n] = (a + b, a - b)
            return (a + b, a - b)

    # we are shit out of luck
    factorization_cache[n] = (n, 1)
    return (n, 1)

def compute_private_key(phi_n, e):
    # shoutout thomas@cryptostackexchange
    g, x, _ = extended_gcd(e, phi_n)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi_n

def extended_gcd(a, b):
    #i heart thomas
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def main():
    # give me them digits
    N = 289689326844881383964970734039648794403  
    e = 65537  
    
    # factorize this shit
    try:
        p, q = factorize_optimized(N)
        print(f"Factors of N: p = {p}, q = {q}")
        
        # compute this shit
        phi_n = (p - 1) * (q - 1)
        
        # also compute this shit
        d = compute_private_key(phi_n, e)
        print(f"Private key (d): {d}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
