from __future__ import annotations
# ^ In case you aren't on Python 3.10
from avl import AVLTree
from hash_table import LinearProbePotionTable
from potion import Potion
from random_gen import RandomGen
from bst import BSTInOrderIterator

class Game:

    def __init__(self, seed=0) -> None:
        self.rand = RandomGen(seed=seed)
        self.potions_hash = None
        self.vendor_inventory_hash = None
        self.potions_tree = AVLTree()
        self.vendor_inventory_tree = AVLTree()
        self.random_generator = RandomGen()
        self.vendor_hash = None


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
            self.potions_hash.insert(key,data) # Hash potions to hash table


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
            self.vendor_inventory_tree[potion_attributes.buy_price] = potion_name_amount_pairs[i]  # Set tree values in vendor inventory based on price

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        Output: list of tuple(name of potion, how much potion)
        """
        k = 10
        self.vendor = []
        self.vendor_hash = LinearProbePotionTable(num_vendors)
        checked = []
        while len(checked) < num_vendors:
            rand_int = self.random_generator.randint(num_vendors - len(checked))

            if rand_int in checked:
                while rand_int in checked:
                    rand_int += 1
            checked.append(rand_int)
            val = self.vendor_inventory_tree.kth_largest(rand_int, self.vendor_inventory_tree.root)
            print(val)
            self.vendor.append(val.item)  # Take the potion that is i'th most expensive and update tree
            self.vendor_hash.insert(val.item[0], val.item[1])
        return self.vendor

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        arbit = AVLTree()
        potion_val_hash = LinearProbePotionTable(len(potion_valuations))
        sorted = []
        for i in range(len(potion_valuations)):
            data = self.potions_hash[potion_valuations[i][0]]
            sell_price = data.buy_price
            price_dif = potion_valuations[i][1] - sell_price
            potion_val_hash[potion_valuations[i][0]] = potion_valuations[i][1]
            if price_dif in arbit:
                arbit[price_dif].append(potion_valuations[i][0])
                continue
            arbit[price_dif] = [potion_valuations[i][0]]

        it = BSTInOrderIterator(arbit.root)
        for j in range(len(arbit)):
            key = it.__next__()
            item = arbit[key]
            if len(item) > 1:
                for i in range(len(item)):
                    sorted.append((item[i], key))
            else:
                sorted.append((item[0], key))
        result = []
        for k in range(len(starting_money)):
            money = starting_money[k]
            profit = 0
            curr = 1
            while money > 0:
                if money >= self.potions_hash[sorted[len(sorted) - curr][0]].buy_price * self.vendor_hash[sorted[len(sorted) - curr][0]]:
                    money -= self.potions_hash[sorted[len(sorted) - curr][0]].buy_price * self.vendor_hash[sorted[len(sorted) - curr][0]]
                    profit += self.vendor_hash[sorted[len(sorted) - curr][0]] * potion_val_hash[sorted[(len(sorted)) - curr][0]]
                elif money < self.potions_hash[sorted[len(sorted) - curr][0]].buy_price * self.vendor_hash[sorted[len(sorted) - curr][0]]:
                    profit += (money/self.potions_hash[sorted[len(sorted) - curr][0]].buy_price) * potion_val_hash[sorted[len(sorted) - curr][0]]
                    money = 0
                curr += 1
            result.append(profit)
        return result
