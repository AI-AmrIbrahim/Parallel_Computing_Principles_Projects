from mpi4py import MPI
import numpy as np
import sys

def distribute_particles(rank, size, N):
    # Calculate the number of particles for each process
    particles_per_process = N // size
    remainder_particles = N % size

    # Calculate the start and end indices for each process
    start_index = rank * particles_per_process + min(rank, remainder_particles)
    end_index = start_index + particles_per_process + (rank < remainder_particles)

    return start_index, end_index

def generate_initial_coordinates(box_side):
    grid_points = box_side + 1
    
    # Generate grid points for each dimension
    x, y, z = np.meshgrid(np.linspace(0, box_side, grid_points),
                          np.linspace(0, box_side, grid_points),
                          np.linspace(0, box_side, grid_points),
                          indexing='ij')
    
    # Flatten the grid points
    coordinates = np.column_stack((x.flatten(), y.flatten(), z.flatten()))
    return coordinates

def compute_local_energy(start_index, end_index, coordinates):
    N = len(coordinates)
    local_energy = 0.0

    for i in range(start_index, end_index):
        for j in range(N):
            if i!=j:
                r_ij = np.linalg.norm(coordinates[i] - coordinates[j])
                local_energy += 0.5 * (1 / (r_ij**12 + 1e-6) - 2 / (r_ij**6 + 1e-6))

    return local_energy

def move_local_particles(start_index, end_index, coordinates, move_size, box_side, fraction):
    moved_coordinates = coordinates.copy()
    num_particles_to_move = int((end_index - start_index) * fraction)
    particles_to_move = np.random.choice(np.arange(start_index, end_index), size=num_particles_to_move, replace=False)
    moved_coordinates[particles_to_move, :] += np.random.uniform(-move_size, move_size, size=(num_particles_to_move, 3))
    
    # Bounce particles back if they go outside the box
    for i in range(3):  # For each dimension
        # If the coordinate is less than 0, make it positive
        moved_coordinates[particles_to_move, i] = np.where(moved_coordinates[particles_to_move, i] < 0, -moved_coordinates[particles_to_move, i], moved_coordinates[particles_to_move, i])
        # If the coordinate is greater than box_side, reflect it back
        moved_coordinates[particles_to_move, i] = np.where(moved_coordinates[particles_to_move, i] > box_side, 2*box_side - moved_coordinates[particles_to_move, i], moved_coordinates[particles_to_move, i])
    
    return moved_coordinates


def metropolis_criterion(delta_energy, temperature=1.0):
    return delta_energy < 0 or np.random.rand() < np.exp(-delta_energy / temperature)

def reduce_energy(comm, rank, start_index, end_index, initial_local_energy, initial_coordinates,
                  move_size, box_side, max_iterations, fraction):
    current_coordinates = initial_coordinates.copy()
    current_local_energy = initial_local_energy.copy()
    last_printed_energy = initial_local_energy.copy()
    min_energy = initial_local_energy.copy()  # Variable to store the minimum energy
    min_coordinates = current_coordinates.copy()  # Variable to store the coordinates associated with the minimum energy

    iteration = 0
    while iteration < max_iterations:
        local_coordinates = move_local_particles(start_index, end_index, current_coordinates, move_size, box_side, fraction)
        local_energy = compute_local_energy(start_index, end_index, local_coordinates)

        if metropolis_criterion(local_energy - current_local_energy):
            current_coordinates = local_coordinates
            current_local_energy = local_energy

        sub_local_coordinates = local_coordinates[start_index:end_index]
        all_coordinates = comm.allgather(sub_local_coordinates)
        current_coordinates = np.concatenate(all_coordinates)

        current_energy = comm.reduce(current_local_energy, op=MPI.SUM, root=0)
        if rank == 0:
            if current_energy < last_printed_energy:
                print("Iteration {}: Energy = {}".format((iteration + 1), current_energy))
                last_printed_energy = current_energy

            # Update the minimum energy and associated coordinates if the current energy is lower
            if current_energy < min_energy:
                min_energy = current_energy
                min_coordinates = current_coordinates.copy()

        iteration += 1

    if rank == 0:
        print("Minimum Energy = {}".format(min_energy))  # Print the minimum energy found during all iterations

    return min_coordinates, min_energy  # Return the coordinates associated with the minimum energy and the minimum energy


def main(P):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    N = 11 * 11 * 11
    box_side = 10
    move_size = 0.01
    max_iterations = 100

    if rank == 0:
        print('P = {}'.format(P))
    comm.Barrier()

    fractions_to_try = [0.1, 0.5, 0.9]

    for fraction in fractions_to_try:
        if rank == 0:
            print('Fraction = {}'.format(fraction))
        comm.Barrier()
        t1 = MPI.Wtime()
        start_index, end_index = distribute_particles(rank, size, N)

        initial_coordinates = generate_initial_coordinates(box_side)
        comm.Barrier()

        initial_local_energy = compute_local_energy(start_index, end_index, initial_coordinates)

        initial_energy = comm.reduce(initial_local_energy, op=MPI.SUM, root=0)
        if rank == 0:
            print('Initial Energy: {}'.format(initial_energy))

        final_coordinates, final_local_energy = reduce_energy(comm, rank, start_index, end_index, initial_local_energy,
                                                              initial_coordinates, move_size, box_side, max_iterations, fraction)

        #final_energy = comm.reduce(final_local_energy, op=MPI.SUM, root=0)

        t2 = MPI.Wtime()
        min_t1 = comm.reduce(t1, op=MPI.MIN, root=0)
        max_t2 = comm.reduce(t2, op=MPI.MAX, root=0)
        if rank == 0:
            time_elapsed = max_t2 - min_t1
            #print('Final Energy: {}'.format(final_energy))
            print('Time elapsed: {}\n'.format(time_elapsed))

if __name__ == "__main__":
    P = int(sys.argv[1])
    main(P)
