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
import multiprocessing as mproc
import traceback
import string
import sys
import copy
import io

try:
    from warehouse import DeliveryPlanner_PartA
    studentExc = None
except Exception as e:
    studentExc = e
    
########################################################################
# For debugging this flag can be set to True to print state 
# which could result in a timeout
########################################################################
VERBOSE_FLAG = False

########################################################################
# For debugging set the time limit to a big number (like 600 or more)
########################################################################
TIME_LIMIT = 5  # seconds

########################################################################
# If your debugger does not handle multiprocess debugging very easily
# then when debugging set the following flag true.
########################################################################
DEBUGGING_SINGLE_PROCESS = False

def truncate_output( s, max_len = 2000 ):
    if len(s) > max_len:
        return s[:max_len-70] + "\n***************** OUTPUT TRUNCATED DUE TO EXCESSIVE LENGTH!**************\n"
    else:
        return s

class Submission:
    """Student Submission.

    Attributes:
        submission_score(Queue): Student score of last executed plan.
        submission_error(Queue): Error messages generated during last executed plan.
    """
    def __init__(self, fout=None):

        if DEBUGGING_SINGLE_PROCESS:
            import queue
            self.submission_score = queue.Queue(1)
            self.submission_error = queue.Queue(1)
            self.logmsgs = queue.Queue(1)
        else:
            self.submission_score = mproc.Manager().Queue(1)
            self.submission_error = mproc.Manager().Queue(1)
            self.logmsgs = mproc.Manager().Queue(1)

        self.fout = io.StringIO()

    def log(self, s):
        self.fout.write(s + '\n')

    def _reset(self):
        """Reset submission results.
        """
        while not self.submission_score.empty():
            self.submission_score.get()

        while not self.submission_error.empty():
            self.submission_error.get()

        while not self.logmsgs.empty():
            self.logmsgs.get()
            
    def execute_student_plan(self, warehouse, boxes_todo):
        """Execute student plan and store results in submission.

        Args:
            warehouse(list(list)): the warehouse map to test against.
            boxes_todo(list): the order of boxes to deliver.
        """
        self._reset()

        state = State(warehouse)

        try:
            student_planner = DeliveryPlanner_PartA(copy.deepcopy(warehouse), copy.deepcopy(boxes_todo))
            action_list = student_planner.plan_delivery()

            num_delivered = 0
            next_box_to_deliver = boxes_todo[num_delivered]

            for action in action_list:
                if VERBOSE_FLAG:
                    state.print_to_console( self.fout )
                    #state.print_to_console( )

                state.update_according_to(action)

                # check if new box has been delivered
                delivered = state.get_boxes_delivered()
                if len(delivered) > num_delivered:
                    last_box_delivered = delivered[-1]
                    if last_box_delivered == next_box_to_deliver:
                        num_delivered += 1
                        if num_delivered < len(boxes_todo):
                            next_box_to_deliver = boxes_todo[num_delivered]
                        else:
                            # all boxes delivered: end test
                            break
                    else:
                        # wrong box delivered: kill test
                        raise Exception('wrong box delivered: {} instead of {}'.format(last_box_delivered,
                                                                                       next_box_to_deliver))

            if VERBOSE_FLAG:
                # print final state
                self.log('\n\n')
                self.log('Final State: ')
                state.print_to_console( self.fout )

            #Note, to receive credit, you must have deliverd all boxes.
            if num_delivered == len(boxes_todo):
               self.submission_score.put(state.get_total_cost())
            else:
               self.submission_score.put(float('inf')) 

        except:
            self.submission_error.put(traceback.format_exc())
            self.submission_score.put(float('inf'))

        self.logmsgs.put( truncate_output( self.fout.getvalue() ) )

class State:
    """Current State.

    Args:
        warehouse(list(list)): the warehouse map.

    Attributes:
        boxes_delivered(list): the boxes successfully delivered to dropzone.
        total_cost(int): the total cost of all moves executed.
        warehouse_state(list(list): the current warehouse state.
        dropzone(tuple(int, int)): the location of the dropzone.
        boxes(list): the location of the boxes.
        robot_position(tuple): the current location of the robot.
        box_held(str): ID of current box held.
    """
    ORTHOGONAL_MOVE_COST = 2
    DIAGONAL_MOVE_COST = 3
    BOX_LIFT_COST = 4
    BOX_DOWN_COST = 2
    ILLEGAL_MOVE_PENALTY = 100
    MOVE_DIRECTIONS = {"n":(-1,0),"ne":(-1,1),"e":(0,1),"se":(1,1),
                    "s":(1,0),"sw":(1,-1),"w":(0,-1),"nw":(-1,-1)}

    def __init__(self, warehouse):
        self.boxes_delivered = []
        self.total_cost = 0
        self._set_initial_state_from(warehouse)

    def _set_initial_state_from(self, warehouse):
        """Set initial state.

        Args:
            warehouse(list(list)): the warehouse map.
        """
        rows = len(warehouse)
        cols = len(warehouse[0])

        self.warehouse_state = [[None for j in range(cols)] for i in range(rows)]
        self.dropzone = None
        self.boxes = dict()

        for i in range(rows):
            for j in range(cols):
                this_square = warehouse[i][j]

                if this_square == '.':
                    self.warehouse_state[i][j] = '.'

                elif this_square == '#':
                    self.warehouse_state[i][j] = '#'

                elif this_square == '@':
                    self.warehouse_state[i][j] = '*'
                    self.dropzone = (i, j)

                else:  # a box
                    box_id = this_square
                    self.warehouse_state[i][j] = box_id
                    self.boxes[box_id] = (i, j)

        self.robot_position = self.dropzone
        self.box_held = None

    def update_according_to(self, action):
        """Update state according to action.

        Args:
            action(str): action to execute.

        Raises:
            Exception: if improperly formatted action.
        """

        # provide a bit more checking on the actions here
        if not isinstance(action,str):
            raise Exception('action is not a string: {}'.format(''.join(action)))

        # what type of move is it?
        action = action.split()
        action_type = action[0]

        if action_type == 'move':
            direction = action[1]
            self._attempt_move(direction)

        elif action_type == 'lift':
            box = action[1]
            self._attempt_lift(box)

        elif action_type == 'down':
            direction = action[1]
            self._attempt_down(direction)

        else:
            # improper move format: kill test
            raise Exception("action type must be 'move','lift' or 'down': {}".format(''.join(action)))


    def _attempt_move(self, direction):
        """Attempt move action if valid.

        The robot may not move outside the warehouse.
        The warehouse does not "wrap" around.
        Two spaces are considered adjacent if they share an edge or a corner.

        The robot may move horizontally or vertically at a cost of 2 per move.
        The robot may move diagonally at a cost of 3 per move.
        Illegal move (100 cost):
            attempting to move to a nonadjacent, nonexistent, or occupied space

        Args:
            direction: direction in which to move to adjacent square
                ("n","ne","e","se","s","sw","w","nw")
            

        Raises:
            ValueError: if improperly formatted move destination.
            IndexError: if move is outside of warehouse.
        """
        try:
              
            destination = self.MOVE_DIRECTIONS[direction][0] + self.robot_position[0], \
                            self.MOVE_DIRECTIONS[direction][1] + self.robot_position[1]

            destination_is_adjacent = self._are_adjacent(self.robot_position, destination)
            destination_is_traversable = self._is_traversable(destination)

            is_legal_move = destination_is_adjacent and destination_is_traversable

            if is_legal_move:
                self._move_robot_to(destination)
            else:
                self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

        except ValueError:
            raise Exception("move direction must be 'n','ne','e','se','s','sw','w','nw' your move is: {}".format(direction))
        except IndexError:  # (row, col) not in warehouse
            self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

    def _attempt_lift(self, box_id):
        """Attempt lift action if valid.

        The robot may pick up a box that is in an adjacent square.
        The cost to pick up a box is 4, regardless of the direction the box is relative to the robot.
        While holding a box, the robot may not pick up another box.
        Illegal moves (100 cost):
            attempting to pick up a nonadjacent or nonexistent box
            attempting to pick up a box while holding one already

        Args:
            box_id(str): the id of the box to lift.

        Raises:
            KeyError: if invalid box id.
        """
        try:
            box_position = self.boxes[box_id]

            box_is_adjacent = self._are_adjacent(self.robot_position, box_position)
            robot_has_box = self._robot_has_box()

            is_legal_lift = box_is_adjacent and (not robot_has_box)
            if is_legal_lift:
                self._lift_box(box_id)
            else:
                self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

        except KeyError:
            self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

    def _attempt_down(self, direction):
        """Attempt down action if valid.

        The robot may put a box down on an adjacent empty space ('.') or the dropzone ('@') at a cost
            of 2 (regardless of the direction in which the robot puts down the box).
        Illegal moves (100 cost):
            attempting to put down a box on a nonadjacent, nonexistent, or occupied space
            attempting to put down a box while not holding one

        Args:
            direction: direction to adjacent square in which to set box down 
                  ("n","ne","e","se","s","sw","w","nw")

        Raises:
            ValueError: if improperly formatted down destination.
            IndexError: if down location is outside of warehouse.
        """
        try:

            destination = self.MOVE_DIRECTIONS[direction][0] + self.robot_position[0], \
                          self.MOVE_DIRECTIONS[direction][1] + self.robot_position[1]

            destination_is_adjacent = self._are_adjacent(self.robot_position, destination)
            destination_is_traversable = self._is_traversable(destination)
            robot_has_box = self._robot_has_box()

            is_legal_down = destination_is_adjacent and destination_is_traversable and robot_has_box
            if is_legal_down:
                self._down_box(destination)
            else:
                self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

        except ValueError:
            raise Exception("down direction must be 'n','ne','e','se','s','sw','w','nw' your move is: {}".format(direction))
        except IndexError:  # (row, col) not in warehouse
            self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

    def _increase_total_cost_by(self, amount):
        """Increase total move cost.

        Args:
            amount(int): amount to increase cost by.
        """
        self.total_cost += amount

    def _is_within_warehouse(self, coordinates):
        """Check if coordinates are within warehouse.

        Args:
            coordinates(tuple(int, int)): coordinates to test.

        Returns:
            True if within warehouse.
        """
        i, j = coordinates
        rows = len(self.warehouse_state)
        cols = len(self.warehouse_state[0])

        return (0 <= i < rows) and (0 <= j < cols)

    def _are_adjacent(self, coordinates1, coordinates2):
        """Verify if coordinates are adjacent.

        Args:
            coordinates1(tuple(int, int)): first coordinate.
            coordinates2(tuple(int, int)): second coordinate.

        Returns:
            True if adjacent in all directions.
        """
        return (self._are_horizontally_adjacent(coordinates1, coordinates2) or
                self._are_vertically_adjacent(coordinates1, coordinates2) or
                self._are_diagonally_adjacent(coordinates1, coordinates2)
                )

    @staticmethod
    def _are_horizontally_adjacent(coordinates1, coordinates2):
        """Verify if coordinates are horizontally adjacent.

        Args:
            coordinates1(tuple(int, int)): first coordinate.
            coordinates2(tuple(int, int)): second coordinate.

        Returns:
            True if horizontally adjacent.
        """
        row1, col1 = coordinates1
        row2, col2 = coordinates2

        return (row1 == row2) and (abs(col1 - col2) == 1)

    @staticmethod
    def _are_vertically_adjacent(coordinates1, coordinates2):
        """Verify if coordinates are vertically adjacent.

        Args:
            coordinates1(tuple(int, int)): first coordinate.
            coordinates2(tuple(int, int)): second coordinate.

        Returns:
            True if vertically adjacent.
        """
        row1, col1 = coordinates1
        row2, col2 = coordinates2

        return (abs(row1 - row2) == 1) and (col1 == col2)

    @staticmethod
    def _are_diagonally_adjacent(coordinates1, coordinates2):
        """Verify if coordinates are diagonally adjacent.

        Args:
            coordinates1(tuple(int, int)): first coordinate.
            coordinates2(tuple(int, int)): second coordinate.

        Returns:
            True if diagonally adjacent.
        """
        row1, col1 = coordinates1
        row2, col2 = coordinates2

        return (abs(row1 - row2) == 1) and (abs(col1 - col2) == 1)

    def _is_traversable(self, coordinates):
        """Verify if space is traversable.

        Args:
            coordinates(tuple(int, int)): coordinate to check.

        Return:
            True if traversable.
        """
        is_wall = self._is_wall(coordinates)
        has_box = self._space_contains_box(coordinates)

        return (not is_wall) and (not has_box)

    def _is_wall(self, coordinates):
        """Verify if space is wall.

        Args:
            coordinates(tuple(int, int)): coordinate to check.

        Return:
            True if wall.
        """
        i, j = coordinates

        return self.warehouse_state[i][j] == '#'

    def _space_contains_box(self, coordinates):
        """Verify if space contains box.

        Args:
            coordinates(tuple(int, int)): coordinate to check.

        Return:
            True if space contains box.
        """
        i, j = coordinates

        return self.warehouse_state[i][j] in (string.ascii_letters + string.digits)

    def _robot_has_box(self):
        """Verify if robot has box.

        Returns:
            True if box is being held.
        """
        return self.box_held is not None

    def _move_robot_to(self, destination):
        """Execute move.

        Args:
            destination(tuple(int, int)): location to set box down at.
        """
        old_position = self.robot_position
        self.robot_position = destination

        i1, j1 = old_position
        if self.dropzone == old_position:
            self.warehouse_state[i1][j1] = '@'
        else:
            self.warehouse_state[i1][j1] = '.'

        i2, j2 = destination
        self.warehouse_state[i2][j2] = '*'

        if self._are_diagonally_adjacent(old_position, destination):
            self._increase_total_cost_by(self.DIAGONAL_MOVE_COST)
        else:
            self._increase_total_cost_by(self.ORTHOGONAL_MOVE_COST)

    def _lift_box(self, box_id):
        """Execute lift box.

        Args:
            box_id(str): the id of the box to lift.
        """
        i, j = self.boxes[box_id]
        self.warehouse_state[i][j] = '.'

        self.boxes.pop(box_id)

        self.box_held = box_id

        self._increase_total_cost_by(self.BOX_LIFT_COST)

    def _down_box(self, destination):
        """Execute box down.

        Args:
            destination(tuple(int, int)): location to set box down at.
        """
        # - If a box is placed on the '@' space, it is considered delivered and is removed from the ware-
        #   house.
        i, j = destination

        if self.warehouse_state[i][j] == '.':
            self.warehouse_state[i][j] = self.box_held
            self.boxes[self.box_held] = (i, j)
        else:
            self._deliver_box(self.box_held)

        self.box_held = None
        self._increase_total_cost_by(self.BOX_DOWN_COST)

    def _deliver_box(self, box_id):
        """Mark box delivered.

        Args:
            box_id(str): id of box to mark delivered.
        """
        self.boxes_delivered.append(box_id)

    def get_boxes_delivered(self):
        """Get list of boxes delivered.

        Returns:
            List of boxes delivered.
        """
        return self.boxes_delivered

    def get_total_cost(self):
        """Get current total cost.

        Returns:
            Total cost of all executed moves.
        """
        return self.total_cost

    def print_to_console(self, fout=None):
        """Print current state to console.
        """
        my_fout = fout or sys.stdout
        my_fout.write("\n")
        for row in self.warehouse_state:
            my_fout.write( ''.join(str(row)) + '\n' )
        my_fout.write( 'total cost: %.02f\n' % self.total_cost )
        my_fout.write( 'box held: %s\n' % str(self.box_held) )
        my_fout.write( 'delivered: %s\n' % str(self.boxes_delivered) )
        my_fout.write( '\n' )


class PartATestCase(unittest.TestCase):
    """ Test Part A.
    """

    results = ['', 'PART A TEST CASE RESULTS']
    SCORE_TEMPLATE = "\n".join((
        "\n-----------",
        "Test Case {test_case}",
        "Output: {output}",
        "cost: {cost:.2f}  (expected min {min_cost:.2f})",
        "credit: {score:.2f}"
    ))
    FAIL_TEMPLATE = "\n".join((
        "\n-----------",
        "Test Case {test_case}",
        "Output: {output}",
        "Failed: {message}",
        "credit: 0"
    ))

    credit = []
    totalCredit = 0

    fout = None

    @classmethod
    def _log(cls, s):
        (cls.fout or sys.stdout).write( s + '\n')

    def setUp(self):
        """Initialize test setup.
        """
        if studentExc:
            self.credit.append( 0.0 )
            self.results.append( "exception on import: %s" % str(studentExc) )
            raise studentExc

        self.student_submission = Submission( fout = self.__class__.fout )

    def tearDown(self):
        self.__class__.totalCredit = sum(self.__class__.credit)

    @classmethod
    def tearDownClass(cls):
        """Save student results at conclusion of test.
        """
        # Prints results after all tests complete
        for line in cls.results:
            cls._log(line)
        cls._log("\n-----------")
        cls._log('\nTotal Credit: {:.2f}'.format(cls.totalCredit))


    def check_results(self, params):

        error_message = ''
        cost = float('inf')
        score = 0.0
        logmsg = ''

        if not self.student_submission.logmsgs.empty():
            logmsg = self.student_submission.logmsgs.get()

        if not self.student_submission.submission_score.empty():
            cost = self.student_submission.submission_score.get()

        score = float(params['min_cost']) / float(cost)

        if not self.student_submission.submission_error.empty():
            error_message = self.student_submission.submission_error.get()
            self.results.append(self.FAIL_TEMPLATE.format(message=error_message, output = logmsg, **params))

        else:
            self.results.append(self.SCORE_TEMPLATE.format(cost=cost, score=score, output = logmsg, **params))

        self.credit.append(score)

        self._log('test case {} credit: {}'.format(params['test_case'], score))
        if error_message:
            self._log('{}'.format(error_message))

        self.assertFalse(error_message, error_message)

    def run_with_params(self, params):
        """Run test case using desired parameters.

        Args:
            params(dict): a dictionary of test parameters.
        """

        if DEBUGGING_SINGLE_PROCESS:
            self.student_submission.execute_student_plan(params['warehouse'], params['todo'])
        else:
            test_process = mproc.Process(target=self.student_submission.execute_student_plan, args=(params['warehouse'],
                                                                                                params['todo']))

        if DEBUGGING_SINGLE_PROCESS :

            # Note: no TIMEOUT is checked in this case so that debugging isn't 
            # inadvertently stopped

            self.check_results( params )

        else:

            logmsg = ''

            try:
                test_process.start()
                test_process.join(TIME_LIMIT)
            except Exception as exp:
                error_message = exp

            if test_process.is_alive():
                test_process.terminate()
                error_message = ('Test aborted due to timeout. ' +
                                'Test was expected to finish in fewer than {} second(s).'.format(TIME_LIMIT))
                if not self.student_submission.logmsgs.empty():
                    logmsg = self.student_submission.logmsgs.get()
                self.results.append(self.FAIL_TEMPLATE.format(message=error_message, output = logmsg, **params))

            else:

                self.check_results( params )
   
    def test_case1(self):
        params = {'test_case': 1,
                  'warehouse': ['1#2',
                                '.#.',
                                '..@'],
                  'todo': ['1', '2'],
                  'min_cost': 23}

        self.run_with_params(params)

    # Notice that we have included several extra test cases below.
    # You can uncomment one or more of these for extra tests.
    #
    def test_case2(self):
        params = {'test_case': 2,
                  'warehouse': ['@....1'],
                  'todo': ['1'],
                  'min_cost': 20}

        self.run_with_params(params)

    def test_case3(self):
        params = {'test_case': 3,
                  'warehouse': ['1.#@#.4',
                                '2#.#.#3'],
                  'todo': ['1', '2', '3', '4'],
                  'min_cost': 57}

        self.run_with_params(params)

    # *** CREDIT TO: Kowsalya Subramanian for adding this test case
    def test_case4(self):
        params = {'test_case': 4,
                  'warehouse': ['3#@',
                                '2#.',
                                '1..'],
                  'todo': ['1', '2', '3'],
                  'min_cost': 44}

        self.run_with_params(params)

    # *** CREDIT TO: Gideon Rossman for adding this test case
    def test_case5(self):
        params = {'test_case': 5,
                  'warehouse': ['..1.',
                                '..@.',
                                '....',
                                '2...'],
                  'todo': ['1', '2'],
                  'min_cost': 19}

        self.run_with_params(params)

    # *** CREDIT TO: venkatasatyanarayana kamisetti for adding this test case
    def test_case6(self):
        params = {'test_case': 6,
                  'warehouse': ['1..',
                                '...',
                                '@.2'],
                  'todo': ['1', '2'],
                  'min_cost': 16}

        self.run_with_params(params)

    # # *** CREDIT TO: Dana Johnson for adding this test case
    def test_case7(self):
        params = {'test_case': 7,
                  'warehouse': ['#J######',
                                '#I#2345#',
                                '#H#1##6#',
                                '#G#0@#7#',
                                '#F####8#',
                                '#EDCBA9#',
                                '########'],
                  'todo': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                           'I', 'J'],
                  'min_cost': 636.0}

        self.run_with_params(params)

    # *** CREDIT TO: Dana Johnson for adding this test case
    def test_case8(self):
        params = {'test_case': 8,
                  'warehouse': ['#######2',
                                '#......1',
                                '#@......'],
                  'todo': ['1', '2'],
                  'min_cost': 47.0}

        self.run_with_params(params)

    def test_case9(self):
        params = {'test_case': 9,
                  'warehouse': ['..#1..',
                                '......',
                                '..####',
                                '..#2.#',
                                '.....@'],
                  'todo': ['1', '2'],
                  'min_cost': 43.0}

        self.run_with_params(params)

    # Test Case 10
    def test_case10(self):
        params = {'test_case': 10,
                  'warehouse': ['..#1..',
                                '#....#',
                                '..##.#',
                                '..#2.#',
                                '#....@'],
                  'todo': ['1', '2'],
                  'min_cost': 30.0}

        self.run_with_params(params)


# Only run all of the test automatically if this file was executed from the command line.
# Otherwise, let Nose/py.test do it's own thing with the test cases.
if __name__ == "__main__":
    PartATestCase.fout = sys.stdout
    unittest.main()
