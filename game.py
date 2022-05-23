from __future__ import annotations
# ^ In case you aren't on Python 3.10
from avl import AVLTree
from hash_table import LinearProbePotionTable
from potion import Potion
from random_gen import RandomGen


class Game:

    def __init__(self, seed=0) -> None:
        self.rand = RandomGen(seed=seed)
        self.potions_hash = None
        self.vendor_inventory_hash = None
        self.potions_tree = AVLTree()
        self.vendor_inventory_tree = AVLTree()
        self.random_generator = RandomGen()

    def set_total_potion_data(self, potion_data: list) -> None:
        """
        This sets the total potion data for the game, including price.

        Complexity: O(C * log(n))
        """
        # Need to set vendors potions to all in potion_data, at 0 litres
        self.potions_hash = LinearProbePotionTable(len(potion_data), True, -1)
        for i in range(len(potion_data)):
            key, potion_type, price = potion_data[i][0], potion_data[i][1], potion_data[i][
                2]  # Prepare to create empty potions
            data = Potion.create_empty(potion_type, key, price)  # Data = (Empty class of potion)
            self.potions_tree[price] = data  # Add empty potions to AVLTree based on price
            self.potions_hash.insert(key, data)  # Hash potions to hash table

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        input: [potion name, amount]
        Complexity: O(C * log(n))
        """
        for i in range(len(potion_name_amount_pairs)):
            key = potion_name_amount_pairs[i][0]
            potion_attributes = self.potions_hash[key]  # Find details about potion via key we are given
            litres = potion_name_amount_pairs[i][1]
            potion_attributes.quantity += litres  # Update val (potion) litres accordingly
            self.vendor_inventory_tree[potion_attributes.buy_price] = potion_name_amount_pairs[
                i]  # Set tree values in vendor inventory based on price

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        Output: list of tuple(name of potion, how much potion)
        """
        output = []
        for i in range(num_vendors, 0, -1):
            rand_int = self.random_generator.randint(i)
            val = self.vendor_inventory_tree.kth_largest(rand_int)
            output.append(val.item)  # Take the potion that is i'th most expensive and update tree
            self.vendor_inventory_tree.delete_aux(self.vendor_inventory_tree.root, val.key)  # Delete potion from tree
        return output

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        raise NotImplementedError()

    if __name__ == "__main__":
        g = Game()
        g.set_total_potion_data([["Potion of Health Regeneration", "Health", 20],
                                 ["Potion of Extreme Speed", "Buff", 10],
                                 ["Potion of Deadly Poison", "Damage", 45],
                                 ["Potion of Instant Health", "Health", 5],
                                 ["Potion of Increased Stamina", "Buff", 25],
                                 ["Potion of Untenable Odour", "Damage", 1]])
        # print(g.potions_hash)
        # print(g.potions_tree)

        g.add_potions_to_inventory([("Potion of Health Regeneration", 4),
                                    ("Potion of Extreme Speed", 5),
                                    ("Potion of Instant Health", 3),
                                    ("Potion of Increased Stamina", 10),
                                    ("Potion of Untenable Odour", 5)])

        print(g.vendor_inventory_tree[5])

        # selling = g.choose_potions_for_vendors(5)
