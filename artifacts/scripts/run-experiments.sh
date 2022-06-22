#!/bin/bash

dataset=$1
out_dir=${HOME}/results//${dataset//\//-}
mkdir -p ${out_dir}
log_path=${out_dir}/${dataset//\//-}

cd ${HOME}/JSONAlgebra
rm ${HOME}/JSONAlgebra/JsonSchema_To_Algebra/test/${dataset}/results/*

mvn exec:java -Dexec.mainClass="it.unipi.di.tesiFalleniLandi.JsonSchema_to_Algebra.MassiveTesting.MainClass" \
        -Dexec.args="${HOME}/JSONAlgebra/JsonSchema_To_Algebra/tcs_data/${dataset} 1 false" -pl JsonSchema_To_Algebra \
        2> ${log_path}-err.log

cp ${HOME}/JSONAlgebra/JsonSchema_To_Algebra/tcs_data/${dataset}/results/*_results.csv ${HOME}/results/${dataset//\//-}/results.csv 2> /dev/null
cp ${HOME}/results/${dataset//\//-}/results.csv ${HOME}/charts/data/${dataset//\//-}/results.csv

cp ${HOME}/JSONAlgebra/JsonSchema_To_Algebra/tcs_data/${dataset}/results/*_size.csv ${HOME}/results/${dataset//\//-}/size.csv 2> /dev/null
cp ${HOME}/results/${dataset//\//-}/size.csv ${HOME}/charts/data/${dataset//\//-}/size.csv
