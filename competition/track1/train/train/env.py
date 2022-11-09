from typing import Any, Dict, List

import gym
import sys
from pathlib import Path
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor
from train.info import Info   # 这是自己编写的train
from train.reward import Reward   # 这是自己编写的train

from smarts.core.controllers import ActionSpaceType
from smarts.env.wrappers.format_action import FormatAction
from smarts.env.wrappers.format_obs import FormatObs
from smarts.env.wrappers.frame_stack import FrameStack
from smarts.env.wrappers.single_agent import SingleAgent

# To import submission folder
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from submission.action import Action as DiscreteAction              # 这是自己编写的submission
from submission.observation import Concatenate, FilterObs, SaveObs  # 这是自己编写的submission

# wrappers是包装器，通过从 ActionWrapper、ObservationWrapper 或 RewardWrapper 继承并实现转化动作、转化观测、转化reward
def wrappers(config: Dict[str, Any]):
    # fmt: off
    wrappers = [
        # Used to format observation space such that it becomes gym-space compliant.
        FormatObs,
        # Used to format action space such that it becomes gym-space compliant.
        lambda env: FormatAction(env=env, space=ActionSpaceType["TargetPose"]),
        Info,
        # Used to shape rewards.
        Reward,
        # Used to save selected observation parameters for use in DiscreteAction wrapper.
        SaveObs,
        # Used to discretize action space for easier RL training.  离散的action
        DiscreteAction,
        # Used to filter only the selected observation parameters.
        FilterObs,
        # Used to stack sequential observations to include temporal information. 
        lambda env: FrameStack(env=env, num_stack=config["num_stack"]),
        # Concatenates stacked dictionaries into numpy arrays.
        lambda env: Concatenate(env=env, channels_order="first"),
        # Modifies interface to a single agent interface, which is compatible with libraries such as gym, Stable Baselines3, TF-Agents, etc.
        SingleAgent,
        lambda env: DummyVecEnv([lambda: env]),
        lambda env: VecMonitor(venv=env, filename=str(config["logdir"]), info_keywords=("is_success",))
    ]
    # fmt: on

    return wrappers


def make(
    config: Dict[str, Any], scenario: str, wrappers: List[gym.Wrapper] = []
) -> gym.Env:
    """Make environment.

    Args:
        config (Dict[str, Any]): A dictionary of config parameters.
        scenario (str): Scenario
        wrappers (List[gym.Wrapper], optional): Sequence of gym environment wrappers.
            Defaults to empty list [].

    Returns:
        gym.Env: Environment corresponding to the `scenario`.
    """

    # Create environment
    # gym.make()的输入：环境ID，输出：环境实例env
    # 通过环境ID找到单个环境
    env = gym.make(
        "smarts.env:multi-scenario-v0",
        scenario=scenario,
        img_meters=config["img_meters"],
        img_pixels=config["img_pixels"],
        sumo_headless=not config["sumo_gui"],  # If False, enables sumo-gui display.
        headless=not config["head"],  # If False, enables Envision display.
    )

    # Wrap the environment 包装环境
    for wrapper in wrappers:
        env = wrapper(env)

    return env
