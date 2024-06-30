# CS6502 Assignment 2
# Conor Giles-Doran
# 121105743

import numpy as np
import random as rm

#### QUESTION 1 A ####

# Matrix multiplication function.
# Computes the result of multiplying two matrices M1 and M2.
def matrixMultiplication(M1,M2):

    # Initializing matrix of zeros for result.
    res = np.zeros([M1.shape[0],M2.shape[1]])

    # Multiply each row of M1 by each column of M, sum the result, and add to res matrix.
    for i in range(res.shape[1]):
        for j in range(res.shape[1]):
            res[i,j] = sum(M1[i,]*M2[:,j])
            
    return res

# Example:
m1 = np.array([[1,2,3],[1,2,3]])
m2 = np.array([[2,3],[2,3],[2,3]])
matrixMultiplication(m1,m2)

#### QUESTION 1 B ####

# powerOfMatrix function
# Computes the n-th power of a square matrix M.
def powerOfMatrix(M,n):

    # n must be >= 1
    if n < 1:
        raise TypeError('n must be >= 1')
        
    else:
        # Copy M to new variable P.
        P = M.copy()
        # While the n-th power is < 1.
        while n > 1:
            # P is the result of multiplying M and P together, P will update each time.
            P = matrixMultiplication(M, P)
            # Subtract 1 from n each time in order to complete the while loop.
            n -= 1
                        
    return P

# Example:
M = np.array([[1,2],[3,4]])
powerOfMatrix(M,2)


#### QUESTION 2 A ####

# random_transition_choice function
# Generates random transitions from a state i to a state j.
def random_transition_choice(i, transitions, transitionMatrix_size):

    choice = np.random.choice(range(transitionMatrix_size),
                              replace = True, p = transitionMatrix[i])
    
    return transitions[i][choice]
    where: transitionMatrix_size = len(transitionMatrix[0])


# markov_chain_path function
# Returns each state of a Markov chain encountered at each time point.
# Returns the final state of the Markov chain at the final time point.
# Returns the probability of the state path taken.
# NOTE: I was unsure whether the states_path variable was to return states as an intger or as a binary matrix, so I have
# included both in the output to be sure.
def markov_chain_path(transitionMatrix, time, initial_state):

    # First construct a list of lists containing all possible state transitions
    transitions = []
    for i in range(len(transitionMatrix)):
        # Empty list each time in order to have each list representing a row of the transition matrix.
        state_trans = []
        for j in range(len(transitionMatrix)):
            state_trans.append([i+1,j+1])
        # Append each list to the main 'transitions' list.
        transitions.append(state_trans)

    # Intitialize the probability value as 1
    prob = 1

    # Find the initial state as an integer valu (where the 1 is located in the binary initial_state matrix).
    # Add +1 in order to match up the correct indexes.
    initial = initial_state.index(1)+1

    # The Markov chain states at each time point will be represented in two formats:
    states_path = [initial]        # Integer values (1,2,3).
    binary_state = [initial_state] # Binary matrices ([1,0,0],[0,1,0],[0,0,1]).

    # At each time point, compute the random_transition_choice, the binary and integer sate formats and the probability.
    for i in range(time):

        # Matrix of zeros initialized at each time point in order to create the binary state format later.
        state = np.zeros([1,3])

        # Random transition choice, with i of this function being the last state that was encountered (-1 for indexing).
        choice = random_transition_choice(states_path[-1]-1, transitions, len(transitionMatrix[0]))

        # Append the state 'j' from random_transition_choice output to the integer states_path list.
        states_path.append(choice[-1])
        state[0, states_path[-1]-1] = 1
        binary_state.append(state)

        # Calculate the probability of this state path:
        # Locate the correct index of the random transition choice output within the transitions list.
        prob_index = transitions[choice[0]-1].index(choice)
        # Use this index to find the correct probability value associated with this transition choice.
        # Multiply each probabiltiy value along this path.
        prob *= transitionMatrix[choice[0]-1][prob_index]

    # Print the final output
    print('States taken at each time:', '\nInteger:', states_path, '\nBinary:', binary_state)
    print("Final state at time " + str(time) + ':', states_path[-1])
    print('Probability of the state path taken:', prob)


# Example:
transitionMatrix = [[0, 1, 0], [0.5, 0, 0.5], [1, 0, 0]]
markov_chain_path(transitionMatrix, time=10, initial_state= [1,0,0])


#### QUESTION 2 B ####

# markov_chain_convergence_test
# Computes the n-th power of the transitionMatrix
# Multiplies this result by the initialDistribution matrix in order to  evaluate the convergence.
def markov_chain_convergence_test(transitionMatrix, time, initialDistribution):

    # use powerOfMatrix function from before
    power = powerOfMatrix(transitionMatrix, time)

    # cannot use matrix multiplication function from before (different dimensions)
    # compute the sum of multiplying the entire row of initialDistribution by each column of power matrix
    # store output in result matrix
    result = np.zeros([initialDistribution.shape[0],power.shape[1]])
    for j in range(result.shape[1]):
        result[0,j] = sum(initialDistribution[0,]*power[:,j])

    return result

initialDistribution = np.array([[1, 0, 0]])
transitionMatrix = np.array([[0, 1, 0], [0.5, 0, 0.5], [1, 0, 0]])

for time in [1,10,50,100]:
    result = markov_chain_convergence_test(transitionMatrix, time, initialDistribution)
    print('Convergence at time =', time, ':', result)
    print()

# At time = 100, it converges to probability of [0.4, 0.4, 0.2]

#### QUESTION 3 ####

# random_walk functions
# Takes a positive integer n (number of steps to take) and returns co-ordinates of a 2D dimensional grid after moving
# in a random direction (North, East, South or West) at each step.

# random_walk(n) function returns just the final co-ordinates.
def random_walk(n):

    direction = ['N', 'E', 'S', 'W']
    x = 0
    y = 0
    for i in range(1,n+1):

        # make random step choice
        step = rm.choice(direction)

        # update co-ordinates accordingly
        if step == 'N':
            y += 1
        
        if step == 'E':
            x += 1
        
        if step == 'S':
            y -= 1
        
        if step == 'W':
            x -= 1
        print([x,y])
    # final co-ordinates achieved when the loop completes
    final_co_ord = [x,y]

    return final_co_ord

# Example:
random_walk(10)

# random_walk_route(n) returns the entire route taken and a plot of the random walk (matplotlib used).
import matplotlib.pyplot as plt

def random_walk_route(n):

    direction = ['N', 'E', 'S', 'W']

    # keep track of route using dictionary
    walk = {0: [0,0]}  
    x_val = [0]
    y_val = [0]
    x = 0
    y = 0
    # perform loop as before
    for i in range(1,n+1):

        step = rm.choice(direction)
    
        if step == 'N':
            y += 1
        
        if step == 'E':
            x += 1
        
        if step == 'S':
            y -= 1
        
        if step == 'W':
            x -= 1

        # add co-ord and chosen direction to dictionary
        walk[i] = [x,y], step
        # append all x and y values to asscoiated lists (easy for plotting below)
        x_val.append(x)
        y_val.append(y)

    # plot the route, with a start point (green) and end point (red)
    plt.plot(x_val,y_val)
    plt.scatter(0,0, color = 'green')
    plt.scatter(x_val[len(x_val)-1], y_val[len(y_val)-1], color = 'red')
    
    return walk

# Example:
# random_walk_route(10)






