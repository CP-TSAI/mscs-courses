from typing import Dict, List

from FlightData.Visualizer import Visualizer

class NoOpVisualizer(Visualizer):
    
    def __init__(self, title: str, x_size: int, y_size: int, number_of_sub_plots: int):
        pass

    def add_plot(self, y_label: str, sub_data: List[Dict]):
        pass

    def done(self):
        pass
