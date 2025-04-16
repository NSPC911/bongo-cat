# Bongo Cat

A cute cat decided to sit on your taskbar and tap to your key presses!

<sub>Made on Windows, untested on Unix systems</sub>

## Installation

1. Download the executable from the [releases](https://github.com/NSPC911/bongo-cat)
2. Run the executable
3. Edit your config at `C:/Users/<user>/AppData/Roaming/bongo-cat`
4. Make sure to quit from the tasktray everytime you edit the config (trying to find a better solution)

## Build
```py
git clone https://github.com/NSPC911/bongo-cat
cd bongo-cat
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
pyinstaller --noconsole --onefile --add-data "idle.png;." --add-data "leftpaw.png;." --add-data "rightpaw.png;." bongocat.py
```

<sub>Starring this repo means a lot to me so I can get the encouragement to make stupid projects like this!</sub>
