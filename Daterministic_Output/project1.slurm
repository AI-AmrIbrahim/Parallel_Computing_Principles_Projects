#!/bin/bash
#
#SBATCH --job-name=project1
#SBATCH --output=project1.out
#SBATCH --ntasks-per-node=20
#SBATCH --nodes=1
#SBATCH --time=02:00
#SBATCH -p short-28core

module load anaconda/2
module load mvapich2/gcc/64/2.2rc1

mpirun -np 20 python ~/AMS530/project1.py
