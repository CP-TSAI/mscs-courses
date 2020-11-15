import argparse
import copy
import math
import time
import turtle
from typing import Tuple, Dict

import testing_suite_gem_finder as testing_suite
import gem_finder

PI = math.pi


class TurtleDisplay(object):
    WIDTH = 800
    HEIGHT = 800

    def __init__(self, xbounds: Tuple[float, float], ybounds: Tuple[float, float]):
        self.xbounds = xbounds
        self.ybounds = ybounds
        self.gem_turtles = {}
        self.gem_estimate_turtles = {}
        self.robot_turtle = None
        self.robot_heading = None
        self.robot_estimate_turtle = None

    def setup(self):
        xmin, xmax = self.xbounds
        ymin, ymax = self.ybounds
        dx = xmax - xmin
        dy = ymax - ymin
        margin = 0.3
        turtle.setup(width=self.WIDTH,
                     height=self.HEIGHT)
        turtle.setworldcoordinates(xmin - (dx * margin),
                                   ymin - (dy * margin),
                                   xmax + (dx * margin),
                                   ymax + (dy * margin))
        turtle.tracer(0, 1)
        turtle.hideturtle()
        turtle.penup()

    def start_time_step(self):

        for gem_id, trtl in self.gem_turtles.items():
            trtl.clear()

    def _new_turtle(self, shape: str = 'circle', color: str = 'gray', shapesize: Tuple[float, float] = (0.1, 0.1)):

        trtl = turtle.Turtle()
        trtl.shape(shape)
        trtl.color(color)
        trtl.shapesize(*shapesize)
        trtl.penup()
        return trtl

    def gem_at_location(self, gem_id: str, x: float, y: float):

        key = (gem_id, x, y)

        if key not in self.gem_turtles:
            self.gem_turtles[key] = self._new_turtle(shape='square',
                                                     color='gray',
                                                     shapesize=(0.5, 0.5))

        self.gem_turtles[key].setposition(x, y)
        self.gem_turtles[key]._write(str(gem_id)[:2], 'center', 'arial')

    def gem_estimate_at_location(self, gem_id: str, x: float, y: float):

        if gem_id not in self.gem_estimate_turtles:
            trtl = turtle.Turtle()
            trtl.shape("circle")
            trtl.color("black" if gem_id != 'self' else 'red')
            trtl.shapesize(0.2, 0.2)
            trtl.penup()
            self.gem_estimate_turtles[gem_id] = trtl

        self.gem_estimate_turtles[gem_id].setposition(x, y)

    def robot_at_location(self, x: float, y: float, bearing: float):

        if self.robot_turtle is None:
            self.robot_turtle = self._new_turtle(color='red',
                                                 shapesize=(0.5, 0.5))
            self.robot_heading = self._new_turtle(color='red', shape='arrow', shapesize=(0.5, 1.0))

        self.robot_turtle.setposition(x, y)
        self.robot_heading.setposition(x, y)
        self.robot_heading.settiltangle(math.degrees(bearing))

    def robot_estimate_at_location(self, x: float, y: float):

        if self.robot_estimate_turtle is None:
            self.robot_estimate_turtle = self._new_turtle(color='yellow',
                                                          shapesize=(0.3, 0.3))

        self.robot_estimate_turtle.setposition(x, y)

    def end_time_step(self):
        turtle.update()
        time.sleep(1.0)

    def done(self):
        turtle.done()


def bounds(state: testing_suite.State):
    robot_init_x = state.robot.x
    robot_init_y = state.robot.y

    xs = [robot_init_x] + [gem['x'] for gem in state.gem_locs_on_map]
    ys = [robot_init_y] + [gem['y'] for gem in state.gem_locs_on_map]

    return ((min(xs), max(xs)),
            (min(ys), max(ys)))


def part_A(params: Dict):
    area_map = params['area_map']
    state = testing_suite.State(area_map=area_map)

    robot_init_x = state.robot.x
    robot_init_y = state.robot.y
    robot_init_b = state.robot.bearing

    xbounds, ybounds = bounds(state)

    display = TurtleDisplay(xbounds=xbounds,
                            ybounds=ybounds)
    display.setup()

    display.start_time_step()
    display.robot_at_location(robot_init_x, robot_init_y, robot_init_b)
    display.end_time_step()

    try:

        rover_slam = gem_finder.SLAM()

        for move in params['move']:

            display.start_time_step()

            meas = state.generate_measurements()
            rover_slam.process_measurements(meas)

            action = move.split()
            state.update_according_to(move)
            belief_x, belief_y = rover_slam.process_movement(float(action[1]),
                                                             float(action[2]))
            belief = (belief_x + robot_init_x, belief_y + robot_init_y)
            truth = (state.robot.x - state._start_position['x'] + robot_init_x,
                     state.robot.y - state._start_position['y'] + robot_init_y)

            for gem in state.gem_locs_on_map:
                display.gem_at_location(gem['type'], gem['x'], gem['y'])

            display.robot_at_location(*truth, state.robot.bearing)
            display.robot_estimate_at_location(*belief)

            for location in state.gem_locs_on_map:
                x, y = rover_slam.get_coordinates_by_landmark_id(location['id'])
                display.gem_estimate_at_location(location['id'],
                                                 x + robot_init_x,
                                                 y + robot_init_y)

            display.end_time_step()

    except Exception as e:
        print(e)

    turtle.bye()


def part_B(params: Dict):
    area_map = params['area_map']
    gem_checklist = params['needed_gems']
    max_distance = params['max_distance']
    max_steering = params['max_steering']
    horizon = params['horizon']
    state = testing_suite.State(area_map=area_map,
                                gem_checklist=gem_checklist,
                                max_distance=max_distance,
                                max_steering=max_steering,
                                horizon=horizon)
    robot_init_x = state.robot.x
    robot_init_y = state.robot.y

    xbounds, ybounds = bounds(state)

    display = TurtleDisplay(xbounds=xbounds,
                            ybounds=ybounds)
    display.setup()

    # display initial state
    display.start_time_step()

    for gem in state.gem_locs_on_map:
        display.gem_at_location(gem['type'], gem['x'], gem['y'])

    display.robot_at_location(state.robot.x, state.robot.y, state.robot.bearing)

    display.end_time_step()

    try:
        student_planner = gem_finder.GemExtractionPlanner(max_distance, max_steering)

        while len(state.collected_gems) < len(gem_checklist):

            display.start_time_step()

            ret = student_planner.next_move(copy.deepcopy(state.gem_checklist),
                                            state.generate_measurements())

            try:
                action, locs = ret

            except IndexError:
                action = ret
                locs = None

            state.update_according_to(action)

            for gem in state.gem_locs_on_map:
                display.gem_at_location(gem['type'], gem['x'], gem['y'])

            display.robot_at_location(state.robot.x, state.robot.y, state.robot.bearing)

            if locs:
                for locid, xy in locs.items():
                    x, y = xy
                    if locid == 'self':
                        display.robot_estimate_at_location(x + robot_init_x,
                                                           y + robot_init_y)
                    else:
                        display.gem_estimate_at_location(locid,
                                                         x + robot_init_x,
                                                         y + robot_init_y)

            display.end_time_step()

        # One more time step to show final state.

        display.start_time_step()

        for gem in state.gem_locs_on_map:
            display.gem_at_location(gem['type'], gem['x'], gem['y'])

        display.robot_at_location(state.robot.x, state.robot.y, state.robot.bearing)
        display.end_time_step()

    except Exception as e:
        print(e)

    turtle.bye()


def main(part: str, case: str):
    try:
        if part == 'A':
            part_A(testing_suite.PartATestCase.params[case])
        elif part == 'B':
            part_B(testing_suite.PartBTestCase.params[case])
        else:
            raise ValueError(f'Testing Part {part} is not supported')
    except KeyError:
        raise ValueError(f'Testing Part {part} does not have a case {case}.')


def parser():
    prsr = argparse.ArgumentParser()
    prsr.add_argument('--part',
                      help="test part",
                      type=str,
                      choices=('A', 'B'))

    prsr.add_argument('--case',
                      help="test case",
                      type=int,
                      default=1,
                      choices=(1, 2, 3, 4, 5, 6, 7, 8, 9))
    return prsr


if __name__ == '__main__':
    args = parser().parse_args()
    main(part=args.part,
         case=args.case)
