from turtle import Screen, Turtle

from typing import NamedTuple, Any, Sequence

from FlightData.Visualizer import Visualizer


class TurtleVisualizer(Visualizer):

    def __init__(self, title, x_size, y_size, number_of_sub_plots):
        super().__init__(title, x_size, y_size, number_of_sub_plots)
        self.x_size = x_size
        self.y_size = int(y_size / number_of_sub_plots + 2)
        self.plot = TurtlePlot(x_size, y_size, title)
        self.current_plot_count = number_of_sub_plots - 1

    def add_plot(self, y_label, sub_data):
        xys = list()
        for plot_data in sub_data:
            record = XYSeriesRecord(x=plot_data['x'],
                                    y=plot_data['y'],
                                    color=plot_data['color'],
                                    label=plot_data['label'])
            xys.append(record)

        plot_record = PlotRecord(ylabel=y_label,
                                 xys=xys)

        y_lower = self.current_plot_count * self.y_size
        y_upper = y_lower + self.y_size
        self.plot.draw(plot_record, x_bounds=(0, self.x_size), y_bounds=(y_lower, y_upper))

        self.current_plot_count -= 1

    def done(self):
        self.plot.done()


class XYSeriesRecord(NamedTuple):
    x: Any  # list or np array
    y: Any  # list or np array
    color: str = "#000000"
    label: str = ''


class PlotRecord(NamedTuple):
    ylabel: str
    xys: Sequence[XYSeriesRecord]


class TurtlePlot:

    def __init__(self, width, height, title=""):
        """
        Initialize a Turtle Plot
        Args:
            width: Width of the screen
            height: Height of the screen
        """

        self.width = width
        self.height = height
        self.title = title
        self.screen = Screen()
        self.screen.clear()

        self.screen.setup(width=width, height=height)
        self.screen.setworldcoordinates(0, 0, width, height)
        self.screen.tracer(0, 1)
        self.screen.onclick(lambda x, y: self.zoom_in(x, y))
        self.screen.title(self.title + "  (click to zoom in)")

    def done(self):
        """
        Wait until user clicks or closes screen.
        """
        self.screen.mainloop()

    def _setworldcoordinates(self, xmin, ymin, xmax, ymax):
        try:
            self.screen.setworldcoordinates(xmin, ymin, xmax, ymax)
        except Exception as e:
            pass

    def zoom_in(self, x, y):
        self._setworldcoordinates(x - 50, y - 50, x + 50, y + 50)
        self.screen.onclick(lambda x, y: self.zoom_out())
        self.screen.title(self.title + "  (click to zoom out)")

    def zoom_out(self):
        self._setworldcoordinates(0, 0, self.width, self.height)
        self.screen.onclick(lambda x, y: self.zoom_in(x, y))
        self.screen.title(self.title + "  (click to zoom in)")

    def draw(self, plot_record: PlotRecord, x_bounds, y_bounds):
        """
        Draw a plot on the turtle screen.
        Args:
            plot_record: The plot record to display.
            x_bounds: The plots x bounds
            y_bounds: The plots y bounds
        """
        outline_turtle = Turtle()
        outline_turtle.hideturtle()

        xy_turtles = [Turtle() for _ in plot_record.xys]
        for i, trtl in enumerate(xy_turtles):
            trtl.penup()
            trtl.pensize(2)
            trtl.pencolor(plot_record.xys[i].color)
            trtl.hideturtle()

        turtle_xmin, turtle_xmax = x_bounds
        turtle_ymin, turtle_ymax = y_bounds
        turtle_dx = turtle_xmax - turtle_xmin
        turtle_dy = turtle_ymax - turtle_ymin

        # leave 20% space on left and bottom
        # for labeling
        turtle_margin_left = 0.2
        turtle_margin_right = 0.2
        turtle_margin_bottom = 0.3
        turtle_margin_top = 0.3
        turtle_x_chart_min = turtle_xmin + (turtle_dx * turtle_margin_left)
        turtle_y_chart_min = turtle_ymin + (turtle_dy * turtle_margin_bottom)
        turtle_x_chart_max = turtle_xmax - (turtle_dx * turtle_margin_right)
        turtle_y_chart_max = turtle_ymax - (turtle_dy * turtle_margin_top)
        turtle_dx_chart = turtle_x_chart_max - turtle_x_chart_min
        turtle_dy_chart = turtle_y_chart_max - turtle_y_chart_min
        fontsize = 8

        outline_turtle.penup()
        outline_turtle.setposition(turtle_xmin, (turtle_y_chart_min + turtle_y_chart_max) * 0.5)
        outline_turtle.write(plot_record.ylabel)
        outline_turtle.setposition(turtle_x_chart_min, turtle_y_chart_max)
        outline_turtle.pendown()
        outline_turtle.setposition(turtle_x_chart_min, turtle_y_chart_min)
        outline_turtle.setposition(turtle_x_chart_max, turtle_y_chart_min)
        outline_turtle.penup()

        all_xs = [x for xy in plot_record.xys for x in xy.x]
        all_ys = [y for xy in plot_record.xys for y in xy.y]

        series_xmin = min(all_xs)
        series_xmax = max(all_xs)
        series_ymin = min(all_ys)
        series_ymax = max(all_ys)

        series_dx = (series_xmax - series_xmin) or 1
        series_dy = (series_ymax - series_ymin) or 1

        # scale factor from series to turtle
        xscale = turtle_dx_chart / series_dx
        yscale = turtle_dy_chart / series_dy

        outline_turtle.setposition(turtle_x_chart_min - fontsize,
                                   turtle_y_chart_max - (fontsize * 0.5))
        outline_turtle.write("%0.02f" % series_ymax, align='right')

        outline_turtle.setposition(turtle_x_chart_min - fontsize,
                                   turtle_y_chart_min + (turtle_dy_chart * 0.5) - (fontsize * 0.5))
        outline_turtle.write("%0.02f" % ((series_ymin + series_ymax) * 0.5), align='right')

        outline_turtle.setposition(turtle_x_chart_min - fontsize,
                                   turtle_y_chart_min - (fontsize * 0.5))
        outline_turtle.write("%0.02f" % series_ymin, align='right')

        outline_turtle.setposition(turtle_x_chart_max, turtle_y_chart_min - (fontsize * 2))
        outline_turtle.write("%0.02f" % series_xmax, align='center')

        outline_turtle.setposition(turtle_x_chart_min + (turtle_dx_chart * 0.5) - fontsize,
                                   turtle_y_chart_min - (fontsize * 2))
        outline_turtle.write("%0.02f" % ((series_xmin + series_xmax) * 0.5), align='center')

        outline_turtle.setposition(turtle_x_chart_min,
                                   turtle_y_chart_min - (fontsize * 2))
        outline_turtle.write("%0.02f" % series_xmin, align='center')

        for i, xy in enumerate(plot_record.xys):

            # position turtle at first xy value
            xy_turtles[i].setposition(turtle_x_chart_min + (xscale * (xy.x[0] - series_xmin)),
                                      turtle_y_chart_min + (yscale * (xy.y[0] - series_ymin)))
            xy_turtles[i].pendown()

            for j in range(min(len(xy.x), len(xy.y))):
                xy_turtles[i].setposition(turtle_x_chart_min + (xscale * (xy.x[j] - series_xmin)),
                                          turtle_y_chart_min + (yscale * (xy.y[j] - series_ymin)))

            xy_turtles[i].penup()
            xy_turtles[i].setposition(turtle_x_chart_max + (fontsize * 2),
                                      turtle_y_chart_max - (fontsize * 2 * i))
            xy_turtles[i].write(xy.label, align='left')
