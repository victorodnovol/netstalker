# menu.py
from dataclasses import dataclass
from inspect import getsourcefile
from os.path import abspath

from colorama import Fore as Fg


@dataclass
class Target:
    name: str = 'time'
    max: int = 1

    def __str__(self):
        return self.name


# @snoop()
def print_menu() -> (int, dict):
    """
    Функция печатает меню и собирает ввод пользователя
    """
    target = Target()
    try:
        logo_path = abspath(getsourcefile(lambda: 0))
    except OSError:
        print('File "logo.txt" is missing')
        return
    try:
        with open(logo_path[:-7] + 'logo.txt', 'r') as logo:
            print(Fg.GREEN + logo.read() + Fg.RESET)
    except FileNotFoundError:
        print('File "logo.txt" is missing')
    print('This netstalker will grab the site imgur.com !')

    while True:
        threads = input(Fg.GREEN + 'Enter threads count: ' + Fg.RESET)
        if not threads:
            print('User input required')
            continue
        try:
            threads = int(threads)
        except ValueError:
            print('User input is invalid')
            continue
        if not threads >= 1:
            print('User input is invalid')
            continue
        break

    menu = {
        '1': 'Time',
        '2': 'Links count',
        '3': 'Target size',
    }
    print(f'{Fg.GREEN}Choose method: {Fg.RESET}')
    header = '\n' + '\n'.join([f'{num}. {menu[num]}' for num in menu])
    print(header)
    while method := input('\nEnter the option number: '):
        if method not in menu.keys():
            print(Fg.RED + 'User choice is incorrect' + Fg.RESET)
            continue
        break
    if method == '1':
        max_time = int(
            input(f'{Fg.GREEN}Select max time [minutes]:{Fg.RESET} ')) * 60
        target = Target('time', max_time)
    elif method == '2':
        max_links = int(input(f'{Fg.GREEN}Select links qnt:{Fg.RESET} '))
        target = Target('links', max_links)
    elif method == '3':
        max_size = int(input(f'{Fg.GREEN}Select max size [kb]:{Fg.RESET} '))
        target = Target('size', max_size * 1024)
    return threads, target
