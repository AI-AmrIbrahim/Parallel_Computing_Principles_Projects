#!/bin/bash
#
#SBATCH --job-name=p3
#SBATCH --output=p3.log
#SBATCH --ntasks-per-node=10
#SBATCH --nodes=1
#SBATCH --time=30:00
#SBATCH -p short-40core

module load anaconda/2
module load mvapich2/gcc/64/2.2rc1

mpirun -np 10 python project3.py
