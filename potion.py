"""
Author: Gabriel Tucker, Leon Li, Junchi Wang, Le Nhat Minh

This file allows us to create potion objects, to later use in game.py
"""

from primes import largest_prime


class Potion:
    """
    Potion

    attributes:
        potion_type: Type of potion object will be
        name: Name of potion
        buy_price: Buy price of potion
        quantity: Quantity of potion object will hold
    """
    
    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity


    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """
        This method creates an empty potion given 3 values: potion type, name, and buy price.

        Time Complexity (Best and worst): O(1)
        """
        return cls(potion_type, name, buy_price, 0)


    @classmethod
    def good_hash(cls, potion_name: str = "", tablesize: int = 1) -> int:
        """
        This method hashes a value, given a key to hash the value for, and a tablesize.
        This hash function attempts to give a unique value for each unique hash key given the table is not full,
            and does it's best to avoid collisions and conflicts.

        Time Complexity (Best and worst): O(potion_name)
        """
        value = 0
        a = largest_prime(10000)
        b = largest_prime(8000)
        for i in range(len(potion_name)):
            value = (ord(potion_name[i]) + a * value) % tablesize
            a = (a * b) % (tablesize - 1)
        return value

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        This method hashes a value, given a key to hash the value for, and a tablesize.

        This function does a poor job of producing unique hash values for each given key for the tablesize.

        Time complexity (Best and worst): O(potion_name)
        """
        value = 0

        for i in range(len(potion_name)):
            value += (ord(potion_name[i])*i) % tablesize
        return value
