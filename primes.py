def largest_prime(k: int) -> int:
    """
    Start off with list of len(k), filled with True. Then turn each True
    to False when it is determined by the algorithm that they are not prime.
    Finally, find the index of the last True element in the list, by
    iterating backwards.

    Input K: Integer
    Output: Closest prime number smaller than k.

    Complexity: O(n)
    """
    prime = [True for i in range(0, k)]
    prime[0] = False
    p = 2
    while p * p <= k - 1:
        if prime[p]:
            for i in range(p ** 2, k, p):
                prime[i] = False
        p += 1

    # Finding last element in prime list that is True
    for i in range(len(prime) - 1, 0, -1):
        if prime[i]:
            return i


if __name__ == "__main__":
    print(largest_prime(100))
