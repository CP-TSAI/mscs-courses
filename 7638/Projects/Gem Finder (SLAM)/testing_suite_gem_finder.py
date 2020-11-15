#!/usr/bin/python

######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

import unittest
import random
import math
import time
import traceback
import hashlib
import copy
import string
from typing import List, Dict

try:
    import gem_finder

    studentExc = None
except Exception as e:
    studentExc = e
import robot

PI = math.pi

########################################################################
# for debugging set the time limit to a big number
########################################################################
TIME_LIMIT = 5  # seconds

########################################################################
# set to True for lots-o-output, also passed into robot under test
########################################################################
VERBOSE_FLAG = False

########################################################################
# set to True to disable multiprocessing while running in a debugger
########################################################################
DEBUGGING_SINGLE_PROCESS = False

########################################################################
# TODO: you can set NOISE_FLAG to false during development
# but be sure to run and test with noise = True
# before submitting your solution.
########################################################################
NOISE_FLAG = True
NOISE_MOVE = 0.01

if DEBUGGING_SINGLE_PROCESS:
    import multiprocessing.dummy as mproc
else:
    import multiprocessing as mproc

########################################################################
# used to generate unique ids for landmarks.  will change for grader
########################################################################
HASH_SEED = 'some_seed'

PART_A_CREDIT = 0.40
PART_B_CREDIT = 0.60

# DO NOT REMOVE THESE VARIABLES.
PART_A_SCORE = None
PART_B_SCORE = None


class Submission:
    """Student Submission.

    Attributes:
        submission_action_plan(Queue): Student score of executed action plan.
        submission_error(Queue): Error messages generated during executed action plan.
        submission_reported_gem_locations(Queue): log of gem locations reported by the extract action used for grading.
    """

    def __init__(self):

        # if DEBUGGING_SINGLE_PROCESS:
        #     import queue
        #     self.time_left = queue.Queue(1)
        #     self.submission_action_plan = queue.Queue(1)
        #     self.submission_error = queue.Queue(1)
        #     self.submission_reported_gem_locations = queue.Queue(1)
        # else:
        self.time_left = mproc.Manager().Queue(1)
        self.submission_action_plan = mproc.Manager().Queue(1)
        self.submission_error = mproc.Manager().Queue(1)
        self.submission_reported_gem_locations = mproc.Manager().Queue(1)

    def _reset(self):
        """Reset submission results.
        """
        while not self.time_left.empty():
            self.submission_action_plan.get()
        self.time_left.put(True)

        while not self.submission_action_plan.empty():
            self.submission_action_plan.get()

        while not self.submission_error.empty():
            self.submission_error.get()

        while not self.submission_reported_gem_locations.empty():
            self.submission_reported_gem_locations.get()

    def execute_student_plan(self, area_map: List[list], gem_checklist: List[str], max_distance: float = 1.0,
                             max_steering: float = PI / 2. + 0.01, robot_distance_noise: float = 0.05,
                             robot_bearing_noise: float = 0.02, horizon: float = float('inf')):
        """Execute student plan and store results in submission.

        Args:
            area_map: the area map to test against.
            gem_checklist: the list of gems to extract.
            max_distance: maximum distance per move.
            max_steering: maximum steering per move.
            robot_distance_noise: distance noise to set for Robot.
            robot_bearing_noise: bearing noise to set for Robot.
            horizon: distance of max measurement
        """
        self._reset()

        state = State(area_map,
                      gem_checklist,
                      max_distance,
                      max_steering,
                      measure_distance_noise=robot_distance_noise,
                      measure_bearing_noise=robot_bearing_noise,
                      horizon=horizon)

        if VERBOSE_FLAG:
            print('Initial State:')
            print(state)

        try:
            student_planner = gem_finder.GemExtractionPlanner(max_distance, max_steering)

            state_output = ''
            time_left = self.time_left.get()

            while len(state.collected_gems) < len(gem_checklist) and time_left:
                state_output += str(state)
                ret = student_planner.next_move(copy.deepcopy(state.gem_checklist),
                                                state.generate_measurements())
                if isinstance(ret, str):
                    action = ret
                else:
                    action, locs = ret

                state.update_according_to(action)
                if VERBOSE_FLAG:
                    print(state)

                if not self.time_left.empty():
                    time_left = self.time_left.get()

            if VERBOSE_FLAG:
                print('Final State:')
                print(state)

            self.submission_action_plan.put(state.collected_gems)
            if not time_left:
                error_message = ('Test aborted due to timeout. ' +
                f'Test was expected to finish in fewer than {TIME_LIMIT} second(s).')
                self.submission_error.put(error_message)

        except Exception:
            self.submission_error.put(traceback.format_exc())
            self.submission_action_plan.put([])


class State:
    """Current State.

    Args:
        area_map: the area map.
        gem_checklist:  the list of gems you need to collect
        max_distance:  the max distance the robot can travel in a single move.
        max_steering:  the max steering angle the robot can turn in a single move.
        measure_distance_noise: Noise of the distance measurement
        measure_bearing_noise: Noise of the bearing measurement
        horizon: distance of max measurement

    Attributes:
        gem_checklist:   the list of needed gems
        collected_gems:  gems successfully extracted.
        max_distance:   max distance the robot can travel in one move.
        max_steering:   the max steering angle the robot can turn in a single move.
        _start_position: location of initial robot placement
    """
    EXTRACTION_DISTANCE = 0.15
    WAIT_PENALTY = 0.1  # seconds

    def __init__(self, area_map: List[list], gem_checklist: List[str] = None, max_distance: float = 1.0,
                 max_steering: float = PI / 2. + 0.01, measure_distance_noise: float = 0.05,
                 measure_bearing_noise: float = 0.02, horizon: float = float('inf')):

        if gem_checklist is None:
            gem_checklist = []

        self.gem_checklist = list(gem_checklist)
        self.collected_gems = []
        self.max_distance = max_distance
        self.max_steering = max_steering
        self.gem_locs_on_map = []
        self.orig_gem_checklist = []
        self.horizon = horizon

        rows = len(area_map)
        cols = len(area_map[0])

        self._start_position = dict()

        # Now process the interior of the provided map
        for i in range(rows):
            for j in range(cols):
                this_square = area_map[i][j]
                x, y = float(j), -float(i)

                # Process gems
                if this_square in string.ascii_uppercase:
                    gem = {'id': int(hashlib.md5((str(this_square) + str(random.random())).encode('utf-8')).hexdigest(),
                                     16),
                           'x': x + 0.5,
                           'y': y - 0.5,
                           'type': this_square}

                    self.gem_locs_on_map.append(gem)
                    self.orig_gem_checklist.append(gem)

                # Process start
                elif this_square == '@':
                    self._start_position['x'] = x + 0.5
                    self._start_position['y'] = y - 0.5

        # initialize the robot at the start position and at a bearing pointing due east
        self.robot = robot.Robot(x=self._start_position['x'],
                                 y=self._start_position['y'],
                                 bearing=0.0,
                                 max_distance=self.max_distance,
                                 max_steering=self.max_steering,
                                 measure_distance_noise=measure_distance_noise,
                                 measure_bearing_noise=measure_bearing_noise)

    def generate_measurements(self, noise: bool = NOISE_FLAG):
        """Generate measurements of gems on map.

        Args:
            noise: Move with noise if True.
                Default: NOISE_FLAG

        Returns:
            Measurements to gems in the format:
                {'unique gem id':{'distance': 0.0, 'bearing': 0.0, 'type': 'A'}, ...}
        """
        measurements = dict()

        # process gems
        for location in self.gem_locs_on_map:
            distance, bearing = self.robot.measure_distance_and_bearing_to((location['x'], location['y']), noise=noise)
            if distance < self.horizon:
                measurements[location['id']] = {'distance': distance,
                                                'bearing': bearing,
                                                'type': location['type']}

        return measurements

    def update_according_to(self, action: str, noise: bool = NOISE_FLAG):
        """Update state according to action.

        Args:
            action: action to execute.
            noise: Move with noise if True.
                Default: NOISE_FLAG

        Raises:
            Exception: if improperly formatted action.
        """
        action = action.split()
        action_type = action[0]

        if action_type == 'move':
            steering, distance = action[1:]
            self._attempt_move(float(steering), float(distance), noise=noise)

        elif action_type == 'extract':
            try:
                gem_type = action[1]
                estimate_x = float(action[2])
                estimate_y = float(action[3])
                self._attempt_extraction(gem_type, estimate_x, estimate_y)
            except IndexError:
                # improper move format: kill test
                raise Exception(f"improperly formatted action: {' '.join(action)}")

        else:
            # improper move format: kill test
            raise Exception(f"improperly formatted action: {' '.join(action)}")

    def _attempt_move(self, steering: float, distance: float, noise: bool = NOISE_FLAG):
        """Attempt move action if valid.

        The robot may move between 0 and max_distance
        The robot may turn between -max_steering and +max_steering

        Illegal moves - the robot will not move
        - Moving a distance outside of [0,max_distance]
        - Steering angle outside [-max_steering, max_steering]

        Args:
            steering: Angle to turn before moving.
            distance: Distance to travel.

        Raises:
            ValueError: if improperly formatted move destination.
        """
        try:
            distance_ok = 0.0 <= distance <= self.max_distance
            steering_ok = (-self.max_steering) <= steering <= self.max_steering

            if noise:
                steering += random.gauss(0.0, NOISE_MOVE)
                distance += random.gauss(0.0, NOISE_MOVE)

            if distance_ok and steering_ok:
                self.robot.move(steering, distance, True)

        except ValueError:
            raise Exception(f"improperly formatted move command : {steering} {distance}")

    def _attempt_extraction(self, gem_type: str, estimate_x: float, estimate_y: float):
        """Attempt to extract a gem from the current x,y location.

        Extract gem if current location is within EXTRACTION_DISTANCE of specified gem_type.
        Otherwise, pause for WAIT_PENALTY
        """

        for gem_location in self.gem_locs_on_map:
            if gem_location['type'] == gem_type:
                robot_distance = robot.compute_distance((self.robot.x, self.robot.y),
                                                        (gem_location['x'], gem_location['y']))

                translated_x = estimate_x + self._start_position['x']
                translated_y = estimate_y + self._start_position['y']

                estimate_distance = robot.compute_distance((translated_x, translated_y),
                                                           (gem_location['x'], gem_location['y']))

                if robot_distance <= self.EXTRACTION_DISTANCE and estimate_distance <= self.EXTRACTION_DISTANCE:
                    self.collected_gems.append(gem_location)
                    self.gem_locs_on_map.remove(gem_location)
                    self.gem_checklist.remove(gem_location['type'])

                    return

        time.sleep(self.WAIT_PENALTY)

        if VERBOSE_FLAG:
            print(f"*** Location ({self.robot.x}, {self.robot.y}) does not contain a gem type <{gem_type}> within "
                  f"the extraction distance.")

    def __repr__(self):
        """Output state object as string.
        """
        output = '\n'
        output += 'Robot State:\n'
        output += f'\t x = {self.robot.x:6.2f}, y = {self.robot.y:6.2f}, hdg = {self.robot.bearing * 180. / PI:6.2f}\n'
        output += f'Gems Extracted: {self.collected_gems}\n'
        output += f'Remaining Gems Needed: {self.gem_checklist}\n'

        return output


class GemFinderTestResult(unittest.TestResult):

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super(GemFinderTestResult, self).__init__(stream, verbosity, descriptions)
        self.stream = stream
        self.credit = []
        self.results = []

    def stopTest(self, test):
        super(GemFinderTestResult, self).stopTest(test)
        try:
            self.credit.append(test.last_credit)
            self.results.append(test.last_result)
            self.stream.write(test.last_result + '\n')

        except AttributeError as exp:
            self.stream.write(str(exp))

    @property
    def avg_credit(self):
        try:
            return sum(self.credit) / len(self.credit)

        except Exception:
            return 0.0


class PartATestCase(unittest.TestCase):
    """Test PartA
    """
    params = {1: {'test_case': 1,
                  'area_map': ['...B..',
                               '......',
                               'A..@.C'],
                  'move': ['move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0'],
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'robot_tolerance': 0.1,
                  'landmark_tolerance': 0.15},
              2: {'test_case': 2,
                  'area_map': ['AB.DE..A',
                               'M......K',
                               'N......L',
                               'O@......',
                               'F.HIJ.TR'],
                  'move': ['move 0.0 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0'],
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'robot_tolerance': 0.1,
                  'landmark_tolerance': 0.15},
              3: {'test_case': 3,
                  'area_map': ['.QRHID.V',
                               '....G..X',
                               '.A..C..Y',
                               '...V.@.Z',
                               'O.B.FBCM'],
                  'move': ['move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0'],
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'robot_tolerance': 0.1,
                  'landmark_tolerance': 0.15},
              4: {'test_case': 4,
                  'area_map': ['........',
                               '...L....',
                               '..A.....',
                               '........',
                               '...D....',
                               '.@......',
                               '......M.'],
                  'move': ['move 1.570963 0.0',
                           'move 1.570963 0.0',
                           'move 0.785481 1.0',
                           'move 0.0 0.5',
                           'move 0.0 0.5',
                           'move 1.0 0.5',
                           'move 0.0 0.5'],
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'robot_tolerance': 0.1,
                  'landmark_tolerance': 0.15},
              5: {'test_case': 5,
                  'area_map': ['J.A.MNOC',
                               'D@..L..P',
                               'G.B....K',
                               'H.....Q.',
                               'I.E.R...'],
                  'move': ['move 0.0 1.0',
                           'move 0.0 1.0',
                           'move 1.570963 1.0',
                           'move 1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0'],
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'robot_tolerance': 0.2,
                  'landmark_tolerance': 0.15},
              6: {'test_case': 6,
                  'area_map': ['A......DEFG',
                               '..........J',
                               'Z..........',
                               'Y..........',
                               'X.@........',
                               'W.........N',
                               'STUV...OPQR'],
                  'move': ['move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.2 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.2 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move -1.570963 1.0',
                           'move 0.0 1.0',
                           'move 0.0 1.0'],
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'robot_tolerance': 0.2,
                  'landmark_tolerance': 0.20}}

    results_file = 'results_partA.txt'

    results = ['', 'PART A TEST CASE RESULTS']
    SCORE_TEMPLATE = "\n".join((
        "\nPart A Test Case {test_case} Results",
        "  Expected Location:\t{expected}",
        "  SLAM Location:\t{location}",
        "  Credit: {score:.0%}"
        "\n\n- - - - END OF TEST CASE - - - -\n",
    ))
    FAIL_TEMPLATE = "\n".join((
        "\nPart A Test Case {test_case} Results",
        "  Failed: {message}",
        "  Expected Location:\t{expected}",
        "  SLAM Location:\t{location}",
        "  Credit: 0.0"
        "\n\n- - - - END OF TEST CASE - - - -\n",
    ))

    credit = []

    def setUp(self):

        self.last_result = ''
        self.last_credit = 0.0

        if studentExc:
            self.last_result = str(studentExc)
            raise studentExc

    def run_with_params(self, params: Dict):
        """Run test case using desired parameters.
        Args:
            params: a dictionary of test parameters.
        """

        state = State(params['area_map'],
                      measure_distance_noise=params['robot_distance_noise'],
                      measure_bearing_noise=params['robot_bearing_noise'])
        robot_dist_error = float('inf')
        landmark_dist_errors = dict()

        state_beliefs = list()
        ground_truth = list()

        try:
            gem_finder_slam = gem_finder.SLAM()

            # calculate robot position error
            for move in params['move']:
                meas = state.generate_measurements()
                gem_finder_slam.process_measurements(meas)

                action = move.split()
                state.update_according_to(move)
                belief = gem_finder_slam.process_movement(float(action[1]), float(action[2]))
                truth = (state.robot.x - state._start_position['x'],
                         state.robot.y - state._start_position['y'])

                robot_dist_error = robot.compute_distance(belief, truth)

                if VERBOSE_FLAG:
                    print("Current Belief:", belief)
                    print("True Position:", truth)
                    print("Error:", robot_dist_error, "\n")

                state_beliefs.append(belief)
                ground_truth.append(truth)

            # calculate landmark errors
            for landmark in state.orig_gem_checklist:
                student_landmark_x, student_landmark_y = gem_finder_slam.get_coordinates_by_landmark_id(landmark['id'])

                translated_x = student_landmark_x + state._start_position['x']
                translated_y = student_landmark_y + state._start_position['y']

                landmark_dist_errors[landmark['id']] = robot.compute_distance((translated_x, translated_y),
                                                                              (landmark['x'], landmark['y']))

        except Exception as exc:
            self.last_result = self.FAIL_TEMPLATE.format(message=traceback.format_exc(),
                                                         expected="exception",
                                                         location="exception",
                                                         **params)
            self.last_credit = 0.0
            self.fail(str(exc))

        max_robot_score = 0.5
        max_landmark_score = 0.5

        robot_score = 0.0
        landmark_score = 0.0

        # calculate score for robot distance error
        if robot_dist_error < params['robot_tolerance']:
            robot_score += max_robot_score

        # calculate score for landmark distance errors
        missed_landmarks = list()
        for landmark_type, landmark_error in landmark_dist_errors.items():
            if landmark_error < params['landmark_tolerance']:
                landmark_score += max_landmark_score / len(state.orig_gem_checklist)
            else:
                missed_landmarks.append({'landmark': landmark_type,
                                         'error': landmark_error})

        robot_score = round(robot_score, 5)
        landmark_score = round(landmark_score, 5)

        total_score = robot_score + landmark_score

        if total_score >= 1.0:
            result = self.SCORE_TEMPLATE.format(expected=ground_truth,
                                                location=state_beliefs,
                                                score=total_score, **params)
        else:
            if robot_score < max_robot_score:
                robot_message = f"Robot location error {robot_dist_error} is greater than {params['robot_tolerance']}. "
            else:
                robot_message = ''

            if landmark_score < max_landmark_score:
                landmark_message = f"A landmark locations are greater than {params['landmark_tolerance']}"
            else:
                landmark_message = ''

            result = self.FAIL_TEMPLATE.format(message=robot_message + landmark_message,
                                               expected=ground_truth,
                                               location=state_beliefs, **params)

        self.last_result = result
        self.last_credit = total_score

        self.assertTrue(robot_score >= max_robot_score,
                        f"Robot location error {robot_dist_error} is greater than {params['robot_tolerance']}")

        self.assertTrue(landmark_score >= max_landmark_score,
                        f"A landmark location error is greater than {params['landmark_tolerance']}\n{missed_landmarks}")

    def test_case1(self):
        self.run_with_params(self.params[1])

    def test_case2(self):
        self.run_with_params(self.params[2])

    def test_case3(self):
        self.run_with_params(self.params[3])

    def test_case4(self):
        self.run_with_params(self.params[4])

    def test_case5(self):
        self.run_with_params(self.params[5])

    def test_case6(self):
        self.run_with_params(self.params[6])


class PartBTestCase(unittest.TestCase):
    """ Test PartB.
    """
    params = {1: {'test_case': 1,
                  'area_map': ['....',
                               '..@A',
                               '..B.'],
                  'needed_gems': list('A'),
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'max_distance': 2.0,
                  'max_steering': PI / 2. + 0.01,
                  'horizon': 1.5},
              2: {'test_case': 2,
                  'area_map': ['AXCZ.Z.S',
                               'M..Z..@.',
                               'O...V..R',
                               '.B..FGH.',
                               'T......E'],
                  'needed_gems': list('ABC'),
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'max_distance': 2.0,
                  'max_steering': PI / 2. + 0.01,
                  'horizon': 3.5},
              3: {'test_case': 3,
                  'area_map': ['A......B',
                               '.F..@...',
                               '.E......',
                               'C......D', ],
                  'needed_gems': list('ABCD'),
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'max_distance': 2.0,
                  'max_steering': PI / 2. + 0.01,
                  'horizon': 5.0},
              4: {'test_case': 4,
                  'area_map': ['O....A...',
                               '.@....C..',
                               '........M',
                               'PB......N'],
                  'needed_gems': list('ABC'),
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'max_distance': 2.0,
                  'max_steering': PI / 2. + 0.01,
                  'horizon': 5.0},
              5: {'test_case': 5,
                  'area_map': ['ABCDEF',
                               'GHIJKL',
                               'M.@PQR',
                               'S.UVWX',
                               '..YNOT'],
                  'needed_gems': list('ABCDEFGHIJKLMNOPQRSTUVWXY'),
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'max_distance': 2.0,
                  'max_steering': PI / 2. + 0.01,
                  'horizon': 2.5},
              6: {'test_case': 6,
                  'area_map': ['..TOP.S',
                               '......I',
                               '......D',
                               '...@..E',
                               '.......'],
                  'needed_gems': list('OPT'),
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'max_distance': 1.0,
                  'max_steering': PI / 2. + 0.01,
                  'horizon': 2.5},
              7: {'test_case': 7,
                  'area_map': ['...C.....O....',
                               '....R......O..',
                               '..N....A......',
                               'S...E.........',
                               '.......L...F..',
                               '..I....S..O...',
                               '....L.....A...',
                               '.....T...I..O.',
                               'N.......@.....',
                               'ZZZZZZZZZZZZZZ'],
                  'needed_gems': list('EFT'),
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'max_distance': 3.0,
                  'max_steering': PI / 2. + 0.01,
                  'horizon': 4.5},
              8: {'test_case': 8,
                  'area_map': ['ABCDEFG',
                               'QR.@.HI',
                               'JKLMNOP'],
                  'needed_gems': list('ACEGIK'),
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'max_distance': 2.0,
                  'max_steering': PI / 2. + 0.01,
                  'horizon': 2.5},
              9: {'test_case': 9,
                  'area_map': ['@A....F',
                               '.....MP',
                               'G....ZD'],
                  'needed_gems': list('ADM'),
                  'max_distance': 1.0,
                  'max_steering': PI / 2. + 0.01,
                  'robot_distance_noise': 0.05,
                  'robot_bearing_noise': 0.02,
                  'horizon': 4.0}}

    results_file = 'results_partB.txt'

    results = ['', 'PART B TEST CASE RESULTS']
    SCORE_TEMPLATE = "\n".join((
        "\nPart B Test Case {test_case} Results",
        "  Needed Gems:\t {needed_gems}",
        "  Collected Gems:{collected}",
        "  Credit: {score:.0%}"
        "\n\n- - - - END OF TEST CASE - - - -\n",
    ))
    FAIL_TEMPLATE = "\n".join((
        "\nPart B Test Case {test_case} Results",
        "  Failed: {message}",
        "  Needed Gems:\t {needed_gems}",
        "  Collected Gems:{collected}",
        "  Credit: {score:.0%}"
        "\n\n- - - - END OF TEST CASE - - - -\n",
    ))

    credit = []

    def setUp(self):
        """Initialize test setup.
        """
        self.last_result = ''
        self.last_credit = 0.0
        if studentExc:
            self.last_result = str(studentExc)
            raise studentExc
        self.student_submission = Submission()

    def check_results(self, params: Dict, error_message: str):

        extracted_gems = 0

        # Get number of gems collected
        if not self.student_submission.submission_action_plan.empty():
            extracted_gems = self.student_submission.submission_action_plan.get()

        extracted_gem_types = sorted([g['type'] for g in extracted_gems])
        extracted_gems_needed = sorted(list(set(extracted_gem_types).intersection(set(params['needed_gems']))))
        score = len(extracted_gems_needed) // float(len(params['needed_gems']))

        if not self.student_submission.submission_error.empty():
            error_message = self.student_submission.submission_error.get()
            result = self.FAIL_TEMPLATE.format(message=error_message, collected=extracted_gem_types, score=score, **params)
        else:
            result = self.SCORE_TEMPLATE.format(collected=extracted_gem_types, score=score, **params)

        return result, score, error_message, extracted_gems_needed

    def run_with_params(self, params: Dict):
        """Run test case using desired parameters.
        Args:
            params: a dictionary of test parameters.
        """
        sys.stdout.write(f'~ ~ ~ Start of test case # {params["test_case"]} ~ ~ ~\n\n')

        error_message = ''

        if DEBUGGING_SINGLE_PROCESS:
            try:
                self.student_submission.execute_student_plan(params['area_map'],
                                                             params['needed_gems'],
                                                             params['max_distance'],
                                                             params['max_steering'],
                                                             params['robot_distance_noise'],
                                                             params['robot_bearing_noise'],
                                                             params['horizon'])
            except Exception as exp:
                error_message = exp

            result, score, error_message, extracted_gems_needed = self.check_results(params, error_message)

        else:
            test_process = mproc.Process(target=self.student_submission.execute_student_plan,
                                         args=(params['area_map'],
                                               params['needed_gems'],
                                               params['max_distance'],
                                               params['max_steering'],
                                               params['robot_distance_noise'],
                                               params['robot_bearing_noise'],
                                               params['horizon']))

            try:
                test_process.start()
                test_process.join(TIME_LIMIT)
                self.student_submission.time_left.put(False)     # notify child process to finish
                test_process.join(1)                             # give child process a second to wrap things up
            except Exception as exp:
                error_message = exp

            # If test still running then terminate
            if test_process.is_alive():
                test_process.terminate()
                extracted_gem_types = []
                error_message = ('Test ended unexpectedly! No extracted gem data available')
                result = self.FAIL_TEMPLATE.format(message=error_message, collected=extracted_gem_types, **params)
                score = 0.0
                extracted_gems_needed = len(params['needed_gems'])
            else:
                result, score, error_message, extracted_gems_needed = self.check_results(params, error_message)
        self.last_result = result
        self.last_credit = score

        self.assertFalse(error_message, error_message)
        self.assertTrue(round(score, 7) == 1.0,
                        f"Only {len(extracted_gems_needed)} gems were extracted out of {len(params['needed_gems'])}")

    def test_case1(self):
        self.run_with_params(self.params[1])

    def test_case2(self):
        self.run_with_params(self.params[2])

    def test_case3(self):
        self.run_with_params(self.params[3])

    def test_case4(self):
        self.run_with_params(self.params[4])

    def test_case5(self):
        self.run_with_params(self.params[5])

    def test_case6(self):
        self.run_with_params(self.params[6])

    def test_case7(self):
        self.run_with_params(self.params[7])

    def test_case8(self):
        self.run_with_params(self.params[8])

    def test_case9(self):
        self.run_with_params(self.params[9])


def run_all(stream):
    suites = map(lambda case: unittest.TestSuite(unittest.TestLoader().loadTestsFromTestCase(case)),
                 [PartATestCase,
                  PartBTestCase])

    avgs = ()
    for suite in suites:
        result = GemFinderTestResult(stream=stream)
        suite.run(result)
        avgs += (result.avg_credit,)

    stream.write('part A score: %.02f\n' % (avgs[0] * 100))
    stream.write('part B score: %.02f\n' % (avgs[1] * 100))

    weights = (PART_A_CREDIT, PART_B_CREDIT)
    total_score = round(sum(avgs[i] * weights[i] for i in (0, 1)) * 100)
    stream.write('score: %.02f\n' % total_score)


# Only run all of the test automatically if this file was executed from the command line.
# Otherwise, let Nose/py.test do it's own thing with the test cases.
if __name__ == "__main__":
    import sys

    run_all(sys.stdout)
