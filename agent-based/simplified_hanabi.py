import itertools as it
import numpy as np
import math
import random

#Game object contains all the rules for simulating a game
class Game:
    def __init__(self):
        
        ###set up the board state
        self.board = {"g":0, "b":0, "h":2}
        DECK = np.array(['g1', 'g1', 'g2', 'g3', 'b1', 'b1', 'b2', 'b3'])
        seed = random.randint(1, 100)
        np.random.seed(seed)
        np.random.shuffle(DECK)
        self.game_over = False

        # Create a deterministically ordered list of unique possible worlds for each player
        l0 = list(it.permutations(DECK[0:4]))
        l1 = list(it.permutations(DECK[4:8]))
        l0_unique = []
        for hand in l0:
            if not hand in l0_unique:
                l0_unique.append(hand)
        l1_unique = []
        for hand in l1:
            if not hand in l1_unique:
                l1_unique.append(hand)
        
        #All possible configurations of the cards given initial observation. A player's knowledge is defined as a subset of this list
        self.worlds = [np.array(l0_unique),
                        np.array(l1_unique)]

        self.true_worlds = [0, 0]

        #set up the players
        self.players = [Player(self.worlds[0]), Player(self.worlds[1])]
        self.turn = 0

        #Record which cards have been played/discarded
        self.played = [np.zeros(4, dtype=bool), np.zeros(4, dtype=bool)]

    def get_cards(self, player, w = None):
        if w == None:
            w = self.true_worlds[player]
        return self.worlds[player][w]

    def get_state_key(self, player, world):
        key = str(self.board["g"]) + str(self.board["b"]) + str(self.board["h"])
        for c in sorted(self.get_cards(1 - player, world)):
            key += str(c)
        for p in self.played:
            for x in p:
                key += str(int(x))
        for x in self.players[player].possible_worlds:
            key += str(x)
        return key

    def get_legal_actions(self):
        if self.game_over:
            return []
        legal_actions = []

        #Add plays and discards
        for idx in [i for i in range(4) if not self.played[self.turn][i]]:
            legal_actions.append("p{}".format(str(idx)))
            if self.board["h"] < 2:
                legal_actions.append("d{}".format(str(idx)))

        #Add hints
        if self.board["h"] > 0:
            for h in ['b', 'g', '1', '2', '3']:
                if any([h in x for x in self.get_cards(1 - self.turn)]):
                    legal_actions.append("h{}".format(h))
        return legal_actions 

    #Takes the action, and returns a record of the action
    def execute_action(self, action):
        m = Move(action) #record the effects of the action here

        if action[0] == "p":
            idx = int(action[1])
            card = self.get_cards(self.turn)[idx]
            if (self.board[card[0]] + 1) == int(card[1]):
                self.board[card[0]] += 1
            else:
                self.game_over = True
            self.played[self.turn][idx] = True
            
            #Record the worlds that get deleted from the player's belief
            m.impossible_worlds = self.players[self.turn].observe_card(idx, card)
            m.learning_agent = self.turn #The agent is learning about its own cards

        if action[0] == "d":
            idx = int(action[1])
            card = self.get_cards(self.turn)[idx]
            self.board["h"] += 1
            self.played[self.turn][idx] = True

            #Record the worlds that get deleted from the player's belief
            m.impossible_worlds = self.players[self.turn].observe_card(idx, card)
            m.learning_agent = self.turn #The agent is learning about its own cards

        if action[0] == "h":
            h = action[1]
            self.board["h"] -= 1

            #Record the worlds that get deleted from the partner's belief
            m.impossible_worlds = self.players[1 - self.turn].receive_hint(h, self.get_cards(1 - self.turn))
            m.learning_agent = 1 - self.turn #The partner is learning

        self.turn = 1 - self.turn

        return m

    def undo_move(self, m):
        self.turn = 1 - self.turn

        if m.action[0] == "p":
            idx = int(m.action[1])
            self.played[self.turn][idx] = False
            if self.game_over:
                self.game_over = False
            else:
                card = self.get_cards(self.turn)[idx]
                self.board[card[0]] -= 1
        if m.action[0] == "d":
            self.board["h"] -= 1
            idx = int(m.action[1])
            self.played[self.turn][idx] = False
        if m.action[0] == "h":
            self.board["h"] += 1
        
        self.players[m.learning_agent].unlearn(m.impossible_worlds) 

    def __str__(self):
        s = "\n\nBoard:\t" + str(self.board) + "\n"
        s += "Played: player1 - " + str(self.played[0]) + "\t player2 - " + str(self.played[1]) + "\n"
        s += "Possible Worlds:\n"
        for i in range(2):
            s += "\tPlayer {0}:\n".format(str(i+1))
            for j, w in enumerate(self.players[i].get_possible_worlds()):
                s += "\t\t" + str(self.worlds[i][w])
                if j == 0:
                    s += "<< True world"
                s += "\n"
        s += "Turn: Player " + str(self.turn + 1)
        return s

class Move:
    def __init__(self, action):
        self.action = action
        self.learning_agent = None
        self.impossible_worlds = None

class Player:
    def __init__(self, all_worlds):
        self.all_worlds = all_worlds
        #Record which worlds are still possible
        self.possible_worlds = np.ones(len(self.all_worlds), dtype=bool) 

    def get_possible_worlds(self):
        worlds = []
        for i, _ in enumerate(self.all_worlds):
            if self.possible_worlds[i]:
                worlds.append(i)
        return np.array(worlds)

    def observe_card(self, idx, card):
        impossible_worlds = []
        for i, w in enumerate(self.all_worlds):
            if self.possible_worlds[i] and w[idx] != card:
                impossible_worlds.append(i)
                self.possible_worlds[i] = False
        return impossible_worlds

    def receive_hint(self, h, true_cards):
        impossible_worlds = []
        for i, w in enumerate(self.all_worlds):
            if self.possible_worlds[i] and any([h in true_cards[j] and not h in w[j] for j in range(len(true_cards))]):
                impossible_worlds.append(i)
                self.possible_worlds[i] = False
        return impossible_worlds

    def unlearn(self, impossible_worlds):
        for idx in impossible_worlds:
            self.possible_worlds[idx] = True

