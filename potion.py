from primes import largest_prime


class Potion:
    
    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity


    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        return cls(potion_type, name, buy_price, 0)


    @classmethod
    def good_hash(cls, potion_name: str = "", tablesize: int = 1) -> int:
        """"""
        value = 0
        a = largest_prime(10000)
        b = largest_prime(8000)
        for i in range(len(potion_name)):
            value = (ord(potion_name[i]) + a * value) % tablesize
            a = (a * b) % (tablesize - 1)
        return value

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """"""
        value = 0

        for i in range(len(potion_name)):
            value += (ord(potion_name[i])*i) % tablesize
        return value
