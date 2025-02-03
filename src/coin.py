from typing import Callable, Optional
from dataclasses import dataclass, field
import functools
from src.logger import log

@dataclass
class Coin:
    c: str
    o: Optional[str] = None
    i: Optional[str] = None
    n: Optional[str] = None
    s: Optional[str] = None

@dataclass
class CoinContext:
    func: Callable
    type: Coin

@dataclass
class CoinBank:
    data: dict[str, dict[str, Callable]] = field(default_factory=dict)
    last_command: Optional[str] = None  # To track last used @command

    def add_command(self, command: str, default_func: Optional[Callable] = None):
        if command not in self.data:
            self.data[command] = {"default": None}
        self.last_command = command  # Store last used command

    def add_option(self, command: Optional[str], option: str, func: Callable):
        if command is None:
            if self.last_command is None:
                raise ValueError(f'Option "{option}" needs an explicit command name!')
            command = self.last_command  # Use last declared command if available

        if command not in self.data:
            raise ValueError(f'Command "{command}" does not exist in the CoinBank')

        if option in self.data[command]:
            raise ValueError(f'Option "{option}" already exists in the CoinBank')

        self.data[command][option] = func

BANK = CoinBank()

def command(name: str) -> Callable:
    BANK.add_command(name)
    def decorator(func: Callable) -> Callable:
        if not hasattr(func, "__wrapped__"):
            BANK.data[name]["default"] = func

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
    return decorator

def option(name: str, command_name: Optional[str] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        BANK.add_option(command_name, name, func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

@command("set")
@option("timer")
def set_timer():
    log.info("You're setting a timer right now, that's cool...")
