#!/bin/bash

# Build our tool
export MAVEN_OPTS="-Xmx10240m"
cd ${HOME}/JSONAlgebra
mvn clean install -DskipTests -pl jsonschema-refexpander,JsonSchema_To_Algebra
