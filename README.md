# dq-xi-casino-bot

Bot that automates playing poker in Puerto Valor in Dragon Quest XI through PS4 Remote Play and a slightly modified https://github.com/komefai/PS4Macro. As a slight disclaimer to anyone trying to get this up and running, this project was put together in a weekend where we focused on getting something running rather than a clean working environment. I plan to build more game automation through this system and will update this repo as everything is cleaned up.

### Prerequisites

Windows

Python

PS4 Remote Play

OpenCV 3.3

### Installing

Clone https://github.com/komefai/PS4Macro

Copy the python scripts and states directory into PS4Macro/bin/Debug/

Swap in this repo's MacroPlayer.cs, which is a modified version that runs the cv scripts and uses output from python to change DualShockState.

After it is all set up, open remote play and go to either the blue or red poker table. Set the stake to the max setting, and run PS4Macro.

## About Poker

Poker in DQXI can be played on three different tables, all seemingly equal except the amount you can bet on each hand. This program can be run on the red and blue tables, with stakes for either 1000 or 100 tokens. To really win substantial money in this version of poker, you need to rely on the double or nothing rounds. The chance of winning each consecutive round drops, starting around 80%, so the optimal strategy is to play more rounds of double or nothing. I've currently set it to attempt 10 rounds for two pair/three of a kind hands, and 4 rounds for all other hands.

On the blue table the program would win on average **~475 tokens a minute** or **684000 every 24 hours**. The red table seems to use the same probabilities as the blue table, and will therefore have 10x winnings.

The algorithm to actually determine what cards to keep is based off of the one [described here.](http://www.videopokerballer.com/strategy/jokers-wild/)


### Double or Nothing Win Rates by Round

|Round|Win %|Samples|
|:-:|:-:|:-:|
|1|78%|8254|
|2|76%|6525|
|3|76%|4572|
|4|73%|1408|
|5|59%|532|
|6|58%|236|
|7|72%|83|

### Hand Win Distribution
|Hand Type|Reward|Total|Percent of Hands|
|:-:|:-:|:-:|:-:|
|Royal Jelly Flush|50000|2|0.01%
|Royal Flush|10000|7|0.04%
|Five of a Kind|5000|31|0.16%
|Straight Flush|2000|368|0.15%
|Four of a Kind|1000|372|1.92%
|Full House|500|752|3.92%
|Flush|400|342|1.78%
|Straight|300|372|1.94%
|Three of a Kind|100|2806|14.64%
|Two Pair|100|2370|12.37%
|Nothing|0|12084|63.06%

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

