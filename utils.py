import os
import pyfiglet

class Utils:
    @staticmethod
    def clear_screen():
        """Clears the entire console screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    # http://www.figlet.org/examples.html
    def CreateAsciiText(text: str="Ascii Text", width: int=1250, selected_font: str="big"):
        ShowText = pyfiglet.figlet_format(
            text, font=selected_font, width=width)
        return f"{ShowText}"