import random
from hanabi_learning_environment.rl_env import Agent
from .custom_agent import CustomAgent

COLOR_CHAR = ["R", "Y", "G", "W", "B"]  # consistent with hanabi_lib/util.cc

class IntSuperSafe(CustomAgent):

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
    if observation['information_tokens'] < self.max_information_tokens:
        action = self.discard_safe(observation, fireworks, discard_pile)
        if not action == None:
            return action

    player_offset = 1
    player_hand = observation['observed_hands'][player_offset]
    player_hints = observation['card_knowledge'][player_offset]
    
    if observation['information_tokens'] > 0:
        a = self.select_hint(observation, fireworks, player_hand, player_hints, player_offset, intent = True, maxinfo = True)
        if not a == None:
            return a

    # If no card is hintable then discard or play.
    if observation['information_tokens'] < self.max_information_tokens:
      return {'action_type': 'DISCARD', 'card_index': 0}
    else:
      return {'action_type': 'PLAY', 'card_index': 4}
