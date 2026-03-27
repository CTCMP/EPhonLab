#!/bin/sh
#PBS -N elphonlab
#PBS -j oe
#PBS -q workq
#PBS -l select=1:ncpus=40:host=node01:mpiprocs=40
#PBS -V
cd $PBS_O_WORKDIR

export I_MPI_HYDRA_BOOTSTRAP=ssh
source /share/intel/2022.2/setvars.sh
module load gcc/10.2.0
export PATH=/share/home/jinxin/soft/QE/q-e-qe-7.2/bin:$PATH
export PATH=/share/home/jinxin/soft/shengbte/thirdorder:$PATH


echo -n "start time  " > time 
date >> time
#######################################################
mpirun -np 40 /share/home/jinxin/soft/QE/q-e-qe-7.2/bin/pw.x < scf.in > scf.log
mpirun -np 40 /share/home/jinxin/soft/QE/q-e-qe-7.2/bin/pw.x < nscf.in > nscf.log
#######################################################
echo -n "End time  " >> time
date >> time