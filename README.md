##  Street Fighter II Bot Controller using Machine Learning ##

This project implements an AI bot for Street Fighter II Turbo (SNES) using supervised machine learning. Replacing a traditional rule-based bot, the new system uses real gameplay data and a trained MLPClassifier model to make decisions in real-time through the BizHawk emulator.

---
## project Objective ##

The main objective was to transition from a rule-based logic system to a machine learning-driven bot that:
- Learns actions based on gameplay data.
- Predicts moves on current game state.
- Works across various characters and scenarios with no manual tunin

##  Project Overview ##

The goal of this project is to build an intelligent bot that can play Street Fighter II Turbo by:
- Collecting gameplay data through bot-controlled sessions
- Training a machine learning model using that data
- Using the trained model to automate bot decisions and actions in the game

---

##  Prerequisites / Dependencies

- **Operating System**: Windows 7 or above (64-bit)

### Python API

- Developed and tested in **Python 3.6.3**
- Compatible with any Python version ≥ 3 (minor adjustments may be needed)

### Java API

- Developed and tested in **JDK 10**
- Should work with other Java versions as well

---
## Machine Learning Overview ##

- We use MLPClassifier from scikit-learn trained on frame-by-frame gameplay data.
- Game State Features:
- Player coordinates (x, y)
- Health and status
- Actions (jumping, crouching, attacking)
- Opponent’s state
- 
Model Output:

- Predicted button/action to be performed

## Initial Setup (Instructor Upload Instructions) ##

To run this bot, simply copy and paste the following uploaded files into your working directory:

- bot.py
- controller.py
- train_model.py
- model_train.pkl
- data/gameplay_data.csv


## Conclusion ##

This project showcases how machine learning can enhance gameplay automation by creating bots that are adaptive, data-driven, and generalizable. Replacing static if-else rules with an MLPClassifier improved realism, flexibility, and overall game intelligence.
  
##  How to Run the Game and Bot

1. Choose gameplay mode:
   - For **bot vs CPU**, use the `single-player/` folder
   - For **bot vs bot**, use the `two-players/` folder

2. Launch `EmuHawk.exe` from the selected folder.

3. From the **File** menu, click **Open ROM** (`Ctrl + O`) and select:

4. From the **Tools** menu, open the **Tool Box** (`Shift + T`).

5. Open a command prompt in the Python API directory and run:
```bash

python controller.py 1
Project Structure

├── single-player/
├── two-players/
├── Street Fighter II Turbo (U).smc
├── python-api/
│   ├── bot.py
│   ├── controller.py
│   ├── train_model.py
│   ├── model_train.pkl
│   └── data/
│       └── gameplay_data.csv
├── java-api/
│   ├── Bot.java
│   ├── Controller.java
│   └── lib/
│       └── json-20160212.jar
└── README.md

