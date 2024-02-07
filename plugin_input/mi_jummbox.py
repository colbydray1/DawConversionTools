# SPDX-FileCopyrightText: 2023 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from functions import data_bytes
from functions import data_values
from functions import xtramath
from functions import colors
from objects import dv_dataset
import plugin_input
import json
import math

filtervals = [2378.41, 3363.59, 4756.83, 5656.85, 8000, 9513.66, 11313.71, 13454.34, 16000, 19027.31, None]

rawChipWaves = {}
rawChipWaves["rounded"] = {"expression": 0.94, "samples": [0,0.2,0.4,0.5,0.6,0.7,0.8,0.85,0.9,0.95,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.95,0.9,0.85,0.8,0.7,0.6,0.5,0.4,0.2,0,-0.2,-0.4,-0.5,-0.6,-0.7,-0.8,-0.85,-0.9,-0.95,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0.95,-0.9,-0.85,-0.8,-0.7,-0.6,-0.5,-0.4,-0.2]}
rawChipWaves["triangle"] = {"expression": 1, "samples": [1/15,0.2,5/15,7/15,0.6,11/15,13/15,1,1,13/15,11/15,0.6,7/15,5/15,0.2,1/15,-1/15,-0.2,-5/15,-7/15,-0.6,-11/15,-13/15,-1,-1,-13/15,-11/15,-0.6,-7/15,-5/15,-0.2,-1/15]}
rawChipWaves["square"] = {"expression": 0.5, "samples": [1,-1]}
rawChipWaves["1/4 pulse"] = {"expression": 0.5, "samples": [1,-1,-1,-1]}
rawChipWaves["1/8 pulse"] = {"expression": 0.5, "samples": [1,-1,-1,-1,-1,-1,-1,-1]}
rawChipWaves["sawtooth"] = {"expression": 0.65, "samples": [1/31,3/31,5/31,7/31,9/31,11/31,13/31,15/31,17/31,19/31,21/31,23/31,25/31,27/31,29/31,1,-1,-29/31,-27/31,-25/31,-23/31,-21/31,-19/31,-17/31,-15/31,-13/31,-11/31,-9/31,-7/31,-5/31,-3/31,-1/31]}
rawChipWaves["double saw"] = {"expression": 0.5, "samples": [0,-0.2,-0.4,-0.6,-0.8,-1,1,-0.8,-0.6,-0.4,-0.2,1,0.8,0.6,0.4,0.2]}
rawChipWaves["double pulse"] = {"expression": 0.4, "samples": [1,1,1,1,1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1]}
rawChipWaves["spiky"] = {"expression": 0.4, "samples": [1,-1,1,-1,1,0]}
rawChipWaves["sine"] = {"expression": 0.88, "samples": [8,9,11,12,13,14,15,15,15,15,14,14,13,11,10,9,7,6,4,3,2,1,0,0,0,0,1,1,2,4,5,6]}
rawChipWaves["flute"] = {"expression": 0.8, "samples": [3,4,6,8,10,11,13,14,15,15,14,13,11,8,5,3]}
rawChipWaves["harp"] = {"expression": 0.8, "samples": [0,3,3,3,4,5,5,6,7,8,9,11,11,13,13,15,15,14,12,11,10,9,8,7,7,5,4,3,2,1,0,0]}
rawChipWaves["sharp clarinet"] = {"expression": 0.38, "samples": [0,0,0,1,1,8,8,9,9,9,8,8,8,8,8,9,9,7,9,9,10,4,0,0,0,0,0,0,0,0,0,0]}
rawChipWaves["soft clarinet"] = {"expression": 0.45, "samples": [0,1,5,8,9,9,9,9,9,9,9,11,11,12,13,12,10,9,7,6,4,3,3,3,1,1,1,1,1,1,1,1]}
rawChipWaves["alto sax"] = {"expression": 0.3, "samples": [5,5,6,4,3,6,8,7,2,1,5,6,5,4,5,7,9,11,13,14,14,14,14,13,10,8,7,7,4,3,4,2]}
rawChipWaves["bassoon"] = {"expression": 0.35, "samples": [9,9,7,6,5,4,4,4,4,5,7,8,9,10,11,13,13,11,10,9,7,6,4,2,1,1,1,2,2,5,11,14]}
rawChipWaves["trumpet"] = {"expression": 0.22, "samples": [10,11,8,6,5,5,5,6,7,7,7,7,6,6,7,7,7,7,7,6,6,6,6,6,6,6,6,7,8,9,11,14]}
rawChipWaves["electric guitar"] = {"expression": 0.2, "samples": [11,12,12,10,6,6,8,0,2,4,8,10,9,10,1,7,11,3,6,6,8,13,14,2,0,12,8,4,13,11,10,13]}
rawChipWaves["organ"] = {"expression": 0.2, "samples": [11,10,12,11,14,7,5,5,12,10,10,9,12,6,4,5,13,12,12,10,12,5,2,2,8,6,6,5,8,3,2,1]}
rawChipWaves["pan flute"] = {"expression": 0.35, "samples": [1,4,7,6,7,9,7,7,11,12,13,15,13,11,11,12,13,10,7,5,3,6,10,7,3,3,1,0,1,0,1,0]}
rawChipWaves["glitch"] = {"expression": 0.5, "samples": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1]}

rawChipWaves["brucebox isolated spiky"] = {"expression": 0.5, "samples": [1.0, -1.0, 1.0, -1.0, 1.0, -1.0]}
rawChipWaves["brucebox pokey 4bit lfsr"] = {"expression": 0.5, "samples": [1.0, -1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0]}
rawChipWaves["brucebox pokey 5step bass"] = {"expression": 0.5, "samples": [1.0, -1.0, 1.0, -1.0, 1.0]}
rawChipWaves["haileybox test1"] = {"expression": 0.5, "samples": [1.0, 0.5, -1.0]}
rawChipWaves["modbox 1% pulse"] = {"expression": 0.5, "samples": [1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]}
rawChipWaves["modbox 10% pulse"] = {"expression": 0.5, "samples": [1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]}
rawChipWaves["modbox acoustic bass"] = {"expression": 0.5, "samples": [1.0, 0.0, 0.1, -0.1, -0.2, -0.4, -0.3, -1.0]}
rawChipWaves["modbox atari bass"] = {"expression": 0.5, "samples": [1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]}
rawChipWaves["modbox atari pulse"] = {"expression": 0.5, "samples": [1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}
rawChipWaves["modbox brass"] = {"expression": 0.45, "samples": [-1.0, -0.95, -0.975, -0.9, -0.85, -0.8, -0.775, -0.65, -0.6, -0.5, -0.475, -0.35, -0.275, -0.2, -0.125, -0.05, 0.0, 0.075, 0.125, 0.15, 0.20, 0.21, 0.225, 0.25, 0.225, 0.21, 0.20, 0.19, 0.175, 0.125, 0.10, 0.075, 0.06, 0.05, 0.04, 0.025, 0.04, 0.05, 0.10, 0.15, 0.225, 0.325, 0.425, 0.575, 0.70, 0.85, 0.95, 1.0, 0.9, 0.675, 0.375, 0.2, 0.275, 0.4, 0.5, 0.55, 0.6, 0.625, 0.65, 0.65, 0.65, 0.65, 0.64, 0.6, 0.55, 0.5, 0.4, 0.325, 0.25, 0.15, 0.05, -0.05, -0.15, -0.275, -0.35, -0.45, -0.55, -0.65, -0.7, -0.78, -0.825, -0.9, -0.925, -0.95, -0.975]}
rawChipWaves["modbox curved sawtooth"] = {"expression": 0.5, "samples": [1.0, 1.0/2.0, 1.0/3.0, 1.0/4.0]}
rawChipWaves["modbox flatline"] = {"expression": 1.0, "samples": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}
rawChipWaves["modbox guitar"] = {"expression": 0.5, "samples": [-0.5, 3.5, 3.0, -0.5, -0.25, -1.0]}
rawChipWaves["modbox loud pulse"] = {"expression": 0.5, "samples": [1.0, 0.7, 0.1, 0.1, 0, 0, 0, 0, 0, 0.1, 0.2, 0.15, 0.25, 0.125, 0.215, 0.345, 4.0]}
rawChipWaves["modbox lyre"] = {"expression": 0.45, "samples": [1.0, -1.0, 4.0, 2.15, 4.13, 5.15, 0.0, -0.05, 1.0]}
rawChipWaves["modbox piccolo"] = {"expression": 0.5, "samples": [1, 4, 2, 1, -0.1, -1, -0.12]}
rawChipWaves["modbox pnryshk a (u5)"] = {"expression": 0.4, "samples": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]}
rawChipWaves["modbox pnryshk b (riff)"] = {"expression": 0.5, "samples": [1.0, -0.9, 0.8, -0.7, 0.6, -0.5, 0.4, -0.3, 0.2, -0.1, 0.0, -0.1, 0.2, -0.3, 0.4, -0.5, 0.6, -0.7, 0.8, -0.9, 1.0]}
rawChipWaves["modbox ramp pulse"] = {"expression": 0.5, "samples": [6.1, -2.9, 1.4, -2.9]} 
rawChipWaves["modbox sax"] = {"expression": 0.5, "samples": [1.0/15.0, 3.0/15.0, 5.0/15.0, 9.0, 0.06]}
rawChipWaves["modbox sine"] = {"expression": 0.5, "samples": [0.0, 0.05, 0.125, 0.2, 0.25, 0.3, 0.425, 0.475, 0.525, 0.625, 0.675, 0.725, 0.775, 0.8, 0.825, 0.875, 0.9, 0.925, 0.95, 0.975, 0.98, 0.99, 0.995, 1, 0.995, 0.99, 0.98, 0.975, 0.95, 0.925, 0.9, 0.875, 0.825, 0.8, 0.775, 0.725, 0.675, 0.625, 0.525, 0.475, 0.425, 0.3, 0.25, 0.2, 0.125, 0.05, 0.0, -0.05, -0.125, -0.2, -0.25, -0.3, -0.425, -0.475, -0.525, -0.625, -0.675, -0.725, -0.775, -0.8, -0.825, -0.875, -0.9, -0.925, -0.95, -0.975, -0.98, -0.99, -0.995, -1, -0.995, -0.99, -0.98, -0.975, -0.95, -0.925, -0.9, -0.875, -0.825, -0.8, -0.775, -0.725, -0.675, -0.625, -0.525, -0.475, -0.425, -0.3, -0.25, -0.2, -0.125, -0.05]}
rawChipWaves["modbox squaretooth"] = {"expression": 0.5, "samples": [0.2, 1.0, 2.6, 1.0, 0.0, -2.4]}
rawChipWaves["modbox sunsoft bass"] = {"expression": 1.0, "samples": [0.0, 0.1875, 0.3125, 0.5625, 0.5, 0.75, 0.875, 1.0, 1.0, 0.6875, 0.5, 0.625, 0.625, 0.5, 0.375, 0.5625, 0.4375, 0.5625, 0.4375, 0.4375, 0.3125, 0.1875, 0.1875, 0.375, 0.5625, 0.5625, 0.5625, 0.5625, 0.5625, 0.4375, 0.25, 0.0]}
rawChipWaves["modbox viola"] = {"expression": 0.45, "samples": [-0.9, -1.0, -0.85, -0.775, -0.7, -0.6, -0.5, -0.4, -0.325, -0.225, -0.2, -0.125, -0.1, -0.11, -0.125, -0.15, -0.175, -0.18, -0.2, -0.21, -0.22, -0.21, -0.2, -0.175, -0.15, -0.1, -0.5, 0.75, 0.11, 0.175, 0.2, 0.25, 0.26, 0.275, 0.26, 0.25, 0.225, 0.2, 0.19, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.275, 0.28, 0.29, 0.3, 0.29, 0.28, 0.27, 0.26, 0.25, 0.225, 0.2, 0.175, 0.15, 0.1, 0.075, 0.0, -0.01, -0.025, 0.025, 0.075, 0.2, 0.3, 0.475, 0.6, 0.75, 0.85, 0.85, 1.0, 0.99, 0.95, 0.8, 0.675, 0.475, 0.275, 0.01, -0.15, -0.3, -0.475, -0.5, -0.6, -0.71, -0.81, -0.9, -1.0, -0.9]}
rawChipWaves["nerdbox unnamed 1"] = {"expression": 0.5, "samples": [0.2 , 0.8/0.2, 0.7, -0.4, -1.0, 0.5, -0.5/0.6]}
rawChipWaves["nerdbox unnamed 2"] = {"expression": 0.5, "samples": [2.0 , 5.0/55.0 , -9.0 , 6.5/6.5 , -55.0, 18.5/-26.0]}
rawChipWaves["sandbox bassoon"] = {"expression": 0.5, "samples": [1.0, -1.0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]}
rawChipWaves["sandbox contrabass"] = {"expression": 0.5, "samples": [4.20, 6.9, 1.337, 6.66]}
rawChipWaves["sandbox deep square"] = {"expression": 1.0, "samples": [1.0, 2.25, 1.0, -1.0, -2.25, -1.0]}
rawChipWaves["sandbox double bass"] = {"expression": 0.4, "samples": [0.0, 0.1875, 0.3125, 0.5625, 0.5, 0.75, 0.875, 1.0, -1.0, -0.6875, -0.5, -0.625, -0.625, -0.5, -0.375, -0.5625, -0.4375, -0.5625, -0.4375, -0.4375, -0.3125, -0.1875, 0.1875, 0.375, 0.5625, -0.5625, 0.5625, 0.5625, 0.5625, 0.4375, 0.25, 0.0]}
rawChipWaves["sandbox double sine"] = {"expression": 1.0, "samples": [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.0, -1.0, -1.1, -1.2, -1.3, -1.4, -1.5, -1.6, -1.7, -1.8, -1.9, -1.8, -1.7, -1.6, -1.5, -1.4, -1.3, -1.2, -1.1, -1.0]}
rawChipWaves["sandbox euphonium"] = {"expression": 0.3, "samples": [0, 1, 2, 1, 2, 1, 4, 2, 5, 0, -2, 1, 5, 1, 2, 1, 2, 4, 5, 1, 5, -2, 5, 10, 1]}
rawChipWaves["sandbox narrow saw"] = {"expression": 1.2, "samples": [0.1, 0.13/-0.1 ,0.13/-0.3 ,0.13/-0.5 ,0.13/-0.7 ,0.13/-0.9 ,0.13/-0.11 ,0.13/-0.31 ,0.13/-0.51 ,0.13/-0.71 ,0.13/-0.91 ,0.13/-0.12 ,0.13/-0.32 ,0.13/-0.52 ,0.13/-0.72 ,0.13/-0.92 ,0.13/-0.13 ,0.13/0.13 ,0.13/0.92 ,0.13/0.72 ,0.13/0.52 ,0.13/0.32 ,0.13/0.12 ,0.13/0.91 ,0.13/0.71 ,0.13/0.51 ,0.13/0.31 ,0.13/0.11 ,0.13/0.9 ,0.13/0.7 ,0.13/0.5 ,0.13/0.3 ,0.13]}
rawChipWaves["sandbox nes pulse"] = {"expression": 0.4, "samples": [2.1, -2.2, 1.2, 3]}
rawChipWaves["sandbox r-sawtooth"] = {"expression": 0.2, "samples": [6.1, -2.9, 1.4, -2.9]}
rawChipWaves["sandbox recorder"] = {"expression": 0.2, "samples": [5.0, -5.1, 4.0, -4.1, 3.0, -3.1, 2.0, -2.1, 1.0, -1.1, 6.0]}
rawChipWaves["sandbox ring pulse"] = {"expression": 1.0, "samples": [1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]}
rawChipWaves["sandbox saw bass"] = {"expression": 0.25, "samples": [1, 1, 1, 1, 0, 2, 1, 2, 3, 1, -2, 1, 4, 1, 4, 2, 1, 6, -3, 4, 2, 1, 5, 1, 4, 1, 5, 6, 7, 1, 6, 1, 4, 1, 9]}
rawChipWaves["sandbox shrill bass"] = {"expression": 0.5, "samples": [0, 1, 0, 0, 1, 0, 1, 0, 0, 0]}
rawChipWaves["sandbox shrill lute"] = {"expression": 0.94, "samples": [1.0, 1.5, 1.25, 1.2, 1.3, 1.5]}
rawChipWaves["sandbox shrill pulse"] = {"expression": 0.3, "samples": [4 -2, 0, 4, 1, 4, 6, 7, 3]}
rawChipWaves["todbox 1/3 pulse"] = {"expression": 0.5, "samples": [1.0, -1.0, -1.0]}
rawChipWaves["todbox 1/5 pulse"] = {"expression": 0.5, "samples": [1.0, -1.0, -1.0, -1.0, -1.0]}
rawChipWaves["todbox accordian"] = {"expression": 0.5, "samples": [0, 1, 1, 2, 2, 1.5, 1.5, 0.8, 0, -2, -3.25, -4, -4.5, -5.5, -6, -5.75, -5.5, -5, -5, -5, -6, -6, -6, -5, -4, -3, -2, -1, 0.75, 1, 2, 3, 4, 5, 6, 6.5, 7.5, 8, 7.75, 6, 5.25, 5, 5, 5, 5, 5, 4.25, 3.75, 3.25, 2.75, 1.25, -0.75, -2, -0.75, 1.25, 1.25, 2, 2, 2, 2, 1.5, -1, -2, -1, 1.5, 2,  2.75, 2.75, 2.75, 3, 2.75, -1, -2, -2.5, -2, -1, -2.25, -2.75, -2, -3, -1.75, 1, 2, 3.5, 4, 5.25, 6, 8, 9.75, 10, 9.5, 9, 8.5, 7.5, 6.5, 5.25, 5, 4.5, 4, 4, 4, 3.25, 2.5, 2, 1, -0.5, -2, -3.5, -4, -4, -4, -3.75, -3, -2, -1]}
rawChipWaves["todbox beta banana wave"] = {"expression": 0.8, "samples": [0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6, 0.5, 0.4, 0.2, 0.0]}
rawChipWaves["todbox beta test wave"] = {"expression": 0.5, "samples": [56, 0, -52, 16, 3, 3, 2, -35, 20, 147, -53, 0, 0, 5, -6]}
rawChipWaves["todbox harsh wave"] = {"expression": 0.45, "samples": [1.0, -1.0, -1.0, -1.0, 0.5, 0.5, 0.5, 0.7, 0.39, 1.3, 0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]}
rawChipWaves["todbox slap bass"] = {"expression": 0.5, "samples": [1, 0.5, 0, 0.5, 1.25, 0.5, -0.25, 0.1, -0.1, 0.1, 1.1, 2.1, 3, 3.5, 2.9, 3.3, 2.7, 2.9, 2.3, 2, 1.9, 1.8, 1, 0.7, 0.9, 0.8, 0.4, 0.1, 0.0, 0.2, 0.4, 0.6, 0.5, 0.8]}
rawChipWaves["trapezoid"] = {"expression": 1.0, "samples": [1.0/15.0, 6.0/15.0, 10.0/15.0, 14.0/15.0, 15.0/15.0, 15.0/15.0, 15.0/15.0, 15.0/15.0, 15.0/15.0, 15.0/15.0, 15.0/15.0, 15.0/15.0, 14.0/15.0, 10.0/15.0, 6.0/15.0, 1.0/15.0, -1.0/15.0, -6.0/15.0, -10.0/15.0, -14.0/15.0, -15.0/15.0, -15.0/15.0, -15.0/15.0, -15.0/15.0, -15.0/15.0, -15.0/15.0, -15.0/15.0, -15.0/15.0, -14.0/15.0, -10.0/15.0, -6.0/15.0, -1.0/15.0,]}
rawChipWaves["wackybox buzz wave"] = {"expression": 0.6, "samples": [0, 1, 1, 2, 4, 4, 4, 4, 5, 5, 6, 6, 6, 7, 8, 8, 8, 9, 9, 9, 9, 9, 9, 8, 8, 8, 11, 15, 23, 62, 61, 60, 58, 56, 56, 54, 53, 52, 50, 49, 48, 47, 47, 45, 45, 45, 44, 44, 43, 43, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 43, 43, 53]}
rawChipWaves["wackybox guitar string"] = {"expression": 0.6, "samples": [0, 63, 63, 63, 63, 19, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 11, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 27, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 34, 63, 63, 63, 63]}
rawChipWaves["wackybox intense"] = {"expression": 0.6, "samples": [36, 25, 33, 35, 18, 51, 22, 40, 27, 37, 31, 33, 25, 29, 41, 23, 31, 31, 45, 20, 37, 23, 29, 26, 42, 29, 33, 26, 31, 27, 40, 25, 40, 26, 37, 24, 41, 32, 0, 32, 33, 29, 32, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31]}
rawChipWaves["zefbox deep pulse"] = {"expression": 0.2, "samples": [1, 2, 2, -2, -2, -3, -4, -4, -5, -5, -5, -5, 0, -1, -2]}
rawChipWaves["zefbox deep sawtal"] = {"expression": 0.7, "samples": [0.75, 0.25, 0.5, -0.5, 0.5, -0.5, -0.25, -0.75]}
rawChipWaves["zefbox deep sawtooth"] = {"expression": 0.5, "samples": [0, 2, 3, 4, 4.5, 5, 5.5, 6, 6.25, 6.5, 6.75, 7, 6.75, 6.5, 6.25, 6, 5.5, 5, 4.5, 4, 3, 2, 1]}
rawChipWaves["zefbox deep square"] = {"expression": 1.0, "samples": [1.0, 2.25, 1.0, -1.0, -2.25, -1.0]}
rawChipWaves["zefbox high pulse"] = {"expression": 0.2, "samples": [1, -2, 2, -3, 3, -4, 5, -4, 3, -3, 2, -2, 1]}
rawChipWaves["zefbox pulse"] = {"expression": 0.5, "samples": [1.0, -2.0, -2.0, -1.5, -1.5, -1.25, -1.25, -1.0, -1.0]}
rawChipWaves["zefbox saw narrow"] = {"expression": 0.65, "samples": [1, 0.5, 1, 0.5, 1, 0.5, 1, 2, 1, 2 ,1]}
rawChipWaves["zefbox saw wide"] = {"expression": 0.65, "samples": [0.0, -0.4, -0.8, -1.2, -1.6 , -2.0, 0.0, -0.4, -0.8, -1.2, -1.6]}
rawChipWaves["zefbox sawtal"] = {"expression": 0.3, "samples": [1.5, 1.0, 1.25, -0.5, 1.5, -0.5, 0.0, -1.5, 1.5, 0.0, 0.5, -1.5, 0.5, 1.25, -1.0, -1.5]}
rawChipWaves["zefbox semi-square"] = {"expression": 1.0, "samples": [1.0, 1.5, 2.0, 2.5, 2.5, 2.5, 2.0, 1.5, 1.0]}
rawChipWaves["zefbox squaretal"] = {"expression": 0.7, "samples": [1.5, 1.0, 1.5, -1.5, -1.0, -1.5]}
rawChipWaves["zefbox triple pulse"] = {"expression": 0.4, "samples": [1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.5, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, 1.5]}

noteoffset = {}
noteoffset['B'] = 11
noteoffset['A♯'] = 10
noteoffset['A'] = 9
noteoffset['G♯'] = 8
noteoffset['G'] = 7
noteoffset['F♯'] = 6
noteoffset['F'] = 5
noteoffset['E'] = 4
noteoffset['D♯'] = 3
noteoffset['D'] = 2
noteoffset['C♯'] = 1
noteoffset['C'] = 0

def calcval(value):
	global jummbox_beatsPerBar
	global jummbox_ticksPerBeat
	return (value*(jummbox_beatsPerBar/jummbox_ticksPerBeat))/2

def addfx(inst_obj, fxgroupname, cvpj_instid, fxname):
	fx_pluginid = cvpj_instid+'_'+fxname
	plugin_obj = convproj_obj.add_plugin(fx_pluginid, fxgroupname, fxname)
	inst_obj.fxslots_audio.append(fx_pluginid)
	return plugin_obj

def add_eq_data(inst_obj, cvpj_instid, eqfiltbands):
	plugin_obj = addfx(inst_obj, 'universal', cvpj_instid, 'eq-bands')
	plugin_obj.visual.name = 'EQ'
	for eqfiltdata in eqfiltbands:
		eqgain_pass = eqfiltdata['linearGain']
		eqgain = (eqfiltdata['linearGain']-2)*6
		eqtype = eqfiltdata['type']

		filter_obj = plugin_obj.eq_add()
		filter_obj.freq  = eqfiltdata['cutoffHz']

		if eqtype == 'low-pass':
			filter_obj.type = 'low_pass'
			filter_obj.q = eqgain_pass
		if eqtype == 'peak':
			filter_obj.type = 'peak'
		if eqtype == 'high-pass':
			filter_obj.type = 'high_pass'
			filter_obj.q = eqgain_pass

def get_harmonics(harmonics_obj, i_harmonics):
	n = 1
	for i in i_harmonics:
		harmonics_obj.add(n, i/100, {})
		n += 1
	harmonics_obj.add(n, i_harmonics[-1]/100, {})
	harmonics_obj.add(n+1, i_harmonics[-1]/100, {})
	harmonics_obj.add(n+2, i_harmonics[-1]/100, {})

def parse_instrument(bb_instrument, bb_type, bb_color, bb_inst_effects, cvpj_instid):
	bb_volume = bb_instrument['volume']
	bb_preset = str(bb_instrument['preset']) if 'preset' in bb_instrument else None

	cvpj_volume = (bb_volume/50)+0.5

	a_decay = 3
	a_sustain = 1

	m_bank, m_inst, m_drum = dataset.midito_get('preset', bb_preset)

	if m_inst != None:
		inst_obj, plugin_obj = convproj_obj.add_instrument_from_dset(cvpj_instid, bb_preset, dataset, dataset_midi, bb_preset, None, bb_color)
	else:
		inst_obj = convproj_obj.add_instrument(cvpj_instid)
		inst_obj.pluginid = cvpj_instid

		bb_inst_type = bb_instrument['type']
		plugin_obj = convproj_obj.add_plugin(cvpj_instid, 'native-jummbox', bb_inst_type)

		if 'unison' in bb_instrument: plugin_obj.datavals.add('unison', bb_instrument['unison'])

		if bb_type == 'pitch': cvpj_instname, _ = dataset.object_get_name_color('inst', bb_inst_type)
		if bb_type == 'drum': cvpj_instname, _ = dataset.object_get_name_color('drums', bb_inst_type)

		if bb_inst_type == 'chip':
			bb_inst_wave = bb_instrument['wave']
			cvpj_instname = bb_inst_wave+' ('+cvpj_instname+')' if cvpj_instname != None else bb_inst_wave+' ('+bb_inst_type+')'
			if bb_inst_wave in rawChipWaves:
				wavesample = rawChipWaves[bb_inst_wave]['samples']
				wave_obj = plugin_obj.wave_add('chipwave')
				wave_obj.set_all(wavesample)

		if bb_inst_type == 'PWM':
			pulseWidth = bb_instrument['pulseWidth']
			cvpj_instname = str(pulseWidth)+'% pulse ('+cvpj_instname+')'
			param_obj = plugin_obj.params.add("pulse_width", pulseWidth/100, 'float')
			param_obj.visual.name = "Pulse Width"

		if bb_inst_type == 'harmonics':
			harmonics_obj = plugin_obj.harmonics_add('harmonics')
			get_harmonics(harmonics_obj, bb_instrument['harmonics'])

		if bb_inst_type == 'Picked String':
			harmonics_obj = plugin_obj.harmonics_add('harmonics')
			get_harmonics(harmonics_obj, bb_instrument['harmonics'])
			a_sustain = bb_instrument['stringSustain']/100

		if bb_inst_type == 'spectrum':
			plugin_obj.datavals.add('spectrum', bb_instrument['spectrum'])

		if bb_inst_type == 'FM':
			plugin_obj.datavals.add('algorithm', bb_instrument['algorithm'])
			plugin_obj.datavals.add('feedback_type', bb_instrument['feedbackType'])
			param_obj = plugin_obj.params.add("feedback_amplitude", bb_instrument['feedbackAmplitude'], 'int')
			param_obj.visual.name = "Feedback Amplitude"

			for opnum in range(4):
				opdata = bb_instrument['operators'][opnum]
				opnumtext = 'op'+str(opnum+1)+'/'
				plugin_obj.datavals.add(opnumtext+'frequency', opdata['frequency'])
				plugin_obj.datavals.add(opnumtext+'waveform', data_values.get_value(opdata, 'waveform', 'sine'))
				plugin_obj.datavals.add(opnumtext+'pulseWidth', data_values.get_value(opdata, 'pulseWidth', 0))
				plugin_obj.params.add(opnumtext+"amplitude", opdata['amplitude'], 'int')

		if bb_inst_type == 'custom chip':
			customChipWave = bb_instrument['customChipWave']
			customChipWave = [customChipWave[str(i)] for i in range(64)]
			wave_obj = plugin_obj.wave_add('chipwave')
			wave_obj.set_all_range(customChipWave, -24, 24)

		if bb_inst_type == 'FM6op': #goldbox
			plugin_obj.datavals.add('algorithm', bb_instrument['algorithm'])
			plugin_obj.datavals.add('feedback_type', bb_instrument['feedbackType'])
			param_obj = plugin_obj.params.add("feedback_amplitude", bb_instrument['feedbackAmplitude'], 'int')
			param_obj.visual.name = "Feedback Amplitude"

			for opnum in range(4):
				opdata = bb_instrument['operators'][opnum]
				opnumtext = 'op'+str(opnum+1)+'_'
				plugin_obj.datavals.add(opnumtext+'frequency', opdata['frequency'])
				plugin_obj.datavals.add(opnumtext+'waveform', data_values.get_value(opdata, 'waveform', 'sine'))
				plugin_obj.datavals.add(opnumtext+'pulseWidth', data_values.get_value(opdata, 'pulseWidth', 0))
				plugin_obj.params.add(opnumtext+"amplitude", opdata['amplitude'], 'int')

			if bb_instrument['algorithm'] == 'Custom': plugin_obj.datavals.add('customAlgorithm', bb_instrument['customAlgorithm'])

		inst_obj.visual.name = cvpj_instname
		inst_obj.visual.color = bb_color

		inst_obj.params.add('vol', cvpj_volume, 'float')

		if 'eqFilterType' in bb_instrument:
			if bb_instrument['eqFilterType'] == False and 'eqSubFilters0' in bb_instrument: 
				add_eq_data(inst_obj, cvpj_instid, bb_instrument['eqSubFilters0'])

			else:
				filter_hz = filtervals[bb_instrument['eqSimpleCut']]
				filter_peak = bb_instrument['eqSimplePeak']
				if filter_hz != None or filter_peak != 0:
					if filter_hz == None: filter_hz = 8000
					plugin_obj = addfx(inst_obj, 'universal', cvpj_instid, 'eq-bands')
					filter_obj = plugin_obj.eq_add()
					filter_obj.freq  = filter_hz
					filter_obj.type = 'low_pass'
					filter_obj.q = (filter_peak*2)+1

		elif 'eqFilter' in bb_instrument:
			bb_eqFilter = bb_instrument['eqFilter']
			if bb_eqFilter != []: 
				fx_pluginid, fx_plugindata = add_eq_data(inst_obj, cvpj_instid, bb_eqFilter)
				
		if 'echo' in bb_inst_effects:
			plugin_obj = addfx(inst_obj, 'universal', cvpj_instid, 'delay-c')
			plugin_obj.visual.name = 'Echo'
			plugin_obj.fxdata_add(1, 0.5)
			plugin_obj.datavals.add('time_type', 'steps')
			plugin_obj.datavals.add('time', bb_instrument['echoDelayBeats']*8)
			plugin_obj.datavals.add('feedback', bb_instrument['echoSustain']/240)
			
		if 'distortion' in bb_inst_effects:
			plugin_obj = addfx(inst_obj, 'simple', cvpj_instid, 'distortion')
			plugin_obj.visual.name = 'Distortion'
			param_obj = plugin_obj.params.add('amount', bb_instrument['distortion']/100, 'float')
			param_obj.visual.name = 'Amount'
			param_obj.min = 0
			param_obj.max = 1
		
		if 'bitcrusher' in bb_inst_effects:
			plugin_obj = addfx(inst_obj, 'universal', cvpj_instid, 'bitcrush')
			plugin_obj.visual.name = 'Bitcrusher'
			t_bits_val = round(xtramath.between_from_one(7, 0, bb_instrument['bitcrusherQuantization']/100))
			plugin_obj.params.add('bits', 2**t_bits_val, 'float')
			plugin_obj.params.add('freq', (bb_instrument['bitcrusherOctave']+1)*523.25, 'float')
			
		if 'chorus' in bb_inst_effects:
			plugin_obj = addfx(inst_obj, 'simple', cvpj_instid, 'chorus')
			plugin_obj.visual.name = 'Chorus'
			param_obj = plugin_obj.params.add('amount', bb_instrument['chorus']/100, 'float')
			param_obj.visual.name = 'Amount'
			param_obj.min = 0
			param_obj.max = 1
			
		if 'reverb' in bb_inst_effects:
			plugin_obj = addfx(inst_obj, 'simple', cvpj_instid, 'reverb')
			plugin_obj.visual.name = 'Reverb'
			reverblvl = data_values.get_value(bb_instrument, 'reverb', 40)
			plugin_obj.fxdata_add(1, reverblvl/100)
			
		if 'vibrato' in bb_inst_effects:
			if 'vibratoSpeed' in bb_instrument and 'vibratoDelay' in bb_instrument:
				if bb_instrument['vibratoSpeed'] != 0 and bb_instrument['vibratoDelay'] != 50:
					lfo_obj = plugin_obj.lfo_add('pitch')
					lfo_obj.predelay = (bb_instrument['vibratoDelay']/49)*2
					lfo_obj.speed_time = 0.7*(1/bb_instrument['vibratoSpeed'])
					lfo_obj.amount = bb_instrument['vibratoDepth']

		a_attack = data_values.get_value(bb_instrument, 'fadeInSeconds', 0)
		a_release = abs(data_values.get_value(bb_instrument, 'fadeOutTicks', 0)/(jummbox_ticksPerBeat*32))
		plugin_obj.env_asdr_add('vol', 0, a_attack, 0, a_decay, a_sustain, a_release, 1)
		return inst_obj

def parse_notes(cvpj_notelist, channum, bb_notes, bb_instruments):
	for note in bb_notes:
		points = note['points']
		pitches = note['pitches']

		pitches = [(x-48 + jummbox_key) for x in pitches]
		cvpj_note_dur = (points[-1]['tick'] - points[0]['tick'])

		arr_bendvals = []
		arr_volvals = []

		for point in points:
			arr_bendvals.append(point['pitchBend'])
			arr_volvals.append(point['volume'])

		maxvol = max(arr_volvals)
		t_vol = maxvol/100

		for bb_instrument in bb_instruments:
			t_instrument = 'bb_ch'+str(channum)+'_inst'+str(bb_instrument)
			cvpj_notelist.add_m_multi(t_instrument, points[0]['tick'], cvpj_note_dur, pitches, t_vol, {})

			ifnotsame_gain = (all(element == arr_volvals[0] for element in arr_volvals) == False) and maxvol != 0
			ifnotsame_pitch = (all(element == arr_bendvals[0] for element in arr_bendvals) == False)

			for point in points:
				auto_pos = point['tick']-points[0]['tick']

				if ifnotsame_gain: 
					autopoint_obj = cvpj_notelist.last_add_auto('gain')
					autopoint_obj.pos = auto_pos
					autopoint_obj.value = (point['volume']*(1/maxvol))

				if ifnotsame_pitch: 
					autopoint_obj = cvpj_notelist.last_add_auto('pitch')
					autopoint_obj.pos = auto_pos
					autopoint_obj.value = point['pitchBend']


def parse_channel(channeldata, channum, durpos):
	global jummbox_notesize
	global jummbox_beatsPerBar
	global jummbox_ticksPerBeat

	bb_color = None
	bb_type = channeldata['type']
	bb_instruments = channeldata['instruments']
	bb_patterns = channeldata['patterns']
	bb_sequence = channeldata['sequence']

	if bb_type == 'pitch' or bb_type == 'drum':
		if bb_type == 'pitch': bb_color = colors_pitch.getcolor()
		if bb_type == 'drum': bb_color = colors_drums.getcolor()

		for t_instnum, bb_instrument in enumerate(bb_instruments):
			bb_inst_effects = data_values.get_value(bb_instrument, 'effects', [])
			cvpj_instid = 'bb_ch'+str(channum)+'_inst'+str(t_instnum+1)
			inst_obj = parse_instrument(bb_instrument, bb_type, bb_color, bb_inst_effects, cvpj_instid)
			if 'panning' in bb_inst_effects: inst_obj.params.add('pan', bb_instrument['pan']/50, 'float')
			if 'detune' in bb_inst_effects: inst_obj.params.add('pitch', bb_instrument['detuneCents']/100, 'float')
			playlist_obj = convproj_obj.add_playlist(channum-1, 1, True)
			playlist_obj.visual.color = bb_color

		for patterncount, bb_pattern in enumerate(bb_patterns):
			nid_name = str(patterncount+1)
			cvpj_patid = 'bb_ch'+str(channum)+'_pat'+str(patterncount)
			bb_notes = bb_pattern['notes']
			if 'instruments' in bb_pattern: bb_instruments = bb_pattern['instruments']
			else: bb_instruments = [1]
			if bb_notes != []: 
				nle_obj = convproj_obj.add_notelistindex(cvpj_patid)
				nle_obj.visual.name = nid_name
				parse_notes(nle_obj.notelist, channum, bb_notes, bb_instruments)

		placement_pos = 0
		for partnum in range(len(bb_sequence)):
			bb_part = bb_sequence[partnum]
			bb_partdur = durpos[partnum]
			if bb_part != 0:
				playlist_obj = convproj_obj.add_playlist(channum-1, True, True)
				cvpj_placement = playlist_obj.placements.add_notes()
				cvpj_placement.fromindex =  'bb_ch'+str(channum)+'_pat'+str(bb_part-1)
				cvpj_placement.position = placement_pos
				cvpj_placement.duration = bb_partdur
			placement_pos += bb_partdur

	if bb_type == 'mod':
		modChannels = bb_instruments[0]['modChannels'] if 'modChannels' in bb_instruments[0] else None
		modInstruments = bb_instruments[0]['modInstruments'] if 'modInstruments' in bb_instruments[0] else None
		modSettings = bb_instruments[0]['modSettings'] if 'modSettings' in bb_instruments[0] else None

		if modChannels:
			bb_def = []
			for num in range(6):
				bb_def.append([modChannels[num],modInstruments[num],modSettings[num]])

			placement_pos = 0
			for partnum in range(len(bb_sequence)):
				bb_part = bb_sequence[partnum]
				bb_partdur = durpos[partnum]
				if bb_part != 0:
					bb_modnotes = bb_patterns[bb_part-1]['notes']
					if bb_modnotes != []:
						for note in bb_modnotes:
							bb_mod_points = note['points']
							bb_mod_pos = placement_pos+bb_mod_points[0]['tick']
							bb_mod_dur = bb_mod_points[-1]['tick'] - bb_mod_points[0]['tick']
							bb_mod_target = bb_def[(note['pitches'][0]*-1)+5]

							t_ap = []
							for bb_mod_point in bb_mod_points:
								if bb_partdur > bb_mod_point['tick']:
									t_ap.append([bb_mod_point['tick']-bb_mod_pos+placement_pos, bb_mod_point['volume']])

							autoloc, m_add, m_mul = None, 0, 1

							if bb_mod_target[0] == -1:
								if bb_mod_target[2] == 1:	autoloc, m_add, m_mul = ['master', 'vol'], 0, 0.01
								elif bb_mod_target[2] == 2:  autoloc, m_add, m_mul = ['main', 'bpm'], 30, 1
								elif bb_mod_target[2] == 17: autoloc, m_add, m_mul = ['main', 'bpm'], 250, 0.01
							else:
								auto_cvpj_instid = 'bb_ch'+str(bb_mod_target[0]+1)+'_inst'+str(bb_mod_target[1]+1)
								#print(bb_mod_t arget, cvpj_autodata)
								if bb_mod_target[2] == 6:	 autoloc, m_add, m_mul = ['track', auto_cvpj_instid, 'pan'], -50, 0.02
								elif bb_mod_target[2] == 7:   autoloc, m_add, m_mul = ['slot', auto_cvpj_instid+'_reverb', 'wet'], 0, 1/32
								elif bb_mod_target[2] == 8:   autoloc, m_add, m_mul = ['slot', auto_cvpj_instid+'_distortion', 'amount'], 0, 1/7
								elif bb_mod_target[2] == 15:  autoloc, m_add, m_mul = ['slot', auto_cvpj_instid, 'pitch'], -200, 1
								elif bb_mod_target[2] == 25:  autoloc = ['plugin', auto_cvpj_instid+'_bitcrush', 'bits']
								elif bb_mod_target[2] == 26:  autoloc = ['plugin', auto_cvpj_instid+'_bitcrush', 'freq']
								elif bb_mod_target[2] == 29:  autoloc, m_add, m_mul = ['plugin', auto_cvpj_instid+'_chorus', 'amount'], 0, 1/8
								elif bb_mod_target[2] == 36:  autoloc, m_add, m_mul = ['track', auto_cvpj_instid, 'vol'], 0, 0.04

								if bb_mod_target[2] == 25: 
									for s_ap in t_ap: s_ap[0] = 2**(7-s_ap[0])

								if bb_mod_target[2] == 26: 
									for s_ap in t_ap: s_ap[0] = (s_ap[0]+1)*523.25

							if autoloc:
								autopl_obj = convproj_obj.add_automation_pl('main/bpm', 'float')
								autopl_obj.position = bb_mod_pos
								autopl_obj.duration = bb_mod_dur

								for s_ap in t_ap: 
									autopoint_obj = autopl_obj.data.add_point()
									autopoint_obj.pos = s_ap[0]
									autopoint_obj.value = s_ap[1]

				placement_pos += bb_partdur

def get_durpos(jummbox_channels):
	global jummbox_notesize
	global jummbox_beatsPerBar
	global jummbox_ticksPerBeat

	autodur = {}
	sequencelen = None

	for jummbox_channel in jummbox_channels:
		bb_type = jummbox_channel['type']
		bb_instruments = jummbox_channel['instruments']
		bb_patterns = jummbox_channel['patterns']
		bb_sequence = jummbox_channel['sequence']
		if sequencelen == None: sequencelen = [jummbox_beatsPerBar*jummbox_ticksPerBeat for _ in range(len(bb_sequence))]

		if bb_type == 'mod':
			modChannels = bb_instruments[0]['modChannels'] if 'modChannels' in bb_instruments[0] else None
			modInstruments = bb_instruments[0]['modInstruments'] if 'modInstruments' in bb_instruments[0] else None
			modSettings = bb_instruments[0]['modSettings'] if 'modSettings' in bb_instruments[0] else None

			if modChannels:
				nextbarfound = None
				for num in range(6):
					autodef = [modChannels[num],modInstruments[num],modSettings[num]]
					if autodef == [-1, 0, 4]:
						nextbarfound = num
						break

				if nextbarfound != None:
					patnum = 1
					for bb_pattern in bb_patterns:
						for autonotedata in bb_pattern['notes']:
							if autonotedata['pitches'][0] == 5-num:
								autodur[patnum] = autonotedata['points'][0]['tick']
						patnum += 1

					for seqnum in range(len(bb_sequence)):
						if bb_sequence[seqnum] in autodur:
							if sequencelen[seqnum] > autodur[bb_sequence[seqnum]]: sequencelen[seqnum] = autodur[bb_sequence[seqnum]]

	return sequencelen


class input_jummbox(plugin_input.base):
	def __init__(self): pass
	def is_dawvert_plugin(self): return 'input'
	def getshortname(self): return 'jummbox'
	def getname(self): return 'jummbox'
	def gettype(self): return 'mi'
	def getdawcapabilities(self): 
		return {
		'track_lanes': True,
		}
	def supported_autodetect(self): return False
	def parse(self, i_convproj_obj, input_file, extra_param):
		global convproj_obj

		global dataset
		global dataset_midi

		global colors_pitch
		global colors_drums

		global jummbox_beatsPerBar
		global jummbox_ticksPerBeat
		global jummbox_key

		convproj_obj = i_convproj_obj
		convproj_obj.type = 'mi'
		convproj_obj.set_timings(8, True)

		dataset = dv_dataset.dataset('./data_dset/beepbox.dset')
		dataset_midi = dv_dataset.dataset('./data_dset/midi.dset')

		colors_pitch = colors.colorset(dataset.colorset_e_list('inst', 'beepbox_dark'))
		colors_drums = colors.colorset(dataset.colorset_e_list('drums', 'beepbox_dark'))

		bytestream = open(input_file, 'r', encoding='utf8')
		jummbox_json = json.load(bytestream)

		convproj_obj.track_master.params.add('vol', jummbox_json['masterGain'] if 'masterGain' in jummbox_json else 1, 'float')
		if 'name' in jummbox_json: convproj_obj.metadata.name = jummbox_json['name']
		
		jummbox_key = noteoffset[jummbox_json['key']]
		jummbox_channels = jummbox_json['channels']
		jummbox_beatsPerBar = jummbox_json['beatsPerBar']
		jummbox_ticksPerBeat = jummbox_json['ticksPerBeat']
		jummbox_beatsPerMinute = jummbox_json['beatsPerMinute']

		global jummbox_notesize
		global ppq_data
		
		jummbox_notesize = jummbox_beatsPerBar*jummbox_ticksPerBeat
		ppq_data = jummbox_notesize*4

		durpos = get_durpos(jummbox_channels)
		patlentable = [x for x in get_durpos(jummbox_channels)]

		convproj_obj.timesig = [4,8]
		convproj_obj.patlenlist_to_timemarker(patlentable, -1)

		#if 'introBars' in jummbox_json and 'loopBars' in jummbox_json:
		#	introbars = sum(patlentable[0:jummbox_json['introBars']])
		#	loopbars = (sum(patlentable[0:jummbox_json['loopBars']]) + introbars)
		#	convproj_obj.loop_active = True
		#	convproj_obj.loop_start = introbars
		#	convproj_obj.loop_end = loopbars if loopbars else patlentable[-1]

		for chancount, jummbox_channel in enumerate(jummbox_channels):
			parse_channel(jummbox_channel, chancount+1, durpos)

		convproj_obj.do_actions.append('do_addloop')
		convproj_obj.params.add('bpm', jummbox_beatsPerMinute, 'float')
