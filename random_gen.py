"""
Author: Gabriel Tucker, Leon Li, Junchi Wang, Le Nhat Minh
"""

from typing import Generator


def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed


def check_nums(lst: list, index: int) -> bool:
    """
    This function returns a boolean expression that tells us if in list of objects, at least three of the objects have a 1, in index position 'index'.

    Complexity: O(1)
    """
    how_many_ones = 0
    for i in range(5):  # Iterate 5 times == length list
        if lst[i][index] == '1':
            how_many_ones += 1
            if how_many_ones == 3:
                break
    return how_many_ones == 3


class RandomGen:
    """
    This class allows us to generate random numbers that will change every time called in the same runtime.

    seed: the seed will be used by lcg function above
    rand_numb_iter: This is an iterator that will provide us with unique random numbers each time it is called
    """

    def __init__(self, seed: int = 0) -> None:
        """
        Initialisation
        """
        self.seed = seed
        self.rand_numb_iter = lcg(pow(2, 32), 134775813, 1, self.seed)

    def randint(self, k: int) -> int:
        """
        This method returns a random number between 0 and k

        Args:
            k: The random number output will be between 0 and k

        Returns: A random number between 0 and k

        Complexity: Best and worst O(1)

        """
        five_ran_nums = ["{:032b}".format((self.rand_numb_iter.__next__()))[:16] for i in
                         range(5)]  # Get 5 numbers from lcg() and transform them to 32 bit binary
        output_binary = ""

        for i in range(16):
            if check_nums(five_ran_nums, i):
                output_binary += "1"
            else:
                output_binary += "0"

        return int(output_binary, 2) % k + 1


