# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A simple episode runner using the RL environment."""

from __future__ import print_function

import sys
import getopt
from hanabi_learning_environment import rl_env

from rb_agents import *

class Runner(object):
  """Runner class."""

  def __init__(self, flags):
    """Initialize runner."""
    self.flags = flags
    self.agent_config = {'players': flags['players']}
    self.environment = rl_env.make('Hanabi-Full', num_players=flags['players'])
    self.agent_classes = [AGENT_CLASSES[flags['agent_class_1']], AGENT_CLASSES[flags['agent_class_2']]]

  def run(self):
    """Run episodes."""
    rewards = []
    for episode in range(flags['num_episodes']):
      observations = self.environment.reset()
      agents = [self.agent_classes[i](self.agent_config)
                for i in range(self.flags['players'])]
      done = False
      episode_reward = 0
      while not done:
        for agent_id, agent in enumerate(agents):
          observation = observations['player_observations'][agent_id]
          action = agent.act(observation)
          if observation['current_player'] == agent_id:
            assert action is not None
            current_player_action = action
          else:
            assert action is None
        # Make an environment step.
        #print('Agent: {} action: {}'.format(observation['current_player'],
        #                                    current_player_action))
        observations, reward, done, unused_info = self.environment.step(
            current_player_action)
        episode_reward += reward
      rewards.append(episode_reward)
      #print('Running episode: %d' % episode)
      #print('Max Reward: %.3f' % max(rewards))
    return rewards

if __name__ == "__main__": 
    N = 1000
    averages = []
    stds = []
    for i, class_1 in enumerate(list(AGENT_CLASSES.keys())):
        averages.append([])
        stds.append([])
        for j, class_2 in enumerate(list(AGENT_CLASSES.keys())): 
            print(class_1, class_2)
            flags = {'players': 2, 'num_episodes': N, 'agent_class_1': class_1, 'agent_class_2': class_2}
            runner = Runner(flags)
            rewards = runner.run()
            mean = sum(rewards) / N
            mean = round(mean, 2)
            print("Mean: ", mean)
            variance = sum([(r - mean) ** 2 for r in rewards]) / N
            std = variance ** 0.5
            std = round(std, 2)
            print("Std: ", std)

            averages[i].append(mean)
            stds[i].append(std)

    print("averages")
    for row in averages:
        print(row)
    
    print("stds")
    for row in stds:
        print(row)

    


