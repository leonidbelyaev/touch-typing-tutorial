# Touch Typing Tutorial
### About
Touch Typing Tutorial is an app which helps you learn how to write fast without looking at your keyboard. It includes multiple modes to improve your typing:
- Basic Course (Type random combinations of only a few keys to help you learn their places)
- Random Typing (Try to type all letters in random order to make sure you remember all of them)
- Words Typing (Practice writing real words)
- Real Texts (Practice writing on real texts to improve your speed even further)

### Settings
This app supports any language and layout as long as the resources are added. By default it ships only with English (US) and QWERTY (as of version 1.0.0)  

### Technical info
This app uses PyQt6 and (will be) packed using pyinstaller. All the resources are in the _src_ directory, which contains:
- `src/fonts` — all TrueType fonts (`.ttf`), automatically added to the program if they are supported
- `src/lessons` — all lesson resources, there is a tree of this directory provided in `src/lessons/help.txt` file
- `src/design` — UI design files for Qt
- `src/index.py` — index of all supported files, (will be) loaded to the program
- other `.py` files — used internally, should not be edited unless required
Requirements are stored in requirements.txt 
