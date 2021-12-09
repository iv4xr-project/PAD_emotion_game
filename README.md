# PAD_emotion_game
This repository contains a simple 2-D game used to train emotional agents along with the code necessary for generating such agents. In this repository can be found the code for the game (infinite_game.py), the code for training a predictive machine learning model (predictor.py), the code for deplying AI agents on said game (rule_based_agents.py) and the data collected from the fist user study conducted using this game and continuous annotation of the 3 dimensions of PAD model of emotion (First_Study folder).

## Running the Game

To run the game, run the "infinite_game.py" file. One way to do so is to write "python3 infinite_game.py" on the command line while in the project's directory.

The game can be run in several different ways. Currently, this is done by commenting and uncommenting blocks of code at the end of the "infinite_game.py" file. These blocks of code are easily identifiable by their headers. An example block of code can be seen here:

![Alt text](Images/block_code.png?raw=true "Block of Code")


## The Collected Traces

Under the folder "First_Study", you can find several gameplay traces. These traces were collected as part of a study where users were asked to play 3 different levels of the game and then report their levels of the PAD emotional dimensions. The levels played can be found on the "Maps" directory and were the "Level1.csv", "Level2.csv" and "Level3.csv".

The traces are divided in 3 folders: one for each of the PAD emotional dimensions.

There are different types of traces in the folders, which can be identified by the name of the file. The final part of the name is always a numeric unique identifier of the player preceded, when appliable, by the game map that the trace corresponds to. 

* **Answers_Answers**
  * These files contain answers to a number of questions. The questions are in portuguese and can be found on the file "Questions.txt"
* **Answers_Order**
  * These files describe the order on which the identified player played the 3 levels.
* **Traces_Actions**
  * These files describe the actions taken by the player at each tick of the game. The actions are key presses or releases. For example, "dd" means that the key 'D' was pressed down, whereas "du" means que key 'D' was pressed up, that is, was released. ' ' means that the spacebar was pressed.
* **Traces_DIMENSION_NAME**
  * These files have the reported value of the corresponding emotional dimension for the given level and player.
* **Traces_Perceptor**
  * These files have the values for each tick of the game of all the collected input variables that were considered relevant for training the predictor.
* **Traces_Position**
  * These files have the x and y coordinates of the player throughout the trace 

The names of the trace files end up with a unique number identifier, which can be used to identify the player. The name also has the 



More information on how to interpret these traces will be soon added...

## Training a PAD Prediction Model Using the Traces Provided

To train a predictive model based on the emotional traces, run the "predictor.py" file. One way to do so is to write "python3 predictor.py" on the command line while in the project's directory.


