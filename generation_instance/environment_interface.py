from abc import ABC, abstractmethod
import numpy as np


class Environment(ABC):

    @abstractmethod
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @abstractmethod
    def create_board(self, width: int, height: int) -> np.ndarray:
        pass

    @abstractmethod
    def set_states(self, width: int, height: int) -> tuple:
        pass
