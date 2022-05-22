import pickle
import random
import copy
import math
import numpy as np
from simplified_hanabi import Game

C = math.sqrt(2)

class Node:
    def __init__(self, legal_actions):
        self.N = 0
        self.n = {a:0 for a in legal_actions}
        self.w = {a:0 for a in legal_actions}
        self.actions = legal_actions  

    def __str__(self):
        return str(self.N) + str(self.n) + str(self.w) + str(self.actions)

    def is_leaf(self):
        if any([self.n[a]==0 for a in self.n]):
            return True
        else:
            return False

    def select(self):
        ucb_max = 0
        max_a = None
        for i, a in enumerate(self.actions):
            ucb = self.w[a]/self.n[a] + C * math.sqrt( math.log(self.N) / self.n[a] )
            if ucb > ucb_max:
                max_a = a
                ucb_max = ucb
        return max_a

    def expand(self):
        for a in self.actions:
            if self.n[a] == 0:
                return a
        return None
    
    def update(self, a, win):
        self.n[a] += 1
        self.N += 1
        self.w[a] += win

    def get_ev(self, a):
        return (self.w[a] + 1) / (self.n[a] + 2)

class TrainGame(Game):
    def __init__(self, state_tree):
        super(TrainGame, self).__init__()
        
        self.state_tree = state_tree

        self.history = []
        self.rollout = False
    
    def select_action(self, w = None):
        if w == None:
            w = self.true_worlds[1 - self.turn]

        legal_actions = self.get_legal_actions()
        if legal_actions == []:
            return None, None
        key = self.get_state_key(self.turn, w)
        if key in self.state_tree.keys():
            if self.state_tree[key].is_leaf():
                action = self.state_tree[key].expand()
            else:
                action = self.state_tree[key].select()
            
            self.history.append([key, action])
        else:
            action = np.random.choice(legal_actions)
            if not self.rollout: 
                self.state_tree[key] = Node(legal_actions)
                self.history.append([key, action])
                self.rollout = True
        return action, None

    def backpropagate_mcts(self, win):
        for [key,action] in self.history:
            self.state_tree[key].update(action, win)

def run_simulation(st):
    g = TrainGame(st)
    while not g.game_over:
        a, _ = g.select_action()
        if a == None:
            g.game_over = True
            break
        g.execute_action(a)
    win = (g.board["g"] + g.board["b"]) >= 6
    g.backpropagate_mcts(win)
    return win

if __name__ == "__main__":
    
    from theory_of_mind import full_test

    state_tree = {}
    size_data = []
    accuracy_data = []
    
    tree_dict = {}
    idx = 0

    print("{0:20}{1:20}{2:20}{3:20}".format("Iteration (10k)", "Tree Size", "TrainAcc", "TestAcc"))
    
    for i in range(400):
        total_wins = 0
        for j in range(10000):
            win = run_simulation(state_tree)
            total_wins += win
        size = len(state_tree)
        train_acc = total_wins / 10000

        test_acc = full_test(state_tree, ["ToM0", "ToM0"], 10000)
        
        print("{0:20}{1:20}{2:20}{3:20}".format(str(i+1), str(size), str(train_acc), str(test_acc)))
        
        size_data.append(size)
        accuracy_data.append(test_acc)
    
        if (i + 1) % 50 == 0:
            print("logged state at accuracy:", test_acc)
            tree_dict[str(i+1)] = copy.deepcopy(state_tree)
            idx += 1

    print("Saving dictiorary...")
    f_results = open("trees_mcts.dict", "wb")
    pickle.dump(tree_dict, f_results)
    f_results.close()

    trajectory = {"size_data": size_data, "win_rate": accuracy_data}
    f_results2 = open("log_training.dict", "wb")
    pickle.dump(trajectory, f_results2)
    f_results2.close()
