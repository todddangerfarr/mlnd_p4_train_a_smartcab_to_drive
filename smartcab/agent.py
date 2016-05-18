import random, operator, sys
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    VALID_ACTIONS = [None, 'forward', 'left', 'right']
    INITIAL_Q_VALUES = 0.0

    def __init__(self, env, gamma=None, epsilon=None, epsilon_decay=None):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # TODO: Initialize any additional variables here
        # Q-Learning Implementation following methods here (http://artint.info/html/ArtInt_265.html)
        # Another Great Q-Learning resource here https://www-s.acm.illinois.edu/sigart/docs/QLearning.pdf
        # One more here http://mnemstudio.org/path-finding-q-learning-tutorial.htm
        self.Q = {} #hashable Q-Table
        self.epsilon = 0.5 if epsilon == None else epsilon # randomness 0.5 == 50% random action
        self.epsilon_decay = 0.99 if epsilon_decay == None else epsilon_decay #decay rate (multiplier) for GLIE
        self.alpha = 0.2  # learning rate

        # if gamma == 1, the agent values future reward just as much as current reward
        # learning doesn't work well at high gamma values because of this
        self.gamma = 0.95 if gamma == None else gamma # future reward value multiplier

        # setup empty Q-Table
        for light_state in ['green', 'red']: # cycle through light state possibilites
            for oncoming_traffic_state in self.VALID_ACTIONS: # cycle through oncoming traffic state possiblities
                for right_traffic_state in self.VALID_ACTIONS: # cycle through right traffic state possiblities
                    for left_traffic_state in self.VALID_ACTIONS: # cycle through left traffic state possibilites
                        for waypoint_state in self.VALID_ACTIONS[1:]: # cycle through way point possibilites, slice off NONE
                            # record each state
                            state = (light_state, oncoming_traffic_state,
                                    right_traffic_state, left_traffic_state,
                                    waypoint_state)

                            # for each state point to dictionary of actions and values
                            self.Q[state] = {}
                            for action in self.VALID_ACTIONS:
                                self.Q[state][action] = self.INITIAL_Q_VALUES


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (inputs['light'], inputs['oncoming'], inputs['right'],
                      inputs['left'], self.next_waypoint)


        # TODO: Select action according to your policy
        if random.random() < self.epsilon:  # add randomness to the choice
            best_action = random.choice(self.VALID_ACTIONS)
        else:
            best_action = None
            max_Q = None
            #cycle through Q values for the given state looking for maximum
            for possible_action in self.Q[self.state]:
                if self.Q[self.state][possible_action] > max_Q:
                    best_action = possible_action
                    max_Q = self.Q[self.state][possible_action]

        #GLIE (decayed epsilon) Udacity: https://youtu.be/yv8wJiQQ1rc
        self.epsilon *= self.epsilon_decay

        # Execute action and get reward
        reward = self.env.act(self, best_action)

        # TODO: Learn policy based on state, action, reward
        # Estimating Q From Transitions - Udacity: https://youtu.be/Xr2U3BTkifQ
        # need to calculate utility of the state
        state = self.state

        # STEP 1: First find utility of the next state
        s_prime_inputs = self.env.sense(self) # sense after act
        s_prime_waypoint = self.planner.next_waypoint() # get next waypoint
        # setup s_prime
        s_prime = (s_prime_inputs['light'], s_prime_inputs['oncoming'],
            s_prime_inputs['right'], s_prime_inputs['left'], s_prime_waypoint)

        utility_of_next_state = None
        # cycle through each action_prime in state_prime searching for Max Q
        for a_prime in self.Q[s_prime]:
            if self.Q[s_prime][a_prime] > utility_of_next_state:
                utility_of_next_state = self.Q[s_prime][a_prime]

        #STEP 2: Find the utility of the state
        utility_of_state = reward + self.gamma * utility_of_next_state

        # update Q Table
        # transition by learning rate Q<s,a> = (1 - alpha) * Q<s,a> + alpha * utility_of_state
        self.Q[state][best_action] = (1 - self.alpha) * \
            self.Q[state][best_action] + self.alpha * utility_of_state

        # Update Learning Rate - Udacity: Learning Incrementally: https://youtu.be/FtRJKOvI_fs
        # Need this so for Q Convergence - Udacity: https://youtu.be/BEJKu3LzWJ4
        if t != 0:
            self.alpha = 1.0 / t

        #sanity check
        print self.Q[state]

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, best_action, reward)  # [debug]


def run(gamma=None, epsilon=None, epsilon_decay=None):
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent, gamma, epsilon, epsilon_decay)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    #record gamma, epsilon, and epsilon decay values as first line of print output
    print 'Gamma: {}, Epsilon: {}, Epsilon_Decay: {}'.format(
            a.gamma, a.epsilon, a.epsilon_decay)

    # Now simulate it
    sim = Simulator(e, update_delay=0.00001)  # reduce update_delay to speed up simulation
    sim.run(n_trials=5)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    arg_list = sys.argv # create a list from command line args

    # first check for args, will return empty lists if not found
    gamma_index = [i for i, s in enumerate(arg_list) if 'gamma' in s]
    epsilon_index = [i for i, s in enumerate(arg_list) if 'epsilon' in s]
    epsilon_decay_index = [i for i, s in enumerate(arg_list) if 'ep_decay' in s]

    # if args are in arg list split the values and save in variables
    gamma = float(arg_list[gamma_index[0]][7:]) if gamma_index else None
    epsilon = float(arg_list[epsilon_index[0]][9:]) if epsilon_index else None
    epsilon_decay = float(arg_list[epsilon_decay_index[0]][10:]) if epsilon_index else None

    run(gamma=gamma, epsilon=epsilon, epsilon_decay=epsilon_decay)
