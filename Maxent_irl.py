from itertools import product

import numpy as np
import numpy.random as rn
import VI
import time

def irl(feature_matrix, n_actions, discount, transition_probability, trajectories, epochs, learning_rate):
        """
        Find the reward function for the given trajectories.

        feature_matrix: Matrix with the nth row representing the nth state. NumPy
                array with shape (N, D) where N is the number of states and D is the
                dimensionality of the state.
        n_actions: Number of actions A. int.
        discount: Discount factor of the MDP. float.
        transition_probability: NumPy array mapping (state_i, action, state_k) to
                the probability of transitioning from state_i to state_k under action.
                Shape (A, N, N).
        trajectories: 3D array of state/action pairs. States are ints, actions
                are ints. NumPy array with shape (T, L, 2) where T is the number of
                trajectories and L is the trajectory length.
        epochs: Number of gradient descent steps. int.
        learning_rate: Gradient descent learning rate. float.
        -> Reward vector with shape (N,).
        """

        n_states, d_states = feature_matrix.shape

        # Initialise weights.
        weights = rn.uniform(size=(d_states,))

        # Calculate the feature expectations \tilde{phi}.
        feature_expectations = find_feature_expectations(feature_matrix, trajectories)

        
        # Gradient descent.
        for i in range(epochs):
                r = feature_matrix.dot(weights)
                expected_svf = find_expected_svf(n_states, r, n_actions, discount, transition_probability, trajectories)
                grad = feature_expectations - feature_matrix.T.dot(expected_svf)

                weights += learning_rate * grad

        return weights

def find_svf(n_states, trajectories):
        """
        Find the state visitation frequency from trajectories.

        n_states: Number of states. int.
        trajectories: 3D array of state/action pairs. States are ints, actions
                are ints. NumPy array with shape (T, L, 2) where T is the number of
                trajectories and L is the trajectory length.
        -> State visitation frequencies vector with shape (N,).
        """

        svf = np.zeros(n_states)

        for trajectory in trajectories:
                for state, _ in trajectory:
                        svf[state] += 1

        svf /= trajectories.shape[0]

        return svf

def find_feature_expectations(feature_matrix, trajectories):
        """
        Find the feature expectations for the given trajectories. This is the
        average path feature vector.

        feature_matrix: Matrix with the nth row representing the nth state. NumPy
                array with shape (N, D) where N is the number of states and D is the
                dimensionality of the state.
        trajectories: 3D array of state/action pairs. States are ints, actions
                are ints. NumPy array with shape (T, L, 2) where T is the number of
                trajectories and L is the trajectory length.
        -> Feature expectations vector with shape (D,).
        """

        feature_expectations = np.zeros(feature_matrix.shape[1])

        for trajectory in trajectories:
                for state, _ in trajectory:
                        feature_expectations += feature_matrix[int(state)]

        feature_expectations /= trajectories.shape[0]

        return feature_expectations

def find_expected_svf(n_states, r, n_actions, discount, transition_probability, trajectories):
        #print("find_expected_svf")
        """
        Find the expected state visitation frequencies using algorithm 1 from
        Ziebart et al. 2008.

        n_states: Number of states N. int.
        r: Reward. NumPy array with shape (N,).
        n_actions: Number of actions A. int.
        discount: Discount factor of the MDP. float.
        transition_probability: NumPy array mapping (state_i, action, state_k) to
                the probability of transitioning from state_i to state_k under action.
                Shape (A, N, N).
        trajectories: 3D array of state/action pairs. States are ints, actions
                are ints. NumPy array with shape (T, L, 2) where T is the number of
                trajectories and L is the trajectory length.
        -> Expected state visitation frequencies vector with shape (N,).
        """

        n_trajectories = trajectories.shape[0]
        trajectory_length = trajectories.shape[1]

        policy = VI.find_policy(n_states, n_actions, transition_probability, r, discount)

        start_state_count = np.zeros(n_states)
        for trajectory in trajectories:
                start_state_count[int(trajectory[0][0])] += 1
        p_start_state = start_state_count/n_trajectories

        expected_svf = np.tile(p_start_state, (trajectory_length, 1)).T
        total = trajectory_length
        for t in range(1, trajectory_length):
                expected_svf[:, t] = 0
                for i, j, k in product(range(n_states), range(n_actions), range(n_states)):
                        
                        expected_svf[k, t] += (expected_svf[i, t-1] * policy[i, j] * transition_probability[j, i, k])
                       
        return expected_svf.sum(axis=1)

