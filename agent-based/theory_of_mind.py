import pickle        
import numpy as np
from simplified_hanabi import Game
from mcts_training import Node

class TestGame(Game):
    def __init__(self, state_tree, orders):
        super(TestGame, self).__init__()

        self.state_tree = state_tree
        self.orders = orders

    @staticmethod
    def downgrade_order(order):
        if order == "ToM1":
            return "ToM0"
        elif order == "ToM2":
            return "ToM1"
        elif order == "ToM1+2":
            return "ToM0+ToM1"
        else:
            return None

    def get_action_values(self, w, order, legal_actions):
        if order == "ToM0":
            evs = []
            key = self.get_state_key(self.turn, w)
            #print(key)
            #print(self.state_tree[key])
            if key in self.state_tree.keys():
                for a in legal_actions:
                    ev = self.state_tree[key].get_ev(a) 
                    evs.append(ev)
            else:
                evs = [0.5 for a in legal_actions]
            return evs
        elif order == "ToM0+":
            evs = []
            key = self.get_state_key(self.turn, w)
            if key in self.state_tree.keys():
                for a in legal_actions:
                    ev = self.state_tree[key].get_ev(a) 
                    evs.append(ev)
            else:
                evs = [0.5 for a in legal_actions]

            lookahead = [0 for a in legal_actions]
            possible_worlds = self.players[self.turn].get_possible_worlds()
            for w in possible_worlds:
                for i, a in enumerate(legal_actions):
                    m = self.execute_action(a)
                    _, ev = self.select_action(w, "ToM0")
                    if ev != 0:
                        lookahead[i] = 1
                    self.undo_move(m)
            evs = [evs[i]*lookahead[i] for i in range(len(evs))]
            evs = [ev / len(possible_worlds) for ev in evs]
            return evs
            
        elif order == "ToM1" or order == "ToM2" or order == "ToM1+2":
            possible_worlds = self.players[self.turn].get_possible_worlds()
            evs = [0 for a in legal_actions]
            for w in possible_worlds:
                for i, a in enumerate(legal_actions):
                    m = self.execute_action(a)
                    _, ev = self.select_action(w, self.downgrade_order(order))                    
                    evs[i] += ev
                    self.undo_move(m)
            evs = [ev / len(possible_worlds) for ev in evs]
            return evs

        elif order == "ToM0+ToM1":
            evs0 = self.get_action_values(w, "ToM0", legal_actions)
            evs1 = self.get_action_values(w, "ToM1", legal_actions)
            evs = [(evs0[i] + evs1[i])/2 for i in range(len(legal_actions))]
            return evs
        elif order == "ToM1+ToM2":
            evs1 = self.get_action_values(w, "ToM1", legal_actions)
            evs2 = self.get_action_values(w, "ToM2", legal_actions)
            evs = [(evs1[i] + evs2[i])/2 for i in range(len(legal_actions))]
            return evs 
        else:
            print("ERROR: invalid ToM given")
        return None

    def select_action(self, w = None, order = None):
        if order == None:
            order = self.orders[self.turn]

        if w == None:
            w = self.true_worlds[1 - self.turn]

        legal_actions = self.get_legal_actions()
        if legal_actions == []:
            if (self.board["g"] + self.board["b"]) == 6:
                return None, 1
            else:
                return None, 0

        evs = self.get_action_values(w, order, legal_actions)
        ev, a = max(zip(evs, legal_actions))        

        return a, ev

def test_simulation(state_tree, orders, verbose = False):
    g = TestGame(state_tree, orders)
    while not g.game_over:
        a, _ = g.select_action()
        if verbose:
            print(g)
            print("Action: ", a)
        if a == None:
            g.game_over = True
            break
        g.execute_action(a)
    win = (g.board["g"] + g.board["b"]) == 6
    if verbose:
        print("Game Over")
        if win:
            print("Win")
        else:
            print("Loss")
    return win
    
def full_test(state_tree, orders, N):
    total_wins = 0
    for j in range(N):
        win = test_simulation(state_tree, orders)
        total_wins += win
    size = len(state_tree)
    acc = total_wins / N
    return acc

def load_dictionary():
    f = open("trees_mcts.dict", "rb")
    dictionary = pickle.load(f)
    f.close()
    return dictionary

if __name__ == "__main__":

    dictionary = load_dictionary()

    for idx in ['100', '200', '300', '400']:
        state_tree = dictionary[idx]
        print("Dictionary: ", idx)
        
        order_list = ["ToM0", "ToM0+", "ToM1", "ToM2", "ToM0+ToM1", "ToM1+ToM2", "ToM1+2"]
        
        for ord1 in order_list:
            for ord2 in order_list:
                print(ord1, "\t", ord2)
                print(full_test(state_tree, [ord1, ord2], 10000))
    
