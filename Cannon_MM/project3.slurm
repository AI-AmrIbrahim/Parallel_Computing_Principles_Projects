#!/bin/bash
#SBATCH --job-name=project3
#SBATCH --output=project3.out
#SBATCH --time=30:00
#SBATCH -p short-96core
#SBATCH --nodes=1

module load anaconda/2
module load mvapich2/gcc/64/2.2rc1

# Array of processor numbers
procs=(1 4 16 64)
#procs=(16 64)

# Run the Python script with different number of processors
for P in "${procs[@]}"; do
    mpirun -np $P python project3.py $P
done
