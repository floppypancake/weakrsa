
#!/usr/bin/python3

from math import gcd, sqrt
import random

# Global cache for memoization
factorization_cache = {}

def is_perfect_square(n):
    """Check if n is a perfect square."""
    root = int(sqrt(n))
    return root * root == n

def pollards_rho(n):
    """Pollard's Rho algorithm for factorization."""
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
    """Optimized factorization method with error handling, memoization, and Pollard's Rho."""
    # Error Handling for input
    if not isinstance(n, int) or n < 1:
        raise ValueError("Input must be a positive integer.")

    # Check cache
    if n in factorization_cache:
        return factorization_cache[n]

    # Handle small numbers directly
    if n < 2:
        return (n, 1)

    # Enhanced handling for even numbers
    if n % 2 == 0:
        factor = 2
        while n % factor == 0:
            n //= factor
        factorization_cache[n] = (n, factor)
        return (n, factor)

    a = int(sqrt(n))

    # Check for perfect square
    if is_perfect_square(n):
        factorization_cache[n] = (a, a)
        return (a, a)

    # Pollard's Rho for larger or difficult numbers
    factor = pollards_rho(n)
    if factor != n:
        factorization_cache[n] = (factor, n // factor)
        return (factor, n // factor)

    # Fallback to the original method if Pollard's Rho does not find a factor
    while True:
        a += 1
        b2 = a * a - n
        if is_perfect_square(b2):
            b = int(sqrt(b2))
            factorization_cache[n] = (a + b, a - b)
            return (a + b, a - b)

    # If no factors found, return n and 1
    factorization_cache[n] = (n, 1)
    return (n, 1)

def compute_private_key(phi_n, e):
    """Compute RSA private key given phi(N) and e."""
    # Extended Euclidean Algorithm to find modular inverse
    g, x, _ = extended_gcd(e, phi_n)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi_n

def extended_gcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def main():
    # Example RSA modulus (N) and public exponent (e)
    N = 289689326844881383964970734039648794403  # Example, typically N would be much larger
    e = 65537  # Common choice for e in RSA
    
    # Factorize N to find p and q
    try:
        p, q = factorize_optimized(N)
        print(f"Factors of N: p = {p}, q = {q}")
        
        # Compute phi(N)
        phi_n = (p - 1) * (q - 1)
        
        # Compute private exponent (d)
        d = compute_private_key(phi_n, e)
        print(f"Private key (d): {d}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
