from abc import ABC, abstractmethod

from typing import Dict, List


class Visualizer(ABC):
    @abstractmethod
    def __init__(self, title: str, x_size: int, y_size: int, number_of_sub_plots: int):
        pass

    @abstractmethod
    def add_plot(self, y_label: str, sub_data: List[Dict]):
        pass

    @abstractmethod
    def done(self):
        pass
