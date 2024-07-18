# Assignment
When running a parallel program on P processors to write out “Hello from Processor X” to
you (who has one series way to receive the write out), the order is non-deterministic when
you run the same program on the same system, multiple times.

For example, when running on a system of 𝑃 = 10, you get the following print out:
```
Hello from Processor 3
Hello from Processor 9
Hello from Processor 8
…
Hello from Processor 0
```
Next time, repeating the same program again on the same computer, you get
```
Hello from Processor 0
Hello from Processor 8
Hello from Processor 7
…
Hello from Processor 4
```
This non-deterministic feature is sometimes undesirable and, too, rectifiable. Write a parallel
program to rectify, i.e., whenever running your program, you always get the system to write
out in a desired/fixed order, e.g.,
```
Hello from Processor 0
Hello from Processor 1
Hello from Processor 2
…
Hello from Processor 9
```
You may test it for a system with at least 13 processors.
One example of revealing many differences of parallel programs from the sequential ones.
# Mini-report

## Problem Description
When running a parallel program on P processors to output “Hello from Processor X” the
order is stochastic as in the order of series of Hello is random with every run. The aim of this
problem is get a deterministic output that in a desired output.
## Program
I used python as my programing language using mpi4py. The logic that I programmed
utilizes send and recv MPI functions where any process with rank > 0 has to wait to receive an
empty message from rank – 1 process before sending their “hello” printout as shown in [project1.py](project1.py).

## Results
As shown in [project1.out](project1.out), all “hello” printouts of the 20 processors are ordered. The stochastic
element of the 1st come 1st print has been eliminated due to send recv function pair.
Fig 3. Project1.out deterministic output of Project1.py

## Analysis
This program demonstrates how to overcome the stochastic nature of parallel computing
by deterministically controlling the order which processors execute. By having each processor
wait to receive data from another processor before printing out its rank and sending data to the
