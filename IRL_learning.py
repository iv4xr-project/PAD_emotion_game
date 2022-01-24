from ast import Pass
import numpy as np
import time
import Maxent_irl as MaxEnt

MAXLIFE = 100
MIN_DIST = 20
MAX_DIST = 300

class MDP:
    
    def __init__(self):
        #feature propreties
        self.features = ['distance_to_closest_coin', 'distance_to_closest_enemy', 'distance_to_closest_cake', 'distance_to_objective', 'health', 'exploration']
        self.feature_limits = self.load_feature_limits()
        # number of states per one feature
        self.one_feature = 4
        #actions
        self.actions = ['go_to_closest_coin', 'fight_closest' , 'go_to_closest_cake', 'go_to_flower', 'explore']
        self.n_actions = len(self.actions)
        #states
        self.n_states = (self.one_feature ** (len(self.features) - 1) )* 2
        #gamma discount factor
        self.discount_factor = 0.9
        
    def get_probability_matrix(self):
        prob_matrix = np.zeros((self.n_actions, self.n_states, self.n_states))
        for action in range(self.n_actions):
            for current_state in range(self.n_states):
                current_features = self.get_features_of_state(current_state)
                if current_features[-2] == 0 or current_features[-1] == 0:
                    #if the goal was achived or is dead
                    prob_matrix[action][current_state][current_state] = 1
                elif action == 4:
                    #explore action exploration = 1
                    next_state_features = current_features
                    next_state_features[-1] = 1
                    prob_matrix[action][current_state][current_state] = 1
                else:
                    #reduce distance
                    #get features of the next state
                    next_state_features = current_features
                    next_state_features[action] -= 1
                    if action == 2:
                        if next_state_features[action] == 0:
                            #if collected cake increase life
                            possible_health_values = self.get_feature_possible_values(self.n_actions-1,current_features[-1])
                            for value in possible_health_values:
                                new_health_feature = self.get_feature_value(self.n_actions-1, ( value + 10)) 
                                next_state_features[-1] = new_health_feature
                                next_state = self.get_state_id(next_state_features)
                                prob_matrix[action][current_state][next_state] += 1/len(possible_health_values)
                        else:
                            next_state = self.get_state_id(next_state_features)
                            prob_matrix[action][current_state][next_state] = 1
                    else:  
                        next_state = self.get_state_id(next_state_features)
                        prob_matrix[action][current_state][next_state] = 1
        return prob_matrix

    def get_state_id(self, feature_vector):
        #feature vector [0-onefeture,...,0-1]
        state_id = feature_vector[0]
        
        for i in range(1, len(feature_vector)):
            state_id += (self.one_feature ** i) * feature_vector[i]
        
        return int(state_id)

    def get_features_of_state(self, state_id):
        feature = np.zeros((len(self.features),))
        remaining = state_id
        #reverse order of ids
        for i in reversed(range(len(self.features))):
            #check if id is bigger than one_feature powered to id
            if remaining > self.one_feature ** i:
                # divide id by one_feature**i to get int value correponded to feature i
                value = int(remaining / (self.one_feature ** i))
                feature[i] = value
                #subtract what remains of id by one_feature**i
                remaining -= (self.one_feature ** i) * value
            
        return(feature)

    def get_feature_value(self, feature_id, feature_value):
        #get feature limits
        low_limit = self.feature_limits[feature_id][0]
        high_limit = self.feature_limits[feature_id][1]
        #get distance between feature values
        feature_distance = (high_limit - low_limit) / self.one_feature 
        #convert [low, hight] to [0, hight-low]
        value = (feature_value - low_limit)
        #get value of feature between 0 and one_feature
        value = int( value / feature_distance)
        #if value is equal to one_feature return one_feature
        #so feature array is lenght one_feature
        return value if value != self.one_feature else (self.one_feature-1)
    

    def feature_matrix(self):
        f_matrix = np.zeros((self.n_states, len(self.features)))
        for state in range(self.n_states):
            #f_matrix[state] = (np.array(self.get_features_of_state(state)) + 1) / self.one_feature
            f_matrix[state] = np.array(self.get_features_of_state(state))
        
        return f_matrix

    def load_feature_limits(self):
        #feature limit list
        # limit: [low limit, hight limit]
        feature_limits = []
        
        for f in range(len(self.features) - 1):
            #first features are distance based 
            feature_limits.append([MIN_DIST,MAX_DIST])
        #last feature is based on life limits
        feature_limits.append([0,MAXLIFE])
        feature_limits.append([0,1])
        
        return feature_limits

    def get_feature_possible_values(self, feature_id, feature_value):
        low_limit = self.feature_limits[feature_id][0]
        high_limit = self.feature_limits[feature_id][1]
        #convert limits to array that stars with 0
        feature_distance = (high_limit - low_limit) / self.one_feature 
        #get limit of possible values
        limit = [int(feature_value * feature_distance), int((feature_value + 1) * feature_distance)]
        possible_values = []
        #if is the first feature
        if feature_value == 0:
            for v in range(limit[0], (limit[1]+1)):
                possible_values.append(v)
        else:
            for v in range(limit[0]+1, (limit[1]+1)):
                possible_values.append(v)
        
        return possible_values
        
def perfrom_irl(mdp, trajectories, training_epochs, learning_rate):
    weights = MaxEnt.irl(mdp.feature_matrix(), mdp.n_actions, mdp.discount_factor, mdp.get_probability_matrix(), trajectories, training_epochs, learning_rate)
    return weights

def perceptor_line_to_value_array(mdp, line):
    values = line.split('_')
    values_list = [values[2], values[0], values[1], values[-5], values[-4], 0]
    feature_values = [0 for x in range(len(mdp.features))]

    for value in range(len(values_list)):
        if values_list[value] == 'inf':
            values_list[value] = mdp.feature_limits[value][1]
            
        if isinstance(values_list[value],str):
            values_list[value] = int(float(values_list[value]))

        if values_list[value] > MAX_DIST:
            values_list[value] = MAX_DIST
        feature_values[value] = mdp.get_feature_value(value, values_list[value])

    return values_list,feature_values


def load_trajectory(mdp, file):
    #read file
    file = open(file, "r")
    lines = file.readlines()
    #final trajectory
    trajectory = []
    #is exploring
    exploring = False

    for l in range(len(lines)-1):
        #action id
        action_id = 0
        #current state
        current_values,current_feature_values = perceptor_line_to_value_array(mdp, lines[l])
        if exploring:
            current_feature_values[-1] = 1
        #next state
        next_values,_ = perceptor_line_to_value_array(mdp, lines[l+1])

        value_distances=[]
        diferent_v = 0
        exploring = False

        for v in range(4):
            if current_values[v] - next_values[v] <= 0:
                diferent_v += 1
            else:
                value_distances.append((v,current_values[v] - next_values[v])) 

        if diferent_v == 4 or diferent_v > 2:
            action_id = 4
        else:
            if value_distances[0][1] > value_distances[1][1]:
                action_id = value_distances[0][0]
            else:
                action_id = value_distances[1][0]
            
        if action_id == 4:
            exploring = True

        #state ids
        current_state_id = mdp.get_state_id(current_feature_values)

        #generate state-action pair
        trajectory.append((current_state_id, action_id))
        
    return trajectory
    

if __name__=="__main__":
    start_time = time.time()
    training_epochs = 1
    training_rate = 0.01
    m = MDP()
    
    t = [load_trajectory(m, 'Traces_Perceptor_Level1_02-05-2021_20-19-05_703.txt')]
    trajectory = np.array(t)
    w = perfrom_irl(m,trajectory, training_epochs, training_rate)
    print(w)
   
    print("--- %s seconds ---" % (time.time() - start_time))