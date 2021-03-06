#!/usr/bin/env python3

from curses import keyname
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
        cache_name="word_cache", expire_after=timedelta(days=30)  # cache for 30 days
    )
    return requests.get(
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    ).json()


def write(word: str):
    with open("word.json", "w") as f:
        json.dump(fetch(word), f)


def phonetic(res: dict) -> None:
    with contextlib.suppress(KeyError, UnboundLocalError):
        phonetic = res[0]["phonetics"]
        for i in phonetic:

            if i["text"] and i["audio"]:
                text = i["text"]
                audio = i["audio"]
                accent = audio.split("/")[-1]

        print(f"\033]8;;{audio}\033\\{CYAN}{text} ({accent})\033]8;;\033\\{RESET}")


def definition(res: dict) -> None:
    with contextlib.suppress(KeyError):
        meanings = res[0]["meanings"]
        for i in meanings:
            for j in i["definitions"]:
                print(
                    f"• {PURPLE}[{i['partOfSpeech']}] {GREEN}{j['definition']}{RESET}"
                )


def example(res: dict) -> None:
    with contextlib.suppress(KeyError):
        meanings = res[0]["meanings"]
        for i in meanings:
            for j in i["definitions"]:
                with contextlib.suppress(KeyError):
                    print(
                        f"• {PURPLE}[{i['partOfSpeech']}] {GREEN}{j['example']}{RESET}"
                    )


def synonym(res: dict) -> None:
    with contextlib.suppress(KeyError):
        meanings = res[0]["meanings"]
        for i in meanings:
            for j in i["definitions"]:
                if j["synonyms"]:
                    for k in j["synonyms"]:
                        print(f"• {PURPLE}[{i['partOfSpeech']}] {GREEN}{k}{RESET}")

            # with contextlib.suppress(KeyError):
            if i["synonyms"]:
                for j in i["synonyms"]:
                    print(f"• {PURPLE}[{i['partOfSpeech']}] {GREEN}{j}{RESET}")


def antonym(res: dict) -> None:
    with contextlib.suppress(KeyError):
        meanings = res[0]["meanings"]
        for i in meanings:
            for j in i["definitions"]:
                if j["antonyms"]:
                    for k in j["antonyms"]:
                        print(f"• {PURPLE}[{i['partOfSpeech']}] {GREEN}{k}{RESET}")

            # with contextlib.suppress(KeyError):
            if i["antonyms"]:
                for j in i["antonyms"]:
                    print(f"• {PURPLE}[{i['partOfSpeech']}] {GREEN}{j}{RESET}")


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
    print(f"\n{BOLD}{YELLOW}Synonyms:{RESET}")
    synonym(RES)
    print(f"\n{BOLD}{YELLOW}Antonyms:{RESET}")
    antonym(RES)


if __name__ == "__main__":
    main()
