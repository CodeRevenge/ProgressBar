"""
:Authors: CodeRevenge
:Version: 0.1 06-29-2020
"""

class ProgressBar:
    """
    Create a progress bar for using in console.
    """

    def __init__(self, total: int = 100, character: str = "hash", type: str = "percentage", load: int = 0):
        """
        :param int total: Set the final count.
        :param str character: (hash, block, dot) Set the fill character.
        :param str type: (percentage, division) Set the numerical count.
        :param int load: Set a initial progress value.
        """
        if not isinstance(total, int):
            raise TypeError("Only integers are allowed.")
        self._total = total

        if character == "hash":
            self._character = "#"
        elif character == "block":
            self._character = "█"
        elif character == "dot":
            self._character = "·"
        else:
            raise Exception("Not valid character has been supplied.")

        if type == "percentage" or type == "division":
            self._type = type
        else:
            raise Exception("Not valid type has been supplied.")

        if not isinstance(load, int):
            raise TypeError("Only integers are allowed.")
        self._load = load

    def _get_progressBar(self):
        if self._type == "percentage":
            load = f"{self._load}%"
        elif self._type == "division":
            load = f"{self._load}/{self._total}"

        return f"\r|{self._character * self._load}{' ' * (self._total - self._load)}| {load}"

    def increase_progress_bar(self, amount: int = 1):
        """ Increase and print the progress bar with the supplied amount.
        :param int amount: set de addition for the progress bar.
        """
        self._load += amount;
        self.bar = self._get_progressBar()
        print(self.bar, end="")

    def set_load(self, amount: int):
        """ Set and print the progress bar with the supplied amount.
        :param int amount: set de value for the progress bar.
        """
        self._load = amount;
        self.bar = self._get_progressBar()
        print(self.bar, end="")


import time

if __name__ == '__main__':
    TOTAL = 20

    pBar = ProgressBar(total=TOTAL,character="block")

    for x in range(TOTAL+1):
        pBar.set_load(x)

        time.sleep(.1)
