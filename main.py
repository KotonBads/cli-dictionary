#!/usr/bin/env python3

import click
import contextlib
import requests
import requests_cache
import json

from datetime import timedelta


# ANSI Color Codes
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"
BOLD = "\033[1m"


def fetch(word: str) -> dict:
    requests_cache.install_cache(
        cache_name="word_cache", expire_after=timedelta(days=30) # cache for 30 days
    )
    return requests.get(
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    ).json()


def write(word: str):
    with open("word.json", "w") as f:
        json.dump(fetch(word), f)


def phonetic(res: dict) -> None:
    with contextlib.suppress(
        KeyError, UnboundLocalError
    ):  # supress errors to show nothing
        phonetic = res[0]["phonetics"]
        for i in phonetic:

            if i["text"] and i["audio"]:
                text = i["text"]
                audio = i["audio"]
                accent = audio.split("/")[-1]

        print(f"\033]8;;{audio}\033\\{CYAN}{text} ({accent})\033]8;;\033\\{RESET}")


def definition(res: dict) -> None:
    with contextlib.suppress(KeyError):  # supress errors to show nothing
        meanings = res[0]["meanings"]
        for i in meanings:
            for j in i["definitions"]:
                print(
                    f"• {PURPLE}[{i['partOfSpeech']}] {GREEN}{j['definition']}{RESET}"
                )


def example(res: dict) -> None:
    meanings = res[0]["meanings"]
    for i in meanings:
        for j in i["definitions"]:
            try:  # contextlib stops the loop if there is no example
                print(f"• {PURPLE}[{i['partOfSpeech']}] {GREEN}{j['example']}{RESET}")
            except KeyError:
                continue


@click.command()
@click.argument("word")
def main(word: str) -> None:
    """
    A CLI tool for fetching the definition of a word.
    """

    RES = fetch(word)

    print(f"{BOLD}{WHITE}[{word}]{RESET}")
    phonetic(RES)
    print(f"\n{BOLD}{YELLOW}Definitions:{RESET}")
    definition(RES)
    print(f"\n{BOLD}{YELLOW}Examples:{RESET}")
    example(RES)


if __name__ == "__main__":
    main()
