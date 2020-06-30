"""
:Authors: CodeRevenge
:Version: 0.3 06-30-2020
"""
import os


class ProgressBar:
    """
    Create a progress bar for using in console.
    """

    def __init__(self, total: int = 100, character: str = "hash", load: int = 0,
                 colored=False, title_position: str = "left", show_numerical_advance: bool = True,
                 type: str = "percentage", numerical_advance_position: str = "right", extra_character: str = "",
                 limit_exception: bool = True):

        """
        :param int total: Set the final count.
        :param str character: (hash, block, dot) Set the fill character.
        :param str type: (percentage, division) Set the numerical count.
        :param int load: Set a initial progress value.
        :param bool colored: Use colors for loading bar. Colorama needed.
        :param str title_position: Set the title location.
        :param bool show_numerical_advance: Set if is needed to show the numerical advance.
        :param str numerical_advance_position: Use it to set the numerical position.
        :param str extra_character: Use a different character. If it is set, character will be ignored.
        :param bool limit_exception: In case of load greater than total use an Exception or pass the constrains.
        """

        valid_position = ["left", "right"]
        valid_booleans = [True, False]

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

        if colored not in valid_booleans:
            raise Exception(f"{colored} is not a valid option.")
        if colored:
            from colorama import init, Fore, Style
            init(autoreset=True)
            self.Fore = Fore
            self.Style = Style
        self.colored = colored

        if title_position not in valid_position:
            raise Exception(f"{title_position} is not a valid position.")
        self._title_position = title_position

        if numerical_advance_position not in valid_position:
            raise Exception(f"{numerical_advance_position} is not a valid position.")
        self._numerical_advance_position = numerical_advance_position

        if show_numerical_advance not in valid_booleans:
            raise Exception(f"{show_numerical_advance} is not a valid option.")
        self._show_numerical_advance = show_numerical_advance

        if len(extra_character) > 1:
            raise Exception(f"{extra_character} must be a character not a string literal.")
        elif len(extra_character) == 1:
            self._character = extra_character

        if limit_exception not in valid_booleans:
            raise Exception(f"{limit_exception} is not a valid option.")
        self._limit_exception = limit_exception

    def increase_progress_bar(self, amount: int = 1, title: str = ""):
        """ Increase and print the progress bar with the supplied amount.
        :param int amount: set de addition for the progress bar.
        """
        if amount > self._total and self._limit_exception:
            raise Exception("The load can not be major than the total.")
        self._load += amount
        self._print_bar(title)

    def print_error(self, title: str = "", error_title: str = ""):
        self._print_bar(title, True, error_title)

    def set_load(self, amount: int, title: str = ""):
        """ Set and print the progress bar with the supplied amount.
        :param int amount: set de value for the progress bar.
        """
        if amount > self._total and self._limit_exception:
            raise Exception("The load can not be major than the total.")
        self._load = amount
        self._print_bar(title)

    def set_total(self, total: int = 100):
        if total < self._load and self._limit_exception:
            raise Exception("The total can not be lower than the load.")
        if not isinstance(total, int):
            raise TypeError("Only integers are allowed.")
        self._total = total

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

            if total >= space:
                total = space
            bar = f"{color}{self._character * total}{' ' * (space - total)}{color_reset}"

            if self._show_numerical_advance:
                if self._type == "percentage":
                    load = f"{'%.2f' % percentage}%"
                elif self._type == "division":
                    load = f"{self._load}/{self._total}"

                if self._numerical_advance_position == "right":
                    return f"|{bar}| {load}"

                return f"{load} |{bar}|"
            return f"|{bar}|"

    def _print_bar(self, title, error: bool = False, error_title: str = ""):
        bar = self._get_progressBar(len(title))
        if self._title_position == "left":
            print(f"\r{title} {bar}", end="")
        else:
            print(f"\r{bar} {title}", end="")
        if error:
            print(f"\n{error_title}")


import time

if __name__ == '__main__':

    TOTAL = 100
    final = 500
    counter = 0

    pBar = ProgressBar(total=TOTAL, character="block", type="division", limit_exception=False)

    while (TOTAL < final):
        pBar.set_load(counter, title="Fetching")

        if counter == 98 or counter == 199:
            TOTAL = TOTAL * 2
            pBar.set_total(TOTAL)
        time.sleep(.001)
        counter += 1
        if counter >= final:
            break
