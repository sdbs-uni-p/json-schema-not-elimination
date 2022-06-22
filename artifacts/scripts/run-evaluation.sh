#!/bin/bash
cd ${HOME}/charts
python3 evaluate.py
cp -r results/. ${HOME}/results
