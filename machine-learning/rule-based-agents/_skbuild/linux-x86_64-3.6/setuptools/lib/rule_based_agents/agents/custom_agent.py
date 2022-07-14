import random
from hanabi_learning_environment.rl_env import Agent

COLOR_CHAR = ["R", "Y", "G", "W", "B"]  # consistent with hanabi_lib/util.cc

class CustomAgent(Agent):

  def __init__(self): #, config, *args, **kwargs):
    """Initialize the agent."""
    #self.config = config
    # Extract max info tokens or set default to 8.
    self.max_information_tokens = 8 #config.get('information_tokens', 8)

  @staticmethod
  def playable_card(card, fireworks):
    """A card is playable if it can be placed on the fireworks pile."""
    return card['rank'] == fireworks[card['color']]

  def safe_to_play(self, card, fireworks, threshold = 1):
    total_plausible = 0
    total_safe = 0
    for color in [0,1,2,3,4]:
        for rank in [0,1,2,3,4]:
            if card.color_plausible(color) and card.rank_plausible(rank):
                if self.playable_card( {'rank':rank, 'color':COLOR_CHAR[color]}, fireworks):
                    total_safe += 1
                total_plausible += 1
    if total_safe / total_plausible >= threshold:
        return True, (total_safe / total_plausible)
    return False, 0

  @staticmethod
  def safe_to_discard(card, fireworks, discard_pile, threshold = 1):
    total_plausible = 0
    total_safe = 0
    for color in [0,1,2,3,4]:
        for rank in [0,1,2,3,4]:
            if card.color_plausible(color) and card.rank_plausible(rank):
                if rank < fireworks[COLOR_CHAR[color]]:
                    total_safe += 1
                total_plausible += 1
    if total_safe / total_plausible >= threshold:
        return True, (total_safe / total_plausible)
    return False, 0

  def play_safe(self, observation, fireworks, threshold = 1):
    actions = []
    max_prob = threshold
    cards = [card for card in observation['pyhanabi'].card_knowledge()[0]]
    for idx, card in enumerate(cards):
        safe, prob = self.safe_to_play(card, fireworks, threshold)
        if safe and prob == max_prob:
            actions.append({'action_type': 'PLAY', 'card_index': idx})
        elif safe and prob > max_prob:
            actions = [{'action_type': 'PLAY', 'card_index': idx}]
            max_prob = prob
    if len(actions) > 0:
        return random.choice(actions)
    else:
        return None

  def discard_safe(self, observation, fireworks, discard_pile, threshold = 1):
    actions = []
    max_prob = threshold
    cards = [card for card in observation['pyhanabi'].card_knowledge()[0]]
    for idx, card in enumerate(cards):
        safe, prob = self.safe_to_discard(card, fireworks, discard_pile, threshold)
        if safe and prob == max_prob:
            actions.append({'action_type': 'DISCARD', 'card_index': idx})
        elif safe and prob > max_prob:
            actions = [{'action_type': 'DISCARD', 'card_index': idx}]
            max_prob = prob
    if len(actions) > 0:
        return random.choice(actions)
    else:
        return None

  def select_hint(self, observation, fireworks, player_hand = None, player_hints = None, player_offset = None, intent = False, maxinfo = False): 
    hint_moves = [move for move in observation['legal_moves'] if 'REVEAL' in move['action_type']]      
    if intent:
        if self.playable_card(player_hand[-1], fireworks):
            a = {
                'action_type': 'REVEAL_COLOR',
                'color': player_hand[-1]['color'],
                'target_offset': player_offset
                }
            return a

        legal_moves = []
        for m in hint_moves:
            if m['action_type'] == "REVEAL_COLOR":
                if player_hand[-1]['color'] != m['color']:
                    legal_moves.append(m)
            if m['action_type'] == "REVEAL_RANK":
                if player_hand[-1]['rank'] != m['rank']:
                    legal_moves.append(m)
    else:
        legal_moves = hint_moves

    if maxinfo:
        top_info = 0
        best_moves = []
        for m in legal_moves:
            total = 0
            for idx, card in enumerate(player_hand):
                if m['action_type'] == "REVEAL_COLOR" and player_hints[idx]['color'] == None:
                    if m['color'] == card['color']:
                        total += 1
                if m['action_type'] == "REVEAL_RANK" and player_hints[idx]['rank'] == None:
                    if m['rank'] == card['rank']:
                        total += 1
            if total == top_info:
                best_moves.append(m)
            if total > top_info:
                best_moves = [m]
                top_info = total
    else:
        best_moves = legal_moves

    if len(best_moves) > 0:
        return random.choice(best_moves)
    else:
        return None

  def act(self, observation):
    """Act based on an observation."""
    if observation['current_player_offset'] != 0:
      return None

    fireworks = observation['fireworks']
    discard_pile = observation['discard_pile']

    # Check if any cards are safely playable
    action = self.play_safe(observation, fireworks)
    if not action == None:
        return action
    
    # Check if any cards are safely discardable
    action = self.discard_safe(observation, discard_pile)
    if not action == None:
        return action

    # Check if it's possible to hint a card to your colleagues.
    if observation['information_tokens'] > 0:
      hint_moves = [move for move in observation['legal_moves'] if 'REVEAL' in move['action_type']]      
      return random.choice(hint_moves)

    # If no card is hintable then discard or play.
    if observation['information_tokens'] < self.max_information_tokens:
      return {'action_type': 'DISCARD', 'card_index': 0}
    else:
      return {'action_type': 'PLAY', 'card_index': 4}
