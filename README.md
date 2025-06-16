# A simple but weird looking ai (handmade) bot.

## It can play games like Minecraft and Roblox in a simple way by moving the character and so. Also be aware that this bot can be a bit creepy with the movements and thats the reason shared it with yall. USE AT YOUR OWN RISK!


## Supported Games

- Roblox
- Minecraft

## Requirements

- Python 3.8 or higher
- Required Python packages:
  - tkinter
  - threading
  - random
  - keyboard
  - win32gui
  - pygetwindow
  - pyautogui
  - pytesseract
  - opencv-python
  - numpy
  - scikit-learn
  - tensorflow

## Installation

1. Install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
2. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-game-bot.git
```
3. Navigate to the project directory:
```bash
cd ai-game-bot
```
4. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python key_press_assist.py
```

2. The GUI will appear with these controls:
   - Select Window: Choose your game window from the dropdown
   - Refresh Games: Update the list of available windows
   - Start/Stop: Toggle the bot on/off
   - Status: Shows current status, game, and stop key
   - AI Status: Shows AI operation status

3. To start the bot:
   - Select your game window from the dropdown
   - Click "Start" or press the stop key ('p')

4. To stop the bot:
   - Click "Stop" button
   - Or press the stop key ('p')

## Configuration

You can customize the bot's behavior by modifying the following parameters:
- Stop key: Default is 'p', can be changed in the code
- Movement weights: Adjusted to favor forward movement
- Chat message probabilities: Different messages have different probabilities of being sent

## Disclaimer

This tool is for educational purposes only. Use responsibly and be aware of game terms of service.

## License

MIT License - see LICENSE file for details
