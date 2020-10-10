from FlightData.Visualizer import Visualizer

import matplotlib.pyplot as plt


class MatPlotLibVisualizer(Visualizer):

    def __init__(self, title, x_size, y_size, number_of_sub_plots):
        super().__init__(title, x_size, y_size, number_of_sub_plots)
        self.rows = number_of_sub_plots
        self.cols = 1
        self.fig, self.axes = plt.subplots(self.rows, self.cols)
        self.fig.suptitle(title)
        self.fig.subplots_adjust(hspace=0.5)
        self.fig.set_figwidth(int(x_size / 75))
        self.fig.set_figheight(int(y_size / 75))
        self.current_plot_count = 0

    def add_plot(self, y_label, sub_data):
        for plot_data in sub_data:
            self.axes[self.current_plot_count].plot(plot_data['x'], plot_data['y'], color=plot_data['color'],
                                                    label=plot_data['label'])
            self.axes[self.current_plot_count].set_ylabel(y_label)
            self.axes[self.current_plot_count].legend(loc='upper right')

        self.current_plot_count += 1

    def done(self):
        plt.show()
