def largest_prime(k: int) -> int:
    """
    Start off with list of len(k), filled with True. Then turn each True
    to False when it is determined by the algorithm that they are not prime.
    Finally, find the index of the last True element in the list, by
    iterating backwards.

    Input K: Integer
    Output: Closest prime number smaller than k.

    Time Complexity (Best and worst): O(n) where n is input k

    """
    assert 0 < k < 100000
    prime = [i for i in range(0, k)]    # Create a list of all values from 0 to k
    p = 2   # Start while loop from 2
    while p * p <= k - 1:   # Keep running loop until p*p is is bigger than or equal to k
        if prime[p]:
            for i in range(p ** 2, k, p):  # Set all multiples of p to False up to k
                prime[i] = False
        p += 1  # Increment p

    # Finding and returning the last element in prime list that is not False
    return list(filter(None, prime))[-1]

