class RLAgent:
    """
    Abstract RL agent wrapper.

    Concrete implementations should override:
        - act()
        - learn()
    """

    def act(self, state):
        """
        Select action given state.
        """
        raise NotImplementedError

    def learn(self, env):
        """
        Train agent in the given environment.
        """
        raise NotImplementedError
