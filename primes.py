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
    # Create a list of all values from 0 to k
    assert 0 < k < 100000
    prime = [i for i in range(0, k)]
    # Set 1 to False
    p = 2
    while p * p <= k - 1:
        if prime[p]:
            for i in range(p ** 2, k, p):
                prime[i] = False
        p += 1

    # Finding and returning the last element in prime list that is not False
    return list(filter(None, prime))[-1]


if __name__ == "__main__":
    print(largest_prime(100))
