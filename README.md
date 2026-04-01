# Bongo Cat

A cute cat decided to sit on your taskbar and tap to your key presses!

https://github.com/user-attachments/assets/6e5dd6db-6d61-4542-8a0b-385ae145eff6

<sub>Made on Windows, pull requests are welcome to add support for Unix systems!</sub>

## Installation

Powershell:
```pwsh
irm "https://raw.githubusercontent.com/NSPC911/bongo-cat/refs/heads/main/install.ps1" | iex
```

Scoop:
```sh
scoop bucket add NSPC911-le-bucket https://github.com/nspc911/le-bucket
scoop install bongocat
```
Normal:
1. Get executable from [releases](https://github.com/NSPC911/bongo-cat)
2. Run executable
  - Reminder that an updater for this isn't properly implemented **at all**, so please use scoop!

## Build
```shell
git clone https://github.com/NSPC911/bongo-cat
cd bongo-cat
uv sync --group build
uv run poe build standalone --lto yes
# keep in mind that this command takes _a while (like 5+ minutes)_ to complete
```

<sub>Starring this repo means a lot to me so I can get the encouragement to make stupid projects like this!</sub>
```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣶⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⣀⡀⣠⣾⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⡇⠀⠀⠀⠀
⠀⣶⣿⣦⣜⣿⣿⣿⡟⠻⣿⣿⣿⣿⣿⣿⣿⡿⢿⡏⣴⣺⣦⣙⣿⣷⣄⠀⠀⠀
⠀⣯⡇⣻⣿⣿⣿⣿⣷⣾⣿⣬⣥⣭⣽⣿⣿⣧⣼⡇⣯⣇⣹⣿⣿⣿⣿⣧⠀⠀
⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣷⠀le bongocat
```
