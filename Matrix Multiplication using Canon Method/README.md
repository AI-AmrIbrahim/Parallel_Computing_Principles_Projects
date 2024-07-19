# Assignment
Please implement one algorithm (chosen between Ring method, aka Canon
method, and the BMR method) for multiplying a pair of large square matrices
𝐴 ∈ $𝑅^{N×N}$ and 𝐵 ∈ $𝑅^{N×N}$ where $𝐴_{ij}$, $𝐵_{ij}$ ~ 𝑈(−1.0, 1.0)
on a parallel computer with 𝑃 cores and any interconnection networks available to you.
Please do:
(1) Describe the algorithm for multiplying the pair of matrices.
(2) Implement your algorithm.
(3) Test the performances of your algorithm with cores 𝑃 = $2^{2}$, $2^{4}$, $2^{6}$ for 𝑁 =
$2^{10}$, $2^{20}$, $2^{30}$ (as big as you can fit in your machine).
(4) Collect your performance results for the above 9 experiments, i.e., for each 𝑃 value,
you perform timing experiments for thee 𝑁 values.
(5) Plot the speedup curves.
(6) Comment on your performance results.
# Mini-report
## Problem Description
This project the task was to implement Matrix-Matrix multiplication algorithm using
either Cannon or BMR methods. Performance of the implemented algorithm would then be
assessed with various number of processes P [ 1 , $2^{2}$ , $2^{4}$ , $2^{6}$ ] and various matrix sizes N
[ $2^{8}$ , $2^{10}$ , $2^{12}$ ] I stopped at $2^{12}$ since after that I get memory errors.
## Program
I used python as my programing language using mpi4py. I am implementing Cannon
which is also known as Row-Partition A, Column-Partition B. As the second name suggest, how
this process works is by partitioning A by rows and partitioning B by columns. Then after
computing the partitioned multiplication rows of A are rolled up by a processor unit or partition
size while keeping B partitions unchanged. This process is repeated until all values of C have
been computed. A benefit of this method is that for each value of C ie C11 there is no need for
additions across processes since each process gets a partition of rows of A and columns of B.

My algorithm starts out with the creation of the matrices A and B using numpy uniform
and only process 0 would have full A and B. Wtime is called to get the start time before calling
cannon. Cannon performs numpy matmul of A and B if the number of processes is 1 and if the
number of processes is not a perfect square raise an error. Passing the first 2 conditions cannon
process is initiated where number of rows per partition is calcauted and A is scattered among
processes. I couldn’t scatter B across processes due to what I believe scatter does partition by
rows rather than columns therefore I partitioned B manually across processes. This concludes the
initial partitioning phase each process has its own local_A and local_B representing their
respective partitions of A and B.

Multiplication and rollup phase is a for loop looping number of processes times.
Local_C is computed by numpy matmul of local_A and local_B and added to a list called
local_C_list. Since the computation of C is filled in a lower diagonal manner as in:

| Step 1 	| Step 3 	| Step 2 	|
|---------|---------|---------|
| Step 2 	| Step 1 	| Step 3 	|
| Step 3 	| Step 2 	| Step 1 	|

The addition of local_C to local_C_list is added to the beginning of local_C_list if
inequality step >= size – rank is satisfied this if not then local_C is appended to the end of
local_C_list this ensures that local_C_list are in order and ready for concatenation. For the
rolling up of A I used the MPI tool Sendrecv_replace this allows each process to efficiently
rollup A without taking in extra space.

The final step is constructing C where each respective local_C_list is concatenated after
concluding the for loop. The result of concatenation is a vector per process those are gathered
into process 0 and concatenated to finalize the construction of matrix C. After finishing up the
cannon algorithm Wtime is called for the end time where root 0 would compute and output the
time taken cannon for each P and N combination.

Additionally, the Slurm script is designed to iterate through the number of processors. As
a result, when running the Python script, two loops are executed: one for the processors specified
in the Slurm file and another for the matrix size within the Python file. This allows for a
comprehensive evaluation of performance.
## Results
I extracted data from the output file, which was in the format "N = %d, P = %d, Cannon
time elapsed = %f." Using these values, I generated Table 1, which includes not only the
extracted values but also the speedup calculated as 𝑆= $𝑇_1/𝑇_𝑃$ where $𝑇_1$ is time elapsed for a single
process and $𝑇_𝑃$ is time elapsed for P processes for a given N. Finally, I generated the Speedup
plot in Figure 1.
|   P   	|    N   	 |   Elapsed Time   	|      Speedup     	|
|:-----:	|:------:	 |:----------------:	|:----------------:	|
|   1   	|  $2^8$ 	 |      0.020522    	|      1.000000    	|
|   1   	| $2^{10}$ |      0.297238    	|      1.000000    	|
|   1   	| $2^{12}$ |     13.713407    	|      1.000000    	|
| $2^2$ 	|  $2^8$ 	 |      0.019018    	|      1.079078    	|
| $2^2$ 	| $2^{10}$ |      0.111422    	|      2.667667    	|
| $2^2$ 	| $2^{12}$ |      4.179950    	|      3.280758    	|
| $2^4$ 	|  $2^8$ 	 |      0.022748    	|      0.902171    	|
| $2^4$ 	| $2^{10}$ |      0.051578    	|      5.762925    	|
| $2^4$ 	| $2^{12}$ |      1.773715    	|      7.731460    	|
| $2^6$ 	|  $2^8$ 	 |      0.202240    	|      0.101475    	|
| $2^6$ 	| $2^{10}$ |      0.037751    	|      7.873645    	|
| $2^6$ 	| $2^{12}$ |      0.803213    	|     17.073191    	|

Table 1. Elapsed Time and Speedup across different P and N values

![image](https://github.com/user-attachments/assets/d2d3671c-cca4-46e9-bfbf-be2a323226c7)

Figure 1. Speedup graph of NxN matrix multiplication (code snippet is available in the appendix)
## Analysis
Here we compared the elapsed time and speedup of Cannon functions across different
number of processors and matrix sizes. As shown in Figure 1 the speed up increases with number
of processes if the matrix size was big as shown in the green line where N = 4096 the line is
close to ideal speedup of slope = 1. However, for smaller matrix size the speedup diminishes as it
goes to 0 as the number of processes increases. In class Dr. Deng was surprised by how fast P =
1 and N = 4096 was computed in around 14 seconds. I used numpy.multmal which I believe is
optimized to compute matrix multiplication in a very time efficient manner.
## Appendix
```
import pandas as pd
import matplotlib.pyplot as plt
data = {
'N': [256, 1024, 4096]*4,
'P': [1]*3 + [4]*3 + [16]*3 + [64]*3,
'Time': [0.020522356033325195, 0.2972376346588135, 13.713406801223755,
0.01901841163635254, 0.11142230033874512, 4.179950475692749,
0.02274775505065918, 0.05157756805419922, 1.7737150192260742,
0.2022397518157959, 0.037750959396362305, 0.8032128810882568]}
df = pd.DataFrame(data)
df['Speedup'] = df.groupby('N')['Time'].transform(lambda x: x.iloc[0] / x)
print(df)
# Plot speedup curves
N_values = df['N'].unique()
for N in N_values:
subset = df[df['N'] == N]
plt.plot(subset['P'], subset['Speedup'], label=f'N={N}')
plt.xlabel('Number of Processes (P)')
plt.ylabel('Speedup')
plt.legend(title='N')
plt.title('Speedup vs. Number of Processes')
plt.grid(True)
plt.show()
```
