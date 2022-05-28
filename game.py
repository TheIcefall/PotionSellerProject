"""
Authors: Gabriel Tucker, Leon Li, Junchi Wang, Le Nhat Minh
"""

from __future__ import annotations
# ^ In case you aren't on Python 3.10
from avl import AVLTree
from hash_table import LinearProbePotionTable
from potion import Potion
from random_gen import RandomGen


class Game:
    """
    This class plays the game for us!

    rand: random number seed

    potions_hash: This is a hash table where all potions available in game are stored for quick retrieval to look at
        details

    vendor_company_tree: This is where all potions in vendor inventory all stored in a tree, based on buy price.

    vendor_company_hash: This is a hash table where all potions available in vendor company inventory are stored for
        quick retrieval to look at details
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

        Complexity: O(N), where N is length potion_data
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
        This function adds potions to the inventory of the vendor corporation.

        potion_name_amount_pairs: Gives a list containing tuples, which provide data on the potion in: names of potion,
            litres to add to inventory


        Complexity: O(C * log(N)), where C is equal to length of potion_name_amount_pairs, and N is number of potions
            provided in set_total_potion_data.

        Complexity analysis:
            Why it is the complexity it is: This is O(C*log(n)) complexity due to the ADTs we have selected and
                used. The initial for loop is O(C) complexity, the most expensive operation in the loop, is adding
                elements to AVLTree: self.vendor_company_tree, which is O(log(n)). Hashing with our good hash method
                has an average complexity of linear time, O(1). Therefore the overall complexity of this function is
                O(C*log(n)). However, if the bad_hash function was used this would have a poorer time complexity.
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
            self.vendor_company_hash[
                key] = potion_attributes  # Add items to hash table for vendors, include litres of potion

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        This function chooses the potions which vendors will sell each day

        num_vendors: This represents the number of vendors that will play in the game

        Output: list of tuple(name of potion, how much potion)

        Complexity: O(C * log(N)) Where C is equal to num_vendors, and N is number of potions provided in set_total_potion_data.

        Complexity analysis:
            Why it is the complexity it is: The complexity is O(C*log(n)), when looking at the code, our while loop will
            until the length of the vendor company tree is 0, therefore, the complexity of this loop is O(C). Inside this
            loop, the most expensive function we have is deleting an item from the tree, and getting the kth largest item,
            both of these operations are O(log(n)). Additionally there is a for loop after the while loop. This loop
            adds the items back to the vendor tree with 0 quantity, it has several operations within it of log(n), but
            they are a set amount of operations and do not increase with the input size. The complexity of this loop is
            O(C*log(n)). This means the overall complexity is O(C*log(n)).
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

        # Add back to vendor inventory O(C*log(n))
        for i in range(len(output)):
            # Update vendor tree without litres O(log(n)
            item_without_litres = (output[i][0][0], 0)  # Updating tree for vendor corporation to have 0 litres
            self.vendor_company_tree[
                output[i][1]] = item_without_litres  # Updating tree for vendor corporation to have 0 litres

            # Update vendor hash without litres O(log(n)
            key = str(output[i][0][0])  # This is our hash key, the name of the potion
            hash_val = self.vendor_company_hash[key]
            hash_val.quantity = 0  # Set quantity of potions in vendor hash to be 0
            item_without_litres = self.vendor_company_hash[key]
            item_without_litres.quantity = 0
            self.vendor_company_hash[key] = item_without_litres

            output[i] = output[i][0]  # Set output to not include other fluff
        return output

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        """
        This function adds potions to an AVL tree, based on the profitability of buying and selling them. It then
            proceeds to iterate through the potions, buying as much as possible, and then going to the next potion,
            or day. It returns the maximum amount of money that can be made, by buying potions from PotionCorp, and
            selling potions to adventurers, on any given day, with a set amount of money.

        Args:
            potion_valuations: This is a list that shows the name of the potion, and how much the adventurers are
            willing to purchase for starting_money: This shows the players amount of money per day

        Returns: A list of the players total money at the end of each day played, indexed by day.

        Complexity: O(N*M + N*log(N)) Where N is length of potion_valuations, and M is the length of starting_money.

        Complexity analysis:
            This function has used the ADT of AVL tree, due to its self balancing nature, and ability
            to get a kth largest element with O(log(n)) complexity. The first for loop is of complexity N*log(n),
            as it runs N times, and each time an item is added to profit_tree, it costs O(log(N)). The overall complexity
            of the first loop is O(N * log(n)), where n is the amount of nodes in the tree. To keep this complexity we
            needed to retrieve the details of the items from self.vendor_company_hash, which is a hash table with the
            ability to access elements in constant time if a good hash function is used.

            The second loop is of complexity: The loop runs N times, each call to kth_largest is log(n).
            Therefore it runs O(N* log(n)) times. This takes every kth element and adds it to a regular list.
            This produces a sorted list of elements from most profitable to least profitable.

            Third loop complexity: The first loop runs M times, the second loop runs N times. Every operation within
            the second loop is constant. This means the overall complexity of this function is O(M*N)

            This gives us an overall complexity of O(2(N*log(n))+M*N) complexity, which ends up being O(N*M + N*log(N)).
        """
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
        # This section is O(n x m) complexity.
        profit_output = []
        profit_for_day = 0
        for i in range(len(starting_money)):  # O(m) complexity for this loop, if we disregard the nested loop.
            money_for_day = starting_money[i]
            for j in range(len(sorted_list_of_potions)):  # O(n) complexity, all lines in this loop are constant time
                if money_for_day == 0:
                    break
                if sorted_list_of_potions[j][0] > money_for_day:  # If there is more than I'm able to purchase
                    profit_for_day += money_for_day * sorted_list_of_potions[j][
                        1]  # Return amount I'm able to purchase times profit factor
                    break
                else:  # If player can purchase all of the potion that there is and still have leftover money
                    profit_for_day += sorted_list_of_potions[j][0] * sorted_list_of_potions[j][
                        1]  # Return amount available for purchase times profit factor
                    money_for_day -= sorted_list_of_potions[j][0]

            # Append profit made for day to output list
            profit_output.append(profit_for_day)
            profit_for_day = 0

        return profit_output
