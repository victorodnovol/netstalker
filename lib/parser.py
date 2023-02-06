# parser.py

import os
import random
import string
import sys
import threading
import time

import click
import requests
from colorama import Fore

from . import menu

stats = {'time': 0.0, 'links': 0, 'size': 0, 'start_time': 0.0}
PRINT_LOCK = threading.Lock()
STATS_LOCK = threading.Lock()


def print_stats():
    """ Функция выводит статистику на экран """
    click.echo('\n')
    click.secho('=' * 40)
    time_taken = stats['time'] - stats['start_time']
    space_taken = stats['size'] / 1024
    time_string = time.strftime("%H hours %M minutes %S seconds",
                                time.gmtime(time_taken))
    click.secho(f'Ready for:\t{time_string}', fg='magenta')
    click.secho(f'Found links:\t{stats["links"]}', fg='magenta')
    click.secho(f'Folder size:\t{round(space_taken)} kb', fg='magenta')
    if input('Would you like to open the Photos folder? Y/N ') == 'Y':
        if sys.platform == 'win32':
            os.startfile(os.getcwd())
        if sys.platform == 'linux':
            os.system('xdg-open .')


def check_site(domain, headers=None) -> bool:
    """Функция проверяет есть ли коннект с хостом"""
    if headers is None:
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36 "
        }
    try:
        response = requests.get(domain, headers, timeout=1)
        response.raise_for_status()
        if response.status_code == 200:
            click.echo(
                f'.....site available!{Fore.RED} Started stalking!{Fore.RESET}'
            )
            return True
        else:
            click.echo('Site is not available!')
            return False
    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
        click.echo(f'HTTP ERROR or Timeout ERROR: {e}')
        return False
    except Exception as e:
        click.echo(
            f'ERROR is unknown. Site is not available.\n Details:\n {e}')
        return False


def run_app():
    """ Точка входа в приложение """
    # headers = get_head()
    try:
        threads, target = menu.print_menu()  # Вывод меню пользователя
    except KeyboardInterrupt:
        print('\nProgram terminated by user request')
        return

    if not check_site('https://imgur.com/'):  # Доступность хоста
        sys.exit()
    if not os.path.isdir("Photos"):
        os.mkdir("Photos")
    os.chdir("Photos")
    do_work(threads, target)  # Главная процедура
    print_stats()


def get_link() -> str:
    """
    Возвращает случайную ссылку начинающуюся с https://i.imgur.com/ 
    и заканчивающуюся на .jpg
    """
    url = 'https://i.imgur.com/'
    url += ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(7))
    url += '.jpg'
    return url


def do_work(threads, target) -> None:
    """
    Функция создает потоки и начинает отсчет времени
    """
    start_time = time.time()
    if target.name == 'time':
        target.max += start_time
    stats['start_time'] = start_time
    my_pool = [
        threading.Thread(target=worker, args=(target, ), daemon=True)
        for _ in range(threads)
    ]
    for proc in my_pool:
        proc.start()
    for proc in my_pool:
        try:
            proc.join()
        except KeyboardInterrupt:
            click.secho(' ERROR: manual stop Ctrl+C', fg='red')
            sys.exit()


def worker(target) -> None:
    """
    Функция вызывает get_link() для создания ссылки,
    проверяет её, и сохраняет результат
    """
    while stats[target.name] < target.max:
        target_url = get_link()
        try:
            host_answer = requests.get(target_url,
                                       allow_redirects=False,
                                       stream=True)
        except requests.ConnectionError:
            click.secho(f'Error in connection to {target_url}', fg='red')
            return
        if host_answer.status_code != 200:
            with PRINT_LOCK:
                print(f"{target_url}", end='                            \r')
        else:
            with PRINT_LOCK:
                click.echo(f"{Fore.GREEN}GOOD!{Fore.RESET} --> {target_url}")
            file_name = f'{target_url.rsplit("/", 1)[-1]}'
            with open(file_name, 'wb') as writer:
                writer.write(host_answer.content)
            # save stats
            with STATS_LOCK:
                stats['links'] += 1
                stats['size'] += os.path.getsize(file_name)
        with STATS_LOCK:
            stats['time'] = time.time()


if __name__ == "__main__":
    """ Точка входа в приложение """
    run_app()
