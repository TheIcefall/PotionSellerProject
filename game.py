from __future__ import annotations
# ^ In case you aren't on Python 3.10
from array_sorted_list import ArraySortedList
from avl import AVLTree
from hash_table import LinearProbePotionTable
from potion import Potion
from random_gen import RandomGen
from bst import BSTInOrderIterator


class Game:
    """
    This class plays the game for us!

    rand:
    potions_hash: This is a hash table where all potions available in game are stored for quick retrieval to look at details
    vendor_company_tree: This is where all potions in vendor inventory all stored in a tree, based on buy price.
    vendor_company_hash: This is a hash table where all potions available in vendor company inventory are stored for quick retrieval to look at details
    """

    def __init__(self, seed=0) -> None:
        """
        Initialisation
        """
        self.rand = RandomGen(seed=seed)
        self.potions_hash = None
        self.vendor_company_tree = AVLTree()
        self.vendor_company_hash = None


    def set_total_potion_data(self, potion_data: list) -> None:
        """
        This sets the total potion data for the game, including price.

        Complexity: O(len(potion_data))
        """
        # Need to set vendors potions to all in potion_data, at 0 litres
        self.potions_hash = LinearProbePotionTable(len(potion_data), True, -1)
        for i in range(len(potion_data)):
            key, potion_type, price = potion_data[i][0], potion_data[i][1], potion_data[i][
                2]  # Prepare to create empty potions
            data = Potion.create_empty(potion_type, key, price)  # Data = (Empty class of potion)
            self.potions_hash.insert(key, data)  # Hash potions to hash table

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        input: [potion name, amount]
        Complexity: O(C * log(n))
        """
        self.vendor_company_hash = LinearProbePotionTable(
            len(potion_name_amount_pairs))  # Initialise hash table for vendors
        for i in range(len(potion_name_amount_pairs)):
            key = potion_name_amount_pairs[i][0]
            potion_attributes = self.potions_hash[key]  # Find details about potion via key we are given
            litres = potion_name_amount_pairs[i][1]
            potion_attributes.quantity += litres  # Update val (potion) litres accordingly
            self.vendor_company_tree[potion_attributes.buy_price] = potion_name_amount_pairs[
                i]  # Set tree values in vendor inventory based on price
            self.vendor_company_hash[key] = potion_attributes  # Add items to hash table for vendors, include litres of potion

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        This function chooses the potions which vendors will sell each day

        num_vendors: This represents the number of vendors that will play in the game

        Output: list of tuple(name of potion, how much potion)

        Complexity: O(c * log(n))
        """
        output = []  # Initialise empty list to fill with potion names and values
        if num_vendors < 1:
            raise ValueError
        rand_gen = RandomGen()
        while self.vendor_company_tree.length != 0:  # Iterate backwards so that each time a potion is deleted, we can get the right size random int
            rand_num = rand_gen.randint(self.vendor_company_tree.length)
            kth_larg = self.vendor_company_tree.kth_largest(rand_num).key  # Get the kth_largest elements key
            output.append((self.vendor_company_tree[kth_larg], kth_larg))  # Add the tuple to output list
            del self.vendor_company_tree[kth_larg]  # Delete item from vendor inventory
        # Add back to vendor inventory
        for i in range(len(output)):
            self.vendor_company_tree[output[i][1]] = output[i]
            output[i] = output[i][0]
        return output

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        profit_tree = AVLTree()

        # This section is O(n*log(n))
        for i in range(len(potion_valuations)):  # Iterate through potions finding the profitability factor of given day
            # Checking if the potion is profitable
            key = potion_valuations[i][0]  # The name of the potion
            sell_price_vendor = self.vendor_company_hash[key].buy_price  # Retrieve price from vendor
            adventurer_buy_price = potion_valuations[i][1]  # What price will the adventurers buy at

            # Finding profit factor and storing in tree if it is profitable
            if sell_price_vendor < adventurer_buy_price:
                vendor_quantity = self.vendor_company_hash[key].quantity
                profit_factor = (
                            adventurer_buy_price / sell_price_vendor)  # Gives percentage of returns (gross profit) that will be made per unit purchased
                amount_purchasable = vendor_quantity * sell_price_vendor
                profit_tree[profit_factor, key] = [amount_purchasable, profit_factor, key]

        # Here is where we take the objects out of the tree, they will be sorted in the list now.
        # This section is O(n x log(n)) complexity
        sorted_list_of_potions = []
        for i in range(len(potion_valuations)):
            kth_largest = profit_tree.kth_largest(i + 1)
            sorted_list_of_potions.append(kth_largest.item)

        # Here is where we solve the puzzle, and find out how much money can be made
        # This section is O(n x m) complexity
        profit_output = []
        profit_for_day = 0
        for i in range(len(starting_money)):
            money_for_day = starting_money[i]
            for j in range(len(sorted_list_of_potions)):
                if money_for_day == 0:
                    break
                if sorted_list_of_potions[j][0] > money_for_day:  # If there is more than I'm able to purchase
                    profit_for_day += money_for_day * sorted_list_of_potions[j][
                        1]  # Return amount I'm able to purchase times profit factor
                    break
                else:  # If I can purchase all there is and still have leftover money
                    profit_for_day += sorted_list_of_potions[j][0] * sorted_list_of_potions[j][
                        1]  # Return amount available for purchase times profit factor
                    money_for_day -= sorted_list_of_potions[j][0]

            # Append profit made for day to output list
            profit_output.append(profit_for_day)
            profit_for_day = 0

        return profit_output
