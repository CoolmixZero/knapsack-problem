import csv


class KnapsackProblem:

    def __init__(self, n: int):
        self.items: list = []
        self.maxCapacity: int = 0
        self.filenames: dict = {
            0: "BoySchoolBackpack",
            1: "BoyTravelBackpack",
            2: "GirlSchoolBackpack",
            3: "GirlTravelBackpack"
        }
        if n not in self.filenames:
            raise KeyError(f'Filenames dict only have {tuple(self.filenames.keys())} as keys, your key: {n}')

        self.__init_data(self.filenames[n])

    def __len__(self) -> int:
        """
        :return: the number of items in the knapsack problem
        """
        return len(self.items)

    def capacity(self) -> int:
        """
        :return: capacity of the knapsack
        """
        return self.maxCapacity

    def __init_data(self, path: str) -> None:
        """initialize the data"""
        with open(f"./{path}.csv", 'r') as file:
            for i, row in enumerate(csv.reader(file)):
                if i == 0:
                    continue  # skip first row

                if len(row) == 1:
                    self.maxCapacity = int(row[0])
                    continue

                self.items.append((row[0], int(row[1]), int(row[2])))

    def getValue(self, evalList: list) -> float:
        """
        Calculates the value of the selected items in the list
        :param evalList: a list of 0/1 values corresponding to the list of the problem's items. '1' means that item was selected.
        :return: the calculated value
        """

        totalWeight = totalValue = 0

        for i in range(len(evalList)):
            item, weight, value = self.items[i]

            if totalWeight + weight <= self.capacity():
                totalWeight += evalList[i] * weight
                totalValue += evalList[i] * value

        return totalValue

    def printItems(self, evalList) -> None:
        """
        Prints the selected items in the list
        :param evalList: a list of 0/1 values corresponding to the list of the problem's items. '1' means that item was selected.
        """
        totalWeight = totalValue = 0
        ArrSkipping = []
        for i in range(len(evalList)):
            item, weight, value = self.items[i]
            if totalWeight + weight <= self.maxCapacity:
                if evalList[i] > 0:
                    totalWeight += weight
                    totalValue += value
                    print(
                        "- Adding {}: weight = {}, value = {}, accumulated weight = {}, accumulated value = {}".format(
                            item, weight, value, totalWeight, totalValue))
                else:
                    ArrSkipping.append(item)
        else:
            print("Done!")

        for i in ArrSkipping:
            print("- Skipping {}".format(i))

        print("- Total weight = {}, Total value = {}".format(totalWeight, totalValue))
