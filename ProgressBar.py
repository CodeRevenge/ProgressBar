"""
:Authors: CodeRevenge
:Version: 0.2 06-29-2020
"""
import os


class ProgressBar:
    """
    Create a progress bar for using in console.
    """

    def __init__(self, total: int = 100, character: str = "hash", type: str = "percentage", load: int = 0,
                 colored=False):
        """
        :param int total: Set the final count.
        :param str character: (hash, block, dot) Set the fill character.
        :param str type: (percentage, division) Set the numerical count.
        :param int load: Set a initial progress value.
        :param bool colored: Use colors for loading bar. Colorama needed.
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

        if type == "percentage":
            self._type = type
            self._count = len(str(total)) + 1;
        elif type == "division":
            self._type = type
            self._count = len(str(total)) * 2 + 1;
        else:
            raise Exception("Not valid type has been supplied.")

        if not isinstance(load, int):
            raise TypeError("Only integers are allowed.")
        self._load = load

        if colored:
            from colorama import init, Fore, Style
            init(autoreset=True)
            self.Fore = Fore
            self.Style = Style
        self.colored = colored

    def _get_color(self, load: int = 0, error: bool = False) -> str:
        if error:
            return self.Fore.LIGHTRED_EX

        if load <= 33:
            return self.Fore.RED + self.Style.BRIGHT
        elif load <= 66:
            return self.Fore.YELLOW + self.Style.BRIGHT
        elif load <= 99:
            return self.Fore.GREEN + self.Style.BRIGHT
        elif load >= 100:
            return self.Fore.CYAN + self.Style.BRIGHT

    def _get_progressBar(self, title_len: int = 0, error: bool = False):
        try:
            terminal_columns = os.get_terminal_size().columns
        except:
            terminal_columns = 150
        finally:
            space = terminal_columns - self._count - 8 - title_len;
            percentage = 100 / self._total * self._load
            total = int((space / self._total) * self._load)

            color = ""
            color_reset = ""
            if self.colored:
                color_reset = self.Style.RESET_ALL
                color = self._get_color(int(percentage), error)

            bar = f"{color}{self._character * total}{' ' * (space - total)}{color_reset}"

            if self._type == "percentage":
                load = f"{'%.2f' %percentage}%"
            elif self._type == "division":
                load = f"{self._load}/{self._total}"

            return f"|{bar}| {load}"

    def increase_progress_bar(self, amount: int = 1, title: str = ""):
        """ Increase and print the progress bar with the supplied amount.
        :param int amount: set de addition for the progress bar.
        """
        self._load += amount
        NAME = self._get_progressBar(len(title))
        print(f"\r{title} {NAME}", end="")

    def print_error(self, title: str = ""):
        NAME = self._get_progressBar(len(title), error=True)
        print(f"\r{title} {NAME}", end="")
        print(f"\nError in {title}")

    def set_load(self, amount: int, title: str = ""):
        """ Set and print the progress bar with the supplied amount.
        :param int amount: set de value for the progress bar.
        """
        self._load = amount
        NAME = self._get_progressBar(len(title))
        if NAME == "":
            print("ok")
        print(f"\r{title} {NAME}", end="")


import time

if __name__ == '__main__':

    TOTAL = 360

    pBar = ProgressBar(total=TOTAL, character="hash", colored=True, type="division")

    for x in range(TOTAL + 1):
        pBar.set_load(x, title="Loading")

        # if x == 800:
        #     pBar.print_error("Fetching")
        #     break
        time.sleep(.001)
