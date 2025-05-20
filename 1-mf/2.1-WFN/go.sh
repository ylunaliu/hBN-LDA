#!/bin/bash
#SBATCH -q regular
#SBATCH -C gpu
#SBATCH -t 01:30:00
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-node=4
#SBATCH --gpu-bind=map_gpu:0,1,2,3
#SBATCH -A m3571
#SBATCH -e sigma.err
export TEMPDIRPATH=$SCRATCH/tmp
export OMP_NUM_THREADS=16
export SLURM_CPU_BIND="cores"
export MPIEXEC="`which srun` "
BGW_PATH=/global/homes/l/lunaliu/software/BerkeleyGW-master/bin
# srun -c 16 $BGW_PATH/hdf2wfn.x BIN WFN_pseudo.h5 WFN >& hdf2wfn.out
srun -c 16 $BGW_PATH/parabands.cplx.x >& parabands.out