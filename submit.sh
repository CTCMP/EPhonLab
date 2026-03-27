#!/bin/sh
#PBS -N w90
#PBS -j oe
#PBS -q workq
#PBS -l select=1:ncpus=40:host=sr850:mpiprocs=40
#PBS -V
cd $PBS_O_WORKDIR

echo -n "start time  " > time
export I_MPI_HYDRA_BOOTSTRAP=ssh
date >> time
source /share/intel/2022.2/setvars.sh
module load gcc/10.2.0
