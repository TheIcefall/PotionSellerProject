def largest_prime(k: int) -> int:
    def largest_prime(k: int) -> int:
    prime = [True for i in range(k)]
    p = 2
    while(p*p <= k - 1):
        if (prime[p] == True):
            for i in range(p**2, k, p):
                prime[i] = False
        p += 1
    prime[0] = False
    prime[1] = False
    for p in range(k - 1, -1, - 1):
        if prime[p] == True:
            return p
#print(largest_prime(10))
