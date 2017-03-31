#! /bin/bash

#PBS -N TrivPar
#PBS -l select=1:ncpus=3:mem=12GB
#PBS -q parallel
#PBS -l walltime=00:30:00
#PBS -A cin_staff

cd $PBS_O_WORKDIR

source venv/bin/activate
module load autoload python/2.7.9

# STARTTIME_S=$(date +%s)
# echo -e "Starting serial version"
# python TrivialCommonCalls3.py -i ../input_trivial/ -o ../out_serial/
# ENDTIME_S=$(date +%s)


STARTTIME_P=$(date +%s)
echo -e "Starting parallel version"
python TrivialCommonCalls3_parallel.py -i ../input_trivial/ -o ../out_parallel/
ENDTIME_P=$(date +%s)

#echo "Elapsed time SERIAL (s): $(($ENDTIME_S-STARTTIME_S))"
echo "Elapsed time PARALLEL version 2 (s): $(($ENDTIME_P-STARTTIME_P))"
