from mpi4py import MPI
import os
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from sklearn.linear_model import LogisticRegression

def read_file(filename):
    data = pd.read_csv(filename)
    y = data['y']
    x = data.drop('y', axis=1)
    x.insert(0,'x0',1) # this should add x0 intercept at the 1st column of x
    return y, x

def read_files_in_directory(rank, size, directory):
    all_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".csv")]

    files_per_process = len(all_files) // size
    remainder = len(all_files) % size

    start_index = rank * files_per_process + min(rank, remainder)
    end_index = start_index + files_per_process + (1 if rank < remainder else 0)
    process_files = all_files[start_index:end_index]
    x_list = []
    y_list = []
    for file in process_files:
        y_local, x_local = read_file(file)
        x_list.append(x_local)
        y_list.append(y_local)
    # Concatenate x and y along rows
    x_combined = pd.concat(x_list, axis=0, ignore_index=True)
    y_combined = pd.concat(y_list, axis=0, ignore_index=True)
    return y_combined, x_combined.values

def initialize_coefficients(X, y):
    # Use LogisticRegression from scikit-learn to get initial coefficients
    clf = LogisticRegression(penalty='l2', C=1e10, solver='lbfgs', max_iter=100)
    clf.fit(X, y)
    B_initial = clf.coef_[0]
    return B_initial

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

def local_regression(y_local, X_local, B_local, u_local, rho, B_bar):
    m, n = X_local.shape

    def objective(B):
        # Logistic Regression Loss Term
        z = np.dot(X_local, B)
        h = sigmoid(z)
        loss = -np.sum(y_local * np.log(h) + (1 - y_local) * np.log(1 - h)) / m

        # Penalty Term
        penalty = rho / 2.0 * np.linalg.norm(B - B_bar + u_local, ord=2)**2

        return loss + penalty

    # Update B_local using the combined objective
    B_local = minimize(objective, B_local, method='BFGS').x

    return B_local

def consensus_update(comm, B_local, u_local, size):
    # Gather local coefficients B_local from all processes to rank 0
    all_B_locals = comm.gather(B_local, root=0)

    # Compute the average B_bar at rank 0
    if comm.rank == 0:
        B_bar = np.mean(all_B_locals, axis=0)
    else:
        B_bar = None

    # Broadcast B_bar to all processes
    B_bar = comm.bcast(B_bar, root=0)

    # Update Lagrange multipliers u_local in each process
    u_local += B_local - B_bar

    return u_local, B_bar

def main():
    # MPI Initialization
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    data_directory = "/gpfs/projects/AMS598/projects2023/project3/"
    y_local, x_local = read_files_in_directory(rank, size, data_directory)
    
    # Use LogisticRegression from scikit-learn to get initial coefficients
    B_local = initialize_coefficients(x_local, y_local)
    u_local = np.zeros(x_local.shape[1])  # Initialize penalty locally
    
    # Consensus update
    u_local, B_bar = consensus_update(comm, B_local, u_local, size)
    
    rho = 1
    num_iterations = 100  # Adjust as needed
    epsilon = 1e-3  # Adjust as needed
    
    for iteration in range(num_iterations):
        B_local = local_regression(y_local, x_local, B_local, u_local, rho, B_bar)

        # Consensus update
        u_local, B_bar = consensus_update(comm, B_local, u_local, size)

        #if rank == 0:
        #    print("Rank {}: Completed iteration {}".format(rank, iteration +1))

        # Check convergence 
        status = 0
        diff_norm = np.linalg.norm(B_local - B_bar, ord=2)
        if diff_norm < epsilon:
            status = 1
        statuses = comm.gather(status, root=0)

        # Rank 0 checks if all processes have converged
        termination_signal = None  # Initialize the variable for all processes
        if rank == 0:
            statuses_count = np.sum(statuses)
            if statuses_count == size:
                print("Converged after {} iterations.".format(iteration + 1))
                termination_signal = "terminate"

        # Broadcast termination signal to all processes
        termination_signal = comm.bcast(termination_signal, root=0)

        # Introduce a barrier to avoid deadlock
        comm.Barrier()

        # Check if termination signal received
        if termination_signal == "terminate":
            if rank == 0:
                print("Rank 0 Converged coefficients:")
                print("{:<15} {:<15}".format("Coefficient", "Value"))
                print("-" * 30)

                # Print the coefficients
                for i, coeff in enumerate(B_local):
                    print("{:<15} {:<15}".format("B_" + str(i), coeff))

                print("-" * 30)
            comm.Barrier()
            print('Rank {}: B_local \n{}'.format(rank, B_local))
            break  # This breaks out of the loop for all processes

if __name__ == '__main__':
    main()
