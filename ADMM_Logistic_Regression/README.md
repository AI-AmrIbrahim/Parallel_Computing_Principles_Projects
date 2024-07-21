# To be continued
# Assignment
One large dataset has been partitioned into 10 files and are stored under the shared class space:
/gpfs/projects/AMS598/projects2023/project3. Each file contains one column called ‘y’, which is
a binary 0/1 response variable, and 25 other columns named x1 – x25, representing explanatory
variables.

Requirements:
1. Use the ADMM algorithm to run a logistic regression on all data, and obtain one set of
consensus estimates for all coefficients (intercept and explanatory variables).
2. Use mpi4py on SeaWulf for the computation.
3. You can use 10 processes in this project (one process per file), but your program should
be able to run with arbitrary number of files.
4. There should be no intermediate files.
# Mini-report
## Algorithm
### Read_file(filename)
This function reads in the data of a specific file and outputs y and x values. Reading is
done utilizing pandas’s read_csv and a column is added at index 0 for x to account for intercept.
### Read_files_in_directory(rank, size, directory)
This function makes sure that each process is reading its own respective number of files
and concatenating their respective xs and ys together. A for loop is used to iterate each process’s
list of files which calls read_file(filename) to extract x and y data.
### Initialize_coefficients(X, y)
To account for a faster convergence this function utilizes sklearn’s LogisticRegression to
get initial B coefficients.
### Sigmoid(z)
This function maps the linear combination of input x and coefficients to a probability. I
also clipped the z value so that it is within a valid range. $𝑠𝑖𝑔𝑚𝑜𝑖𝑑(𝑧) = \frac{1}{1 + 𝑒^{−𝑧}}$
### Local_regression(y_local, x_local, B_local, u_local, rho, B_bar)
This function computes loss and penalty terms and utilizes scipy.optimize’s minimize
function to minimize B. $𝐵_{𝑖}^{𝑘+1} = 𝑎𝑟𝑔𝑚𝑖𝑛_{𝐵_𝑖}(𝑙_{𝑖}(𝑦_{𝑖},𝑋_{𝑖}^{𝑇}𝐵_{𝑖}) + \frac{\rho}{2} ||𝐵_𝑖−\bar{𝐵^𝑘}+𝑢_{𝑖}^{𝑘}||_{2}^{2})$ 
where 𝑙𝑖(𝑦𝑖,𝑋𝑖𝑇𝐵𝑖)=−1𝑚∑ 𝑦𝑖log(𝑠𝑖𝑔𝑚𝑜𝑖𝑑(𝑧))+(^1 −𝑦𝑖)log(^1 −𝑠𝑖𝑔𝑚𝑜𝑖𝑑(𝑧))𝑚𝑖= 1 where m isnumber of rows or observations.
### Consensus_update(comm, B_local, u_local, size)
The consensus update function manages the communication and synchronization
between processes. It gathers the local coefficients, computes the average B_bar, broadcasts it to

all processes, and updates u_local. 𝑢𝑖𝑘+^1 =𝑢𝑖𝑘+(𝐵𝑖𝑘+^1 −𝐵𝑘+^1 )

### Main()
Finally main function orchestrates the overall execution of the logistic regression
algorithm using ADMM. It initializes necessary variables, performs ADMM iterations, checks
for convergence, and outputs the final consensus estimate.

## Results
Using rho = 1, the logistic regression takes 38 iterations to reach convergence with
consensus. After convergence, each process prints out its respective B_local. The values of
B_local across all processes demonstrate a high degree of consensus, with minimal differences
within the threshold of 1e-3. The B_local for Rank 0 is

Coefficient Value

B_0 0.
B_1 0.
B_2 0.
B_3 -0.
B_4 0.
B_5 -0.
B_6 -0.
B_7 0.
B_8 0.
B_9 0.
B_10 0.
B_11 0.
B_12 0.
B_13 0.
B_14 0.
B_15 -0.
B_16 -0.
B_17 -0.
B_18 -0.
B_19 0.
B_20 0.
B_21 0.
B_22 -0.
B_23 0.
B_24 0.
B_25 0.

## Discussion
ADMM logistic regression algorithm was implemented, and I was able to get a
converging B values after 3 8 iterations using a constant rho of 1. I tried using different rho
values larger than 1 and I got faster convergence and also different values for B. The difference
of values is probably due to the increased emphasis on the penalty term meaning more
regularization which in turn decreases the coefficients values. I ended up sticking with rho of 1
since I wanted more emphasis on the loss term as in preference for fitting the data. Further cross
validation would be required to assess optimal rho value. The convergence occurred with 1e- 3
threshold difference between B_local and B_bar.
From the Rank 0 B_local the top 5 coefficients are: 𝐵_0 = 0. 688 ,𝐵_{25} = 0. 249 ,𝐵_1 =
0. 224 ,𝐵_4 = 0. 220 ,𝐵_{11} = 0. 0112.
The main thing I have learned from this project was the usage of objective functions and
scipy.optimize.
