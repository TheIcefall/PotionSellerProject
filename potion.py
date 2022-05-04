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
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """"""
        sum = 0
        for i in range(len(potion_name)):
            sum += ord(potion_name[i])*i
        hash_value = sum//tablesize
        return hash_value

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """"""
        sum = 0
        for i in range(len(potion_name)):
            sum += ord(potion_name[i])
        hash_value = sum//tablesize
        return hash_value

