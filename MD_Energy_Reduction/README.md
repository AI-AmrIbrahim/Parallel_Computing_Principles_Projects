# Assignment
Given a system of 𝑁 = 11 × 11 × 11 particles placed, initially,
on the grid points of a 3D box of dimensions 10 × 10 × 10, i.e.,
at (0,0,0), (1, 0, 0), …, (10, 10, 10) you place your particles. The
particles 𝑖 and 𝑗 interact with the so-called Lenard-Jones
potential (ignoring constants)

$$V_{ij} = \frac{1}{(r_{ij}^{12} )} - \frac{2}{(r_{ij}^{6} )}$$

where $r_{ij}=|x_i-x_j|$ is the distance between the two particles.
The total energy for the system is

$$𝐸 = \frac{1}{2} \sum_{j!=i}^{N} V_{ij}$$

Please complete the following:
1. Design algorithm(s) to reduce the total energy E of the system by kicking them around.
The method suggested is a truncated “Monte Carlo”; project’s goal is to parallelize the energy
calculations rather than a creative MC method.
2. Implement your algorithm(s) on a parallel computer 𝑃 = 2), 2', 21 cores.
3. Here are the detailed steps:
    * Generate the initial coordinates and compute the corresponding initial energy 𝐸3.
    * Kick your particles by a random vector of max random length 0.5.
      * The random vector length can deviate a little from the suggested 0.5.
      * Free to kicking one, a few, or all N particles at a time.
      * Discard the moves that do not reduce the total energy.
      * If a particle is kicked off your box, bring them back by periodic conditions.
    * Repeat the above for a fixed 100 steps regardless of energy change to be up/down/flat. Record the energies of the steps if it’s lowered.
4. Report your timing for the three experiments of energy reductions. To be fair for all three
core cases, please select the same/similar conditions.
# Mini-report
## Program
I used python as my programing language using mpi4py. My implementation follows the
steps recommended in the 4.4 problem statement document:

1. Generate initial coordinates and compute the corresponding initial energy: The
    algorithm starts by distributing the number of particles among processes. This is done
    through integer division of N by the number of processes and distributing the remaining
    particles among the processes to reduce load imbalance. Initial coordinates are generated
    using a mesh grid and column stacking the flattened meshes, resulting in particles placed
    at box grid points (0,0,0) ... (10,10,10). All processes run the initial coordinate
    generation function since all processes require the full coordinates to compute energy.
    Computation of energy is done locally, then gathered to compute the total energy. Since
    particles are distributed among processes, each process computes the energy for its
    corresponding particles, generating local energy. Local energies are then reduced to rank
    0 with the SUM operation, generating total energy.
2. Kick your particles by a random vector of max length 0. 01 : Each process moves its own
    fraction of randomly chosen particles by a vector of random values from – 0. 01 to 0. 01
    using a uniform random function. Particles that exceed the box are returned to the box
    bounced back into the box. The fraction of particles moved is varied [0.1,0.5, 0.9] in
    order to compare performance among different sizes of particles moved.
3. Repeat step 2 for a fixed 100 steps and record the energies of the steps if its lowered: If a kick/move does not reduce the total energy, then the move is rejected. The implementation utilizes the Metropolis criterion to accept or reject a move. If the new energy is lower than the previous energy, the move is accepted, and the coordinates are updated. However, if the energy is equal to or higher than the previous energy, then the move can be accepted with a probability of $𝑒^{-\frac{∆𝐸}{𝑇}}$, ∆𝐸 = $𝐸_{𝑙𝑜𝑐𝑎𝑙_𝑖}−𝐸_{𝑙𝑜𝑐𝑎𝑙_{𝑖− 1}}$, 𝑇 is a constant
parameter (temperature). This allows for the program to avoid being stuck at a local
minimum. For each iteration, each process moves its corresponding particles, computes,
and compares its local energies. At the end of the iteration, the local coordinates are all
gathered to all processes and a new total energy is reduced to rank 0.

Additionally, the Slurm script is designed to iterate through the number of processors. As
a result, when running the Python script, two loops are executed: one for the processors specified in the Slurm file and another for the fraction size within the Python file. This allows for a comprehensive evaluation of performance. Time is compute right before distributing the particles and ends right after computing the final energy reduction iteration.
## Results
I extracted data from the output file, which was in the format
```
P = %d
Fraction = %f
Initial Energy = %f
Iteration i = %f
Minimum Energy = %f
Time elapsed = %f
```
Using these values, I generated Table 1, which includes not only the extracted values but also the speedup calculated as 𝑆 = $\frac{𝑇_1}{𝑇_𝑃}$ where $𝑇_1$ is time elapsed for a single process and $𝑇_P$ is time elapsed for P processes for a given fraction. Finally, I generated the Speedup plot in Figure 1.
|   P   	| Fraction 	| Initial Energy 	|    Minimum Energy   	|    Elapsed Time   	| Avg Time among Fractions 	|  Speedup  	|
|:-----:	|:--------:	|:--------------:	|:-------------------:	|:-----------------:	|:------------------------:	|:---------:	|
|   1   	|    0.1   	|  -6010.790303  	|     -6012.317775    	|     682.897049    	|        685.644075        	|  1.000000 	|
|   1   	|    0.5   	|  -6010.790303  	|     -6013.365855    	|     686.969769    	|        685.644075        	|  1.000000 	|
|   1   	|    0.9   	|  -6010.790303  	|     -6014.390053    	|     687.065407    	|        685.644075        	|  1.000000 	|
| $2^2$ 	|    0.1   	|  -6010.790303  	|     -6012.666469    	|     169.902790    	|        169.914420        	|  4.035232 	|
| $2^2$ 	|    0.5   	|  -6010.790303  	|     -6013.317135    	|     169.922742    	|        169.914420        	|  4.035232 	|
| $2^2$ 	|    0.9   	|  -6010.790303  	|     -6014.429257    	|     169.917729    	|        169.914420        	|  4.035232 	|
| $2^4$ 	|    0.1   	|  -6010.790303  	|     -6011.842052    	|      47.136176    	|         46.668212        	| 14.691886 	|
| $2^4$ 	|    0.5   	|  -6010.790303  	|     -6012.668914    	|      46.409920    	|         46.668212        	| 14.691886 	|
| $2^4$ 	|    0.9   	|  -6010.790303  	|     -6012.040993    	|      46.458540    	|         46.668212        	| 14.691886 	|
| $2^6$ 	|    0.1   	|  -6010.790303  	|     -6012.372502    	|      13.713184    	|         13.231111        	| 51.820597 	|
| $2^6$ 	|    0.5   	|  -6010.790303  	|     -6012.035503    	|      12.980711    	|         13.231111        	| 51.820597 	|
| $2^6$ 	|    0.9   	|  -6010.790303  	|     -6011.637690    	|      12.999438    	|         13.231111        	| 51.820597 	|

Table 1. Elapsed Time and Speedup across different P and Fraction values

![image](https://github.com/user-attachments/assets/5341c0d7-fe9e-4e14-a58b-0e33c9281efa)

Figure 1. Speedup graph of Molecular Dynamics (MD) Truncated Monte Carlo Energy reduction
(generated using [project4_speedup.py](project4_speedup.py))
## Analysis
Here we compared the elapsed time and speedup of MD energy reduction across different
number of processors and fraction sizes. As shown in Figure 1 the speed up increases with
number of processes.

As shown in [project4.out](project4.out) within each number of processes fraction sizes the only difference is the number of possible iterations that reduce energy where 0.1 fraction size has more iterations overall and 0.9 fraction size has the least number of iterations. Among the different number of processes, the is no significant difference within minimum energy or number of iterations the only apparent difference is the elapsed time which is expected.

I have done some edits to my implementation after my presentation where I learned about
Lenard-Jones potential having a lower limit. The changes I made were (1) decreasing the
move/kick size from 0.5 to 0.01 since 0.5 was considerably a large kick size that skyrocketed the potential since particles more often than not would be too close to each other (2) changing the boundary condition from periodic conditions using modulus to bounce back boundary condition. After applying those two edits my energy reduction algorithm produced reasonable results which
did not skyrocket and there was a reduction in the system energy.
