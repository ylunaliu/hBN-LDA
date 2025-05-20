#!/bin/bash
#SBATCH -J fin_Q
#SBATCH -o myjob.o\%j
#SBATCH -e myjob.e\%j
#SBATCH -p development
#SBATCH -N 40
#SBATCH -n 2160
#SBATCH -t 02:00:00
#SBATCH -A PHY20032

#QEPATH='/global/homes/b/bwhou/software/qe-6.7/bin'
BGWPATH1='/home1/08237/bwhou/software/BerkeleyGW-3.0.1/bin/'


cd inteqp
ibrun $BGWPATH1/inteqp.cplx.x > inteqp.out
cd ../
for ((i=1;i<=27;i++));
do
cd ./Q-$i
cd ./5.1-kernel-Q
ibrun   $BGWPATH1/kernel.cplx.x > kernel.out
cd ../5.2-absorp-Q
ibrun  $BGWPATH1/absorption.cplx.x > absorption.out
cd ../../
done