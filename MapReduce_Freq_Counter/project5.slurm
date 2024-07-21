#!/bin/bash
#
#SBATCH --job-name=project1
#SBATCH --output=output.log
#SBATCH --ntasks-per-node=4
#SBATCH --nodes=1
#SBATCH --time=05:00
#SBATCH -p short-28core

module load anaconda/2
module load mvapich2/gcc/64/2.2rc1

mpirun -np 4 python /gpfs/projects/AMS598/class2023/amibrahim/project1/project1.py
