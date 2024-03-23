#!/bin/bash

input_data=$2 #first input
text=$4 #second input

python3 Canny.py --path "$input_data" --text "$text"