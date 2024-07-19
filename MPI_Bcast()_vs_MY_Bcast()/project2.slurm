#!/bin/bash
#SBATCH --job-name=project2
#SBATCH --output=project2.out
#SBATCH --time=30:00
#SBATCH -p short-40core
#SBATCH --nodes=1

module load anaconda/2
module load mvapich2/gcc/64/2.2rc1

# Array of processor numbers
procs=(4 7 28 37)

# Run the Python script with different number of processors
for P in "${procs[@]}"; do
    mpirun -np $P python project2.py $P
done
