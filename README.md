# CLI Dictionary
A Simple CLI Dictionary made possible by this free [Dictionary API](https://dictionaryapi.dev/). Currently a WIP and only works properly on some terminals (Clicakble Text)

This functionality should be working on kitty, gnome-terminal, and iterm2.

# Installation
I have not tested this with other python versions other than 3.10, so I'm not sure if it will work on other versions.

```bash
git clone https://github.com/KotonBads/cli-dictionary.git
pip install -r requirements.txt
```
that should all be the requirements installed

# Usage
```bash
# run this wherever the python file is
./main.py [WORD] # or whatever you named the file
```
since I'm using click, any future options should be automatically documented in the help command.
```bash
# run this wherever the python file is
./main.py --help # or whatever you named the file
```
you could also pipe this into a pager like `less` or `more`
```bash
# run this wherever the python file is
./main.py [WORD] | less -R # -R makes the colors work
```

# Caching
I used `requests-cache` for caching the response of the API. This greatly improved the speed of the program. The cache is stored in the same directory as the program and is valid for 30 days (1 month).

# Future Features
- Search by definition
- Customizing output (eg only show synonyms or meaning)