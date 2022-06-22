#!/bin/bash
export MAVEN_OPTS="-Xmx10240m"
cd "${BASH_SOURCE%/*}/"
# The following experiments are run without interpreting OneOf as AnyOf

echo "Running experiments on positive sample dataset (1/2)..."
./run-experiments.sh negated_sample

echo "Running experiments on negated sample dataset (2/2)..."
./run-experiments.sh positive_sample
