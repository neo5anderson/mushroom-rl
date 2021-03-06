import numpy as np

from mushroom_rl.algorithms.value.td import TD
from mushroom_rl.utils.table import Table


class RLearning(TD):
    """
    R-Learning algorithm.
    "A Reinforcement Learning Method for Maximizing Undiscounted Rewards".
    Schwartz A.. 1993.

    """
    def __init__(self, mdp_info, policy, learning_rate, beta):
        """
        Constructor.

        Args:
            beta (Parameter): beta coefficient.

        """
        self.Q = Table(mdp_info.size)
        self._rho = 0.
        self.beta = beta

        self._add_save_attr(Q='pickle', _rho='numpy', beta='pickle')

        super().__init__(mdp_info, policy, self.Q, learning_rate)

    def _update(self, state, action, reward, next_state, absorbing):
        q_current = self.Q[state, action]
        q_next = np.max(self.Q[next_state, :]) if not absorbing else 0.
        delta = reward - self._rho + q_next - q_current
        q_new = q_current + self.alpha(state, action) * delta

        self.Q[state, action] = q_new

        q_max = np.max(self.Q[state, :])
        if q_new == q_max:
            delta = reward + q_next - q_max - self._rho
            self._rho += self.beta(state, action) * delta
