# Assignment
MPI provides a large collection of collective operation functions such as broadcast, gather,
scatter, all-gather, etc. Describe the algorithms of implementation five functions: MPI_Bcast(),
MPI_Scatter(), and MPI_Allgather(), MP_Alltoall() and MPI_Reduce().

Implement MPI_Bcast() on your supercomputer using MPI_Isend() and MPI_Irecv() and a few
other supporting (non-data moving) MPI functions. Study the performance of your
MY_Bcast() vs. MPI_Bcast() provided by MPI by varying the broadcasted data sizes, measured
in the number of floating-point numbers. For example, if your data size 𝑁 = 2!", 2!#, 2!$ and
𝑃 = 4, 7, 28, 37 processing cores, measure the time needed for each of the 4x4 cases, i.e.,
create a table to store your timing results.
# Mini-report
## Problem Description
MPI has a large collection of operation function one of which is MPI_Bcast(). What
Bcast does is transmit send a message from a single processor to all processors. The objective of
this project is to create my own MY_Bcast() function that utilized MPI_Isend() and MPI_Irecv()
and compare the performance with MPI_Bcast(). This performance assessment will be based on
the time taken for broadcasting, and it will consider two key metrics: the size of the data being
broadcasted (N) and the number of participating processes (P).
## Program
I used python as my programing language using mpi4py. Using MPI_Isend() and
MPI_Irecv the root node send the data to all other processors. Time span of MY_Broadcast() is
computed in the main function where start time t1 is taken right before running MY_Broadcast()
line and end time t2 is taken right after it. T2 would not be accurate since I am using Isend and
Irecv therefore I added a while loop that terminates once the processor confirms receiving the
data. The pseudocode for MY_Bcast() is as follows:
```
MY_Bcast(data,rank,root=0)
If rank == root do
  for i = 0 to size do
    Isend the data to all processors except root
else do
  Irecv the data
  confirm that the data was received
return data
```
To compare the performance of the two broadcast functions, I calculate the execution
time in the main function. I measure t1 before initiating the broadcast function and t2 after
completion. The time span is then determined as t2 - t1. To ensure a fair comparison, I employ
MPI.MAX reduction for both broadcast functions.

Additionally, the Slurm script is designed to iterate through the number of processors. As
a result, when running the Python script, two loops are executed: one for the processors specified
in the Slurm file and another for the data size within the Python file. This allows for a
comprehensive evaluation of performance.
## Results
I extracted data from the output file, which was in the format "N = %d, P = %d,
MY_Bcast() time = %f, Bcast() time = %f." Using these values, I generated Table 1, which
includes not only the extracted values but also the absolute difference and percentage difference
calculated as (MY_Bcast - MPI_Bcast) / (MPI_Bcast) * 100.
|  P 	| N 	 | MPI_Bcast() Time 	| MY_Bcast() Time 	| Abs. Diff 	| Perc. Diff 	|
|:--:	|:-:	 |:----------------:	|:---------------:	|:---------:	|:----------:	|
|  4 	| 2^10 |     0.000087     	|     0.00005     	|  0.000037 	|   -42.53   	|
|  4 	| 2^12 |     0.000095     	|     0.000067    	|  0.000028 	|   -29.47   	|
|  4 	| 2^14 |     0.001777     	|     0.000045    	|  0.001732 	|   -97.47   	|
|  4 	| 2^20 |     0.006565     	|     0.002913    	|  0.003652 	|   -55.63   	|
|  7 	| 2^10 |     0.000088     	|     0.000074    	|  0.000014 	|   -15.91   	|
|  7 	| 2^12 |     0.000117     	|     0.00013     	|  0.000013 	|    11.11   	|
|  7 	| 2^14 |     0.001238     	|     0.000072    	|  0.001166 	|   -94.18   	|
|  7 	| 2^20 |     0.008826     	|     0.003766    	|  0.00506  	|   -57.33   	|
| 28 	| 2^10 |     0.000179     	|     0.000272    	|  0.000093 	|    51.96   	|
| 28 	| 2^12 |     0.000194     	|     0.000615    	|  0.000421 	|   217.01   	|
| 28 	| 2^14 |     0.000431     	|     0.000875    	|  0.000444 	|   103.02   	|
| 28 	| 2^20 |     0.007073     	|     0.017273    	|   0.0102  	|   144.21   	|
| 37 	| 2^10 |      0.00023     	|     0.001062    	|  0.000832 	|   361.74   	|
| 37 	| 2^12 |     0.000261     	|     0.000768    	|  0.000507 	|   194.25   	|
| 37 	| 2^14 |     0.000435     	|     0.001099    	|  0.000664 	|   152.64   	|
| 37 	| 2^20 |     0.007638     	|     0.023975    	|  0.016337 	|   213.89   	|

Table 1. MPI_Bcast() VS MY_Bcast() across different P and N values. Green shading indicates
faster/shorter time span
## Analysis
Here we compared the time efficiency of MPI_Bcast() and my own MY_Bcast()
functions across different number of processors and data sizes. As shown in Table 1
MPI_Bcast() is more optimized for larger number of processors which explains why MY_Bcast()
performs better at smaller number of processors. A surprising result is that MPI_Bcast() did
better than MY_Bcast() for P = 7 and N = 2^12. However, since the difference is very small I do
not consider it a significant outlier without further analysis of both the algorithm and the node
utilized.


