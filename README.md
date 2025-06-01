# Bongo Cat

A cute cat decided to sit on your taskbar and tap to your key presses!

<sub>Made on Windows, pull requests are welcome to add support for Unix systems!</sub>

## Installation

Scoop:
```sh
scoop bucket add NSPC911-le-bucket https://github.com/nspc911/le-bucket
scoop install bongocat
```
Normal:
1. Get executable from [releases](https://github.com/NSPC911/bongo-cat)
2. Run executable
  - Reminder that an updater for this hasn't been made, so scoop is super recommended!

## Build
```py
git clone https://github.com/NSPC911/bongo-cat
cd bongo-cat
uv sync
pyinstaller --noconsole --onefile bongocat.py
```

<sub>Starring this repo means a lot to me so I can get the encouragement to make stupid projects like this!</sub>
