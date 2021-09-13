from rich.console import Console
from rich.theme import Theme

class MyCustomPrint():
    THEMES = {
        "success": "bold green",
        "error": "bold red",
        "warning": "bold yellow",
        "info": "bold blue",
    }

    def __init__(self, statement="", style="info"):
        self.console = Console(theme=Theme(self.THEMES))
        self.statement = f"[SERVER]: {statement}"

        self.console.print(self.statement, style=self.THEMES.get(style))