from mpi4py import MPI
import os

# Mapper Function
def mapper(rank, size):
    for i in range(rank, 16, size): # this ensures that regardless of size the files would be split among processes
        filename = '/gpfs/projects/AMS598/projects2023/project1/data{}.txt'.format(i + 1)
        with open(filename, 'r') as f:
            data_str = f.read()
        data = [int(line) for line in data_str.split('\n') if line] # Split the string into lines and to an integer
        output_filename = '/gpfs/projects/AMS598/class2023/amibrahim/project1/mapper_output{}.txt'.format(i + 1)
        with open(output_filename, 'w') as f:
            for number in data:
                f.write('{},1\n'.format(number)) # create key,value pairs number,1 and write into output files

# Reducer Function
def reducer(rank, size):
    counts = {} # initialize counts - dictionary including counts of each individual key/number
    reduced_counts = {} # initialize reduced_counts - counts of after gathering all counts dictionaries
    for i in range(rank, 16, size):
        input_filename = '/gpfs/projects/AMS598/class2023/amibrahim/project1/mapper_output{}.txt'.format(i + 1)
        with open(input_filename, 'r') as f:
            for line in f:
                number, count = map(int, line.strip().split(',')) # extract number and count
                if number in counts: # if number is already in the dictionary count += count if not = count
                    counts[number] += count
                else:
                    counts[number] = count
                    
    all_counts = comm.gather(counts, root=0) # Root 0 gets all counts dictionaries from all processes
    if rank == 0:
        for counts in all_counts:
            for number, count in counts.items(): # if number is already in the dictionary count += count if not = count
                if number in reduced_counts:
                    reduced_counts[number] += count
                else:
                    reduced_counts[number] = count
    return reduced_counts

if __name__ == '__main__': # I learned that this function runs everything within if the script is run
    comm = MPI.COMM_WORLD
    str_time = MPI.Wtime()
    rank = comm.Get_rank()
    size = comm.Get_size()

    mapper(rank, size) # call mapper function

    comm.Barrier()

    final_counts = reducer(rank, size) # call reducer function

    if rank == 0: # Root 0 would print out the top 6 integers
        sorted_counts = sorted(final_counts.items(), key=lambda item: item[1], reverse=True) # sort dictionary
        top_6 = sorted_counts[:6] # get top 6
        for number, count in top_6: # print number and their respective count in the top 6
            print("Number: %d, Count: %d" %(number,count))
    	end_time = MPI.Wtime()
    	print("\nElapsed time: %f seconds" %(end_time-str_time))
