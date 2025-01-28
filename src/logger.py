# TODO:
#   - Support passing class initializers to the logger

from colorama import Fore, Back, Style
from typing import Dict, Any, Optional, List
import builtins
import logging

MAPPING: Dict[int, str] = {
    logging.DEBUG: Fore.WHITE,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.FATAL: Fore.BLACK + Back.RED + Style.BRIGHT,
}

FORMAT_TEXT_STREAM = "%(levelname)-8s | %(message)s"
FORMAT_TEXT_FILE = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

class ColoredFormatter(logging.Formatter):
    def __init__(self, format_text, colorful=True):
        logging.Formatter.__init__(self)
        self.format_text = format_text
        self.colorful = colorful

    def format(self, record):
        formatter = logging.Formatter()
        if self.colorful is True:
            color = MAPPING.get(record.levelno, Fore.WHITE) # default white
            formatter = logging.Formatter(color + self.format_text + Style.RESET_ALL)
        return formatter.format(record)

# create top level logger
log = logging.getLogger("main")
log.setLevel(logging.DEBUG)

# add stream handler
stream_handle = logging.StreamHandler()
stream_handle.setLevel(logging.DEBUG)
stream_handle.setFormatter(ColoredFormatter(FORMAT_TEXT_STREAM))
log.addHandler(stream_handle)

# add file handler
file_handle = logging.FileHandler('ellie.log')
file_handle.setLevel(logging.DEBUG)
file_handle.setFormatter(ColoredFormatter(FORMAT_TEXT_FILE, colorful=False))
log.addHandler(file_handle)

# NOTE: If this seems hacky, it is...
#       The goal is more verbose logging
old_import = __import__

def noisy_importer(name, locals=None, globals=None, fromlist=(), level=0):
    #print(f'name: {name!r}')
    #print(f'fromlist: {fromlist}')
    #print(f'level: {level}')
    return old_import(name, locals, globals, fromlist, level)

builtins.__import__ = noisy_importer

# EXAMPLE:
#log.debug("Ellie has started")
#log.info("Logging to 'ellie.log' in your cwd")
#log.warning("This is my last warning, take heed.")
#log.error("This is an error.")
#log.critical("Ellie is dead")
