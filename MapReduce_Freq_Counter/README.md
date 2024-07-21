# Assignment
Counting	with	Map/Reduce:
Under	[Data](data),	there	are	 16	 data	files,	
each	containing	about	1.5	millions	integers	ranging	from	0-100.	
Use	the	Map/Reduce	concept	and	SeaWulf	to	count	the	frequencies	of	those	integers	
and	report	 6	 integers	with	the	highest	frequencies	and	their	corresponding	
frequencies.

Requirements:

1. Only	one	script	file	and	one	slurm	file	are	allowed.	
2. There	should	be	a mapper() function	and	a reducer() function
3. After	mapper	is	done,	results should	be	saved	to	hard	disk.	
4. Reducers	cannot	start	until	all	mappers	are	completed.
5. Use	4	processes	for	both	mappers	and	reducers
# Mini-report
## Algorithm
### Mapper
Mapper function takes in rank and size to assure that the function works regardless of
process sizes. When reading the data.txt files range(rank, 16, size) where rank is start, 16 is stop,
and size is the step so that no file is read more than once. Since range starts at 0 reading and
writing would be in (i+1) format. The mapper outputs 16 files with key,value pairs such that each
integer would have a 1 next to it comma separated i.e. 75,1. The 16 mapper output files are then
saved to my project directory.
### Reducer
Similar to the mapper, the reducer reads the mapper output files and separates the integer
and the value 1 into variables number and count. First I reduced each file separately using a
dictionary counts to hold the numbers and keys and count as value using a for loop where
whenever a number is encountered count += count if the number is already in the counts
dictionary if not create the number key and value.

Second I reduce all files, I gather all dictionaries to root 0 and utilize a new dictionary
reduced_counts where once again whenever a number is encountered count += count if the
number is already in the counts dictionary if not create the number key and value.
Reduced_counts is returned as output. So the reducer basically runs 2 reduction processes where
the 1st reduction is applied on a file level and the 2nd is applied on the full data from the 1st
reduction.
### Running
Running the script, it initiates the three fundamental MPI operations:
MPI.COMM_WORLD, Get_rank, and Get_size. It then records the start time using Wtime. The
mapper function is called next, followed by a barrier to ensure all mapping tasks are completed.
The reducer function is then ran, and its output is sorted to identify the top six integers along
with their respective frequencies. Finally, Wtime is used again to record the end time, to
calculate the elapsed time for process 0. The entire script is executed across four processes,
which are utilized for both the mapper and reducer functions.
## Results
Running the script 16 mapper output files were generated in my class project 1 directory
and the output.log had the top 6 integers along with their respective counts as follows:
```
Number: 23, Count: 773404
Number: 17, Count: 772993
Number: 88, Count: 772708
Number: 48, Count: 772168
Number: 71, Count: 771839
Number: 49, Count: 548302

Elapsed time: 15.337017 seconds
```
## Discussion
The program algorithm does complete the project task of computing the integer
frequencies and prints out the top 6 integers in an elapsed time of 15.34 seconds. Even though
the algorithm works regardless of the number of processes, however there is the question of
scalability since as the number of files and integers dramatically increase root 0 would have a lot
more work to do as a final reduction. With a lot more work to do and considerably more data
errors could pop up regarding memory or runtime.
