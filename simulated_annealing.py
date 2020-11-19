from math import exp, sqrt
from random import random, randint
import json 


def anneal_phase(X0, coords, transition, objective, N_steps, T):
    """
    Performs a single step of the annealing process at a single provided temperture
    It converts the input into a list since they have less overhead in single element operations
    
    Inputs:
        X0: the initial state as a list of indices
        coords: the coordinates of each index
        transition: an arbitrary function that can modify the state 
        objective: an arbitrary function that can return a score for the state
        N_steps: the number of random transitions to attempt
        T: the annealing temperature (higher T makes it more likely to accept unfavorable transitions)
        
    Returns:
        current: contains the current score and state as a tuple
        best: contains the best score and state as a tuple
    """
    X = [ x for x in X0 ]
    score = objective(X, coords)
    best = (score, X)
    for m in range(N_steps):
        new_X = transition(X, coords)
        new_score = objective(new_X, coords)
        delta = score - new_score
        if new_score < score:
            X, score = new_X, new_score
            if score < best[0]:
                best = (score, X)
        else:
            P = exp( delta/T )
            if random() < P:
                X, score = new_X, new_score
    current = (score, X)
    return current, best

def swap(X0, coords):
    """
    Swaps a random pair of nodes in the path
    
    Inputs: 
        X0: a list of indices defining the current path order
        coords: a list of coordinates defining the location of each index
        
    Returns:
        X: a list of indices defining a proposed new path order
    """
    X = [ x for x in X0 ]
    i = randint( 0, len(X)-1 )
    j = i
    while j == i:
        j = randint( 0, len(X)-1 )
    X[i], X[j] = X[j], X[i]
    return X

def reverse(X0, coords, max_fraction = 0.25):
    """
    Reverses a random section (with a random length) of the path
    
    Inputs: 
        X0: a list of indices defining the path order
        coords: a list of coordinates defining the location of each index
        max_fraction: the maximum fraction of the path that can be reversed 
        
    Returns:
        X: a list of indices defining a proposed new path order
    """
    X = [ x for x in X0 ]
    N_reverse = randint(2, len(X)*max_fraction )
    i = randint( 0, len(X)-N_reverse )
    j = i + N_reverse
    X[i:j] = X[j-1:i-1:-1]
    return X

def path_length(X, coords):
    """
    Calculates the total path length for a given route
    
    Inputs: 
        X: a list of indices defining the path order
        coords: a list of coordinates defining the location of each index
        
    Returns:
        total: the length of the path
    """
    coords = coords
    total = 0.
    for i, x in enumerate(X):
        if i == 0 :
            x0, y0 = coords[x]
        else:
            x1, y1 = coords[x]
            total += (x1-x0)**2 + (y1-y0)**2
            x0, y0 = x1, y1
    x1, y1 = coords[X[0]]
    total += (x1-x0)**2 + (y1-y0)**2
    return sqrt(total)


def simulated_annealing(X0, coords, transition, objective, T0, alpha, N_steps, N_phases):
    """
    Performs simulated annealing on the initial state based on the provided specifications
    
    Inputs:
        X0: the initial state as a list of indices
        coords: the coordinates of each index
        transition: an arbitrary function that can modify the state 
        objective: an arbitrary function that can return a score for the state
        T0: the initial annealing temperature (higher T makes it more likely to accept unfavorable transitions)
        alpha: the scaling factor used to reduce the temperature after each phase (should be <1)
        N_steps: the number of random transitions to attempt in each phase (i.e. for each temperature)
        N_phases: the number of phases to attempt overall (i.e. number of temperature reductions)
    
    Returns:
        best: a tuple containing the best score and path sequence across all runs
        scores: a list of the best scores at the end of each phase
    """
    X = [ x for x in X0 ]
    T = T0
    scores = []
    for n in range(N_phases):
        current, best = anneal_phase(X, coords, swap, objective, N_steps, T)
        T *= alpha
        scores.append( best[0] ) 
        X = best[1]
    return best, scores
