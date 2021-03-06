"""
Created on Sat Jan  2 15:39:10 2022

@author: Charlie
"""

from typing import List
import os
import cv2
from dqn_agent import DQNAgent
from tetris import Tetris
from run_train import AgentConf
from keras.engine.saving import load_model
from sys import exit

def run_eval(dir_name: str, episodes: int = 100, render: bool = False) -> List[int]:
    agent_conf = AgentConf()
    env = Tetris()
    agent = DQNAgent(env.get_state_size(),
                     n_neurons=agent_conf.n_neurons, activations=agent_conf.activations,
                     epsilon_stop_episode=agent_conf.epsilon_stop_episode, mem_size=agent_conf.mem_size,
                     discount=agent_conf.discount, replay_start_size=agent_conf.replay_start_size)

    

    log_dir = 'logs/' + dir_name

    # load_model
    agent.model = load_model(f'{log_dir}/model.hdf')
    agent.epsilon = 0
    scores = []
    for episode in range(episodes):
        env.reset()
        done = False

        while not done:
            next_states = env.get_next_states()
            best_state = agent.best_state(next_states.values())

            # find the action, that corresponds to the best state
            best_action = None
            for action, state in next_states.items():
                if state == best_state:
                    best_action = action
                    break
            _, done = env.hard_drop([best_action[0], 0], best_action[1], render=render)
        scores.append(env.score)
        # print results at the end of the episode
        print(f'episode {episode} => {env.score}')
    return scores


def enumerate_run_eval(episodes: int = 128, render: bool = False):
    dirs = [name for name in os.listdir('logs') if os.path.isdir(os.path.join('logs', name))]
    dirs.sort(reverse=True)
    dirs = [dirs[0]]  # take the most recent model
    # dirs = [
    #     'tetris-0108-231806-ms25000-e1-ese2000-d0.99',
    #     'tetris-0107-140127-ms25000-e1-ese2000-d0.99',
    # ]
    dirs = ['tetris-0108-231806-ms25000-e1-ese2000-d0.99', 'tetris-0107-140127-ms25000-e1-ese2000-d0.99']
    max_scores = []
    for d in dirs:
        print(f"Evaluating dir '{d}'")
        scores = run_eval(d, episodes=episodes, render=render)
        max_scores.append((d, max(scores)))

    max_scores.sort(key=lambda t: t[1], reverse=True)
    for k, v in max_scores:
        print(f"{v}\t{k}")


if __name__ == "__main__":
    enumerate_run_eval(episodes=16, render=True)
    cv2.destroyAllWindows()
    exit(0)
