from typing import Any, Dict

import gym
import numpy as np
import math


class Reward(gym.Wrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.posbefore = np.array([0, 0, 0])

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)

    def step(self, action):
        """Adapts the wrapped environment's step.

        Note: Users should not directly call this method.
        """
        obs, reward, done, info = self.env.step(action)
        # print("obs",obs)
        # print("reward",reward)
        # print("obs", obs)

        wrapped_reward = self._reward(obs, reward)

        for agent_id, agent_done in done.items():
            if agent_id != "__all__" and agent_done == True:
                if obs[agent_id]["events"]["reached_goal"]:
                    print(f"{agent_id}: Hooray! Reached goal.")
                elif obs[agent_id]["events"]["reached_max_episode_steps"]:
                    print(f"{agent_id}: Reached max episode steps.")
                elif (
                    obs[agent_id]["events"]["collisions"]
                    | obs[agent_id]["events"]["off_road"]
                    | obs[agent_id]["events"]["off_route"]
                    | obs[agent_id]["events"]["on_shoulder"]
                    | obs[agent_id]["events"]["wrong_way"]
                ):
                    pass
                else:
                    print("Events: ", obs[agent_id]["events"])
                    raise Exception("Episode ended for unknown reason.")

        return obs, wrapped_reward, done, info

    def _reward(
        self, obs: Dict[str, Dict[str, Any]], env_reward: Dict[str, np.float64]
    ) -> Dict[str, np.float64]:
        reward = {agent_id: np.float64(0) for agent_id in env_reward.keys()}

        for agent_id, agent_reward in env_reward.items():
            # Penalty for colliding
            if obs[agent_id]["events"]["collisions"]:
                reward[agent_id] -= np.float64(30)
                print(f"{agent_id}: Collided.")
                # break

            # Penalty for driving off road
            if obs[agent_id]["events"]["off_road"]:
                reward[agent_id] -= np.float64(10)
                print(f"{agent_id}: Went off road.")
                # break

            # Penalty for driving off route
            if obs[agent_id]["events"]["off_route"]:
                reward[agent_id] -= np.float64(5)
                print(f"{agent_id}: Went off route.")
                # break

            # Penalty for driving on road shoulder
            if obs[agent_id]["events"]["on_shoulder"]:
                reward[agent_id] -= np.float64(8)
                print(f"{agent_id}: Went on shoulder.")
                # break

            # Penalty for driving on wrong way
            if obs[agent_id]["events"]["wrong_way"]:
                reward[agent_id] -= np.float64(10)
                print(f"{agent_id}: Went wrong way.")
                # break

            # Penalty for driving stop
            if obs[agent_id]["events"]["not_moving"]:
                reward[agent_id] -= np.float64(0.5)
                print(f"{agent_id}: The car stops.")
                # break

            # Reward for reaching goal
            if obs[agent_id]["events"]["reached_goal"]:
                reward[agent_id] += np.float64(100)

            # Reward for distance travelled

            poserror = abs(sum(obs['Agent_0']['ego']['pos'] - self.posbefore))
            if(poserror == 0.0):
                agent_reward_mine = -np.float64(0.2)
                self.posbefore = obs['Agent_0']['ego']['pos']
            else:
                reward_std = 3
                delta = obs['Agent_0']['waypoints']['pos'][0][19]-obs['Agent_0']['waypoints']['pos'][0][0]
                tan = (delta[1])/(delta[0])
                angle = math.atan(tan)
                if angle < 0.01:
                    v_reference = 12
                elif angle > 0.7854:
                    v_reference = 8
                else:
                    v_reference = 10
                v_speed = -abs(obs['Agent_0']['ego']['speed'] - v_reference) * 0.1
                to_destination_distance_list = []
                y = obs['Agent_0']['waypoints']['pos'].shape[1]-1
                for i in range(obs['Agent_0']['waypoints']['pos'].shape[0]):
                    to_destination_distance_list.append(np.sqrt(np.sum(((obs['Agent_0']['mission']['goal_pos'] - obs['Agent_0']['waypoints']['pos'][i][y])**2))))
                min_index = to_destination_distance_list.index(min(to_destination_distance_list))
                v_deviation = -np.sqrt(np.sum((obs['Agent_0']['ego']['pos'] - obs['Agent_0']['waypoints']['pos'][min_index][0])**2))/100

                v_destination = -(np.sum((np.abs(obs['Agent_0']['ego']['pos'] - obs['Agent_0']['mission']['goal_pos'])))*0.01)
                v_collision = -(1/np.min(np.sqrt(np.sum(((obs['Agent_0']['ego']['pos'] - obs['Agent_0']['neighbors']['pos']) ** 2),axis=1))))*10
                # print("v_speed,v_deviation,v_destination,v_collision", v_speed, v_deviation, v_destination, v_collision)
                agent_reward_mine = reward_std + (v_speed + v_deviation + v_destination + v_collision)
                self.posbefore = obs['Agent_0']['ego']['pos']
            reward[agent_id] += np.float64(agent_reward_mine)
            # reward[agent_id] += np.float64(agent_reward)

            # Reward for distance travelled
            reward[agent_id] += np.float64(agent_reward)
            x_deta = np.abs((obs['Agent_0']['ego']['pos'] - obs['Agent_0']['mission']['goal_pos'])[0])
            y_deta = np.abs((obs['Agent_0']['ego']['pos'] - obs['Agent_0']['mission']['goal_pos'])[1])
            if np.abs((x_deta+y_deta) - 30)<0.5:
                reward[agent_id] += np.float64(10)
            v_destination = 5/(y_deta+x_deta+0.1)
            reward[agent_id] += np.float64(v_destination)

        return reward

