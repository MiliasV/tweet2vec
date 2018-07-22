#!/bin/bash

# specify data file here
datafile="../misc/processed_tweets2.txt"

# specify model path here
modelpath="best_model/"

# specify result path here
resultpath="result/"

mkdir -p $resultpath

# test
python2 encode_char.py $datafile $modelpath $resultpath
