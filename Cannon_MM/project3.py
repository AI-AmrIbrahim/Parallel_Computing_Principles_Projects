from mpi4py import MPI
import numpy as np
import sys
import pandas as pd

def cannon(comm, rank, size, A, B):
    if size == 1:
        return np.dot(A, B)  # Apply multiplication on a single process
    elif not (size ** 0.5).is_integer():
        raise ValueError("Number of processes must be a perfect square")  # Raise an error
    else:
        grid_size = int(size ** 0.5)
        comm_cart = comm.Create_cart((grid_size, grid_size))
        my_coords = comm_cart.Get_coords(rank)

        N = A.shape[0]
        local_rows = N // grid_size
        local_cols = N // grid_size

        A_local = np.empty((local_rows, local_cols), dtype=np.float64)
        B_local = np.empty((local_rows, local_cols), dtype=np.float64)

        comm.Scatter(A, A_local, root=0)
        comm.Scatter(B, B_local, root=0)

        C_local = np.zeros((local_rows, local_cols), dtype=np.float64)

        for i in range(grid_size):
            A_local = np.roll(A_local, -my_coords[1] * local_cols, axis=1)
            B_local = np.roll(B_local, -my_coords[0] * local_rows, axis=0)
            C_local += np.dot(A_local, B_local)

        C = None
        if rank == 0:
            C = np.empty((N, N), dtype=np.float64)

        comm.Gather(C_local, C, root=0)

    return C

def main(P):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    N_values = [2**8, 2**10, 2**12]  # 2**14 didn't work so 2**12 it is
    res = []
    for N in N_values:
        A = np.empty((N, N))
        B = np.empty((N, N))

        if rank == 0:
            A = np.random.uniform(-1, 1, (N, N))
            B = np.random.uniform(-1, 1, (N, N))

        # Create non-blocking broadcasts
        A_req = comm.Ibcast(A, root=0)
        B_req = comm.Ibcast(B, root=0)

        # Wait for broadcasts to complete
        A_req.Wait()
        B_req.Wait()

        # Synchronize after broadcast (remove the barrier)

        t1 = MPI.Wtime()
        C = cannon(comm, rank, size, A, B)
        t2 = MPI.Wtime()
        min_t1 = comm.reduce(t1, op=MPI.MIN, root=0)  # get the minimum t1
        max_t2 = comm.reduce(t2, op=MPI.MAX, root=0)  # get the maximum t2

        if rank == 0:
            time_elapsed = max_t2 - min_t1
            print('N = %d, P = %d, Cannon time elapsed = %f' % (N, P, time_elapsed))

if __name__ == "__main__":
    P = int(sys.argv[1])
    main(P)
