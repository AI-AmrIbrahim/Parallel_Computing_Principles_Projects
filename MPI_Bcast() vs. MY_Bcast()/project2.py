from mpi4py import MPI
import numpy as np
import sys

def MY_Bcast(data,rank,size,root=0):
    comm = MPI.COMM_WORLD
    if rank == root:
        for i in range(size): # root sends data to all processors
            if i != root:
                req = comm.Isend(data, dest=i) 
    else:
        req = comm.Irecv(data, source=root)
        while not req.Test(): # a while loop which breaks after the message have been received
            pass
    return data

def main(P):
    N_values = [2**10, 2**12, 2**14, 2**20]
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    for N in N_values:
        if rank == 0:
            data = np.random.rand(N)
        else:
            data = np.empty(N)
        
        comm.Barrier()  # Ensure all processes start at the same time
        bcast_t1 = MPI.Wtime()
        comm.Bcast(data,root=0)
        bcast_t2 = MPI.Wtime()
        bcast_time = bcast_t2 - bcast_t1
        comm.Barrier()
        max_bcast_time = comm.reduce(bcast_time, op=MPI.MAX, root=0) # get max time taken among bcasts
        
        t1=t2=0 # initialize t1 and t2 for MY_Bcast()
        comm.Barrier()  # Ensure all processes start at the same time
        t1 = MPI.Wtime() # get t1 before MY_Bcast
        MY_Bcast(data,rank,size, root=0)
        t2 = MPI.Wtime() # get t2 after MY_Bcast 
        comm.Barrier()
        min_my_bcast_t1 = comm.reduce(t1, op=MPI.MIN, root=0) # get minimum t1
        max_my_bcast_t2 = comm.reduce(t2, op=MPI.MAX, root=0) # get maximum t2
        

        # The root prints the results
        if rank == 0:
            my_bcast_time = max_my_bcast_t2 - min_my_bcast_t1
            print('N = %d, P = %d, MY_Bcast() time = %f, Bcast() time = %f' %(N, P, my_bcast_time, max_bcast_time))

if __name__ == "__main__":
    P = int(sys.argv[1])
    main(P)
