#!/bin/bash

logdir=${HOME}/logs
mkdir -p $logdir
cd scripts
chmod +x *.sh

echo "Running setup... (this may take a while, depending on your network speed)"
./setup.sh
echo "Running JSONAlgebra experiments... (this may take a few hours)"
./run-JSONAlgebra.sh
echo "Creating charts and summary..."
./run-evaluation.sh
echo "Done: Results are in ${HOME}/results."
