# Negation-Closure for JSON Schema - Reproduction Package

This is a reproduction package for the article "Negation-Closure for JSON Schema",
by Mohamed-Amine Baazizi, Dario Colazzo, Giorgio Ghelli, Carlo Sartiani, and Stefanie Scherzinger.

This reproduction package has been created by Stefan Klessinger.
The package is provided as a Docker container.

Our original results are provided in directory [results](artifacts/results). These files are overwritten if you calculate new results in the container. 

## Setting up the Docker container
To build the container run ``docker build -t js_repro .`` (mind the dot) inside the root directory of this repository.

After building you can start the container with ``docker run -it js_repro``. 

## Running experiments
We provide a number of scripts for running our experiments inside the container.

To run all experiments, execute ``./doAll.sh``. Note that this can take **several hours**.
For this reason, we also make our original results available. 

There are several scripts in [scripts](artifacts/scripts) with the following functionality:

* ``./run-evaluation.sh`` performs the evaluation on the data in [results](artifacts/results). The resulting charts (as PDF) and a summary text file containing the statistics shown as tables in the paper are also stored [results](artifacts/results).

* ``./run-JSONAlgebra`` performs the experiments without the evaluation. Note that the originals results we provide are overwritten by this script.

* ``./setup.sh`` builds and installs our tool. You do **not** have to run this in order to use the scripts above.

* ``run-experiments.sh`` is used to run our tool on specific datasets. It takes an input folder as a parameter, specified as a path relative to [JSONAlgebra/JsonSchema_To_Algebra/tcs_data/](artifacts/JSONAlgebra/JsonSchema_To_Algebra/tcs_data/)

## Comparing the Results
To compare the computed results with the results stated in the paper, inspect the file summary.txt in the directory [results](artifacts/results) after running ``./doAll.sh`` or ``./run-evaluation.sh``.

## Generating Charts
To generate charts, execute ``./run-evaluation.sh``. The generated charts are stored in [results](artifacts/results).

## Moving Results to the Host System
All results are stored at /home/repro/results in the container. To copy the results to the host system, use ``docker cp <containerID>:/home/repro/results .`` after obtaining the containerID using ``docker ps``

## Remarks
We have some additional remarks about this reproduction package and its configuration:

* It is possible to specify a timeout. To do so the parameter 'false' in [run-experiments](artifacts/scripts/run-experiments.sh) (line 12) needs to be changed to 'true X' where X is the timeout in milliseconds. We decided not to specify a timeout in the standard configuration because it might greatly change the results, depending on the system. During our experiments, a timeout of 1 200 000ms was set.

* For the purpose of easier comparability of the charts with those in the submitted paper, the limits of the charts are set to a fixed value. Note that on a considerably slower machine, some points might be missing on charts showing the runtime.

* We sometimes experienced that Maven builds got stuck in a downloading step. In this case, please abort the script you ran by pressing CTRL-C and run the same script again. Note that it might be necessary to press CTRL-C multiple times, e.g., when running doAll.sh, to also abort subsequent commands.