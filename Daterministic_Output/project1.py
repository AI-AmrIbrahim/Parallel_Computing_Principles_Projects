# Project 1
from mpi4py import MPI # import mpi using mpi4py

comm = MPI.COMM_WORLD # initialize MPI env
rank = comm.Get_rank() # get rank of processor
size = comm.Get_size() # get size of the group

if rank >  0:
        data = comm.recv(source = rank - 1) # if rank > 0 recv from rank - 1
print("Hello from Processor %d" % rank)
if rank < size - 1:
        comm.send(None,dest = rank + 1)  # send 'None' to rank + 1 if rank < max rank
