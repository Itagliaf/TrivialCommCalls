#! /bin/bash

#PBS -N TrivPar
#PBS -l select=1:ncpus=3:mem=12GB
#PBS -q parallel
#PBS -l walltime=00:10:00
#PBS -A cin_staff

source venv/bin/activate
module load autoload python/2.7.9

cd $PBS_O_WORKDIR

STARTTIME_S=$(date +%s)
echo -e "Starting serial version"
python TrivialCommonCalls3.py -i ../input_trivial/ -o ../out_serial/
ENDTIME_S=$(date +%s)


STARTTIME_P=$(date +%s)
echo -e "Starting parallel version"
python TrivialCommonCalls3_parallel.py -i ../input_trivial/ -o ../out_parallel/
ENDTIME_P=$(date +%s)

echo "Elapsed time SERIAL (s): $(($ENDTIME_S-STARTTIME_S))"
echo "Elapsed time PARALLEL (s): $(($ENDTIME_P-STARTTIME_P))"
