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


import math

class DeliveryPlanner_PartA:

    """
    Required methods in this class are:
    
      plan_delivery(self, debug = False) which is stubbed out below.  
        You may not change the method signature as it will be called directly 
        by the autograder but you may modify the internals as needed.
    
      __init__: which is required to initialize the class.  Starter code is 
        provided that intializes class variables based on the definitions in 
        testing_suite_partA.py.  You may choose to use this starter code
        or modify and replace it based on your own solution
    
    The following methods are starter code you may use for part A.  
    However, they are not required and can be replaced with your
    own methods.
    
      _set_initial_state_from(self, warehouse): creates structures based on
          the warehouse and todo definitions and intializes the robot
          location in the warehouse
    
      _search(self, debug=False): Where the bulk of the A* search algorithm
          could reside.  It should find an optimal path from the robot
          location to a goal.  Hint:  you may want to structure this based
          on whether looking for a box or delivering a box.
  
    """

    ## Definitions taken from testing_suite_partA.py
    ORTHOGONAL_MOVE_COST = 2
    DIAGONAL_MOVE_COST = 3
    BOX_LIFT_COST = 4
    BOX_DOWN_COST = 2
    ILLEGAL_MOVE_PENALTY = 100

    def __init__(self, warehouse, todo):
        
        self.todo = todo
        self.boxes_delivered = []
        self.total_cost = 0
        self._set_initial_state_from(warehouse)

        self.delta = [[-1, 0 ], # north
                      [ 0,-1 ], # west
                      [ 1, 0 ], # south
                      [ 0, 1 ], # east
                      [-1,-1 ], # northwest (diag)
                      [-1, 1 ], # northeast (diag)
                      [ 1, 1 ], # southeast (diag)
                      [ 1,-1 ]] # southwest (diag)

        self.delta_directions = ["n","w","s","e","nw","ne","se","sw"]

        # Can use this for a visual debug
        self.delta_name = [ '^', '<', 'v', '>','\\','/','[',']' ]

        # Costs for each move
        self.delta_cost = [  self.ORTHOGONAL_MOVE_COST, 
                             self.ORTHOGONAL_MOVE_COST, 
                             self.ORTHOGONAL_MOVE_COST, 
                             self.ORTHOGONAL_MOVE_COST,
                             self.DIAGONAL_MOVE_COST,
                             self.DIAGONAL_MOVE_COST,
                             self.DIAGONAL_MOVE_COST,
                             self.DIAGONAL_MOVE_COST ]

    ## state parsing and initialization function from testing_suite_partA.py
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

    
    def _search(self, debug=False):
        """
        This method should be based on Udacity Quizes for A*, see Lesson 12, Section 10-12.
        The bulk of the search logic should reside here, should you choose to use this starter code.
        Please condition any printout on the debug flag provided in the argument.  
        You may change this function signature (i.e. add arguments) as 
        necessary, except for the debug argument which must remain with a default of False
        """

        # get a shortcut variable for the warehouse (note this is just a view no copying)
        grid = self.warehouse_state

        # Find and fill in the required moves per the instructions - example moves for test case 1
        moves = [ 'move w',
                  'move nw',
                  'lift 1',
                  'move se',
                  'down e',
                  'move ne',
                  'lift 2',
                  'down s']

  
        return moves 

  
    def plan_delivery(self, debug = False):
        """
        plan_delivery() is required and will be called by the autograder directly.  
        You may not change the function signature for it.
        Add logic here to find the moves.  You may use the starter code provided above
        in any way you choose, but please condition any printouts on the debug flag
        """

        # Find the moves - you may add arguments and change this logic but please leave
        # the debug flag in place and condition all printouts on it.

        # You may wish to break the task into one-way paths, like this:
        #
        #    moves_to_1   = self._search( ..., debug=debug )
        #    moves_from_1 = self._search( ..., debug=debug )
        #    moves_to_2   = self._search( ..., debug=debug )
        #    moves_from_2 = self._search( ..., debug=debug )
        #    moves        = moves_to_1 + moves_from_1 + moves_to_2 + moves_from_2
        #
        # If you use _search(), you may need to modify it to take some
        # additional arguments for starting location, goal location, and
        # whether to pick up or deliver a box.

        moves = self._search( debug=debug )

        if debug:
            for i in range( len(moves) ):
                print(moves[i])

        return moves


class DeliveryPlanner_PartB:
    """
    Required methods in this class are:

        plan_delivery(self, debug = False) which is stubbed out below.
        You may not change the method signature as it will be called directly
        by the autograder but you may modify the internals as needed.

        __init__: required to initialize the class.  Starter code is
        provided that intializes class variables based on the definitions in
        testing_suite_partB.py.  You may choose to use this starter code
        or modify and replace it based on your own solution

    The following methods are starter code you may use for part B.
    However, they are not required and can be replaced with your
    own methods.

        _set_initial_state_from(self, warehouse): creates structures based on
            the warehouse and todo definitions and intializes the robot
            location in the warehouse

        _find_policy(self, debug=False): Where the bulk of the A* search algorithm
            could reside.  It should find an optimal path from the robot
            location to a goal.  Hint:  you may want to structure this based
            on whether looking for a box or delivering a box.

    """

    # Definitions taken from testing_suite_partA.py
    ORTHOGONAL_MOVE_COST = 2
    DIAGONAL_MOVE_COST = 3
    BOX_LIFT_COST = 4
    BOX_DOWN_COST = 2
    ILLEGAL_MOVE_PENALTY = 100

    def __init__(self, warehouse, warehouse_cost, todo):

        self.todo = todo
        self.boxes_delivered = []
        self.total_cost = 0
        self._set_initial_state_from(warehouse)
        self.warehouse_cost = warehouse_cost

        self.delta = [[-1, 0],  # go up
                        [0, -1],  # go left
                        [1, 0],  # go down
                        [0, 1],  # go right
                        [-1, -1],  # up left (diag)
                        [-1, 1],  # up right (diag)
                        [1, 1],  # dn right (diag)
                        [1, -1]]  # dn left (diag)

        self.delta_directions = ["n", "w", "s", "e", "nw", "ne", "se", "sw"]

        # Use this for a visual debug
        self.delta_name = ['^', '<', 'v', '>', '\\', '/', '[', ']']

        # Costs for each move
        self.delta_cost = [self.ORTHOGONAL_MOVE_COST,
                        self.ORTHOGONAL_MOVE_COST,
                        self.ORTHOGONAL_MOVE_COST,
                        self.ORTHOGONAL_MOVE_COST,
                        self.DIAGONAL_MOVE_COST,
                        self.DIAGONAL_MOVE_COST,
                        self.DIAGONAL_MOVE_COST,
                        self.DIAGONAL_MOVE_COST]

    # state parsing and initialization function from testing_suite_partA.py
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


    def _find_policy(self, goal, pickup_box=True, debug=False):
        """
        This method should be based on Udacity Quizes for Dynamic Progamming,
        see Lesson 12, Section 14-20 and Problem Set 4, Question 5.  The bulk of
        the logic for finding the policy should reside here should you choose to
        use this starter code.  Please condition any printout on the debug flag
        provided in the argument. You may change this function signature
        (i.e. add arguments) as necessary, except for the debug argument which
        must remain with a default of False
        """

        ##############################################################################
        # insert code in this method if using the starter code we've provided
        ##############################################################################


        # get a shortcut variable for the warehouse (note this is just a view it does not make a copy)
        grid = self.warehouse_state
        grid_costs = self.warehouse_cost

        # You will need to fill in the algorithm here to find the policy
        # The following are what your algorithm should return for test case 1
        if pickup_box:
            # To box policy
            policy = [['B',  'lift 1','move w'],
                      ['lift 1', '-1', 'move nw'],
                      ['move n', 'move nw', 'move n']]

        else:
            # Deliver policy
            policy = [['move e', 'move se', 'move s'],
                      ['move ne', '-1', 'down s'],
                      ['move e', 'down e', 'move n']]

        return policy


    def plan_delivery(self, debug=False):
        """
        plan_delivery() is required and will be called by the autograder directly.  
        You may not change the function signature for it.
        Add logic here to find the policies:  First to the box from any grid position
        then to the dropzone, again from any grid position.  You may use the starter
        code provided above in any way you choose, but please condition any printouts
        on the debug flag
        """
        ###########################################################################
        # Following is an example of how one could structure the solution using
        # the starter code we've provided.
        ###########################################################################


        # Start by finding a policy to direct the robot to the box from any grid position
        # The last command(s) in this policy will be 'lift 1' (i.e. lift box 1)
        goal = self.boxes['1']
        to_box_policy = self._find_policy(goal, pickup_box=True, debug=debug)

        # Now that the robot has the box, transition to the deliver policy.  The
        # last command(s) in this policy will be 'down x' where x = the appropriate
        # direction to set the box into the dropzone
        goal = self.dropzone
        deliver_policy = self._find_policy(goal, pickup_box=False, debug=debug)

        if debug:
            print("\nTo Box Policy:")
            for i in range(len(to_box_policy)):
                print(to_box_policy[i])

            print("\nDeliver Policy:")
            for i in range(len(deliver_policy)):
                print(deliver_policy[i])

            print("\n\n")

        return (to_box_policy, deliver_policy)


if __name__ == "__main__":
    """ 
    You may execute this file to develop and test the search algorithm prior to running 
    the delivery planner in the testing suite.  Copy any test cases from the
    testing suite or make up your own.
    Run command:  python warehouse.py
    """

    # Test code in here will not be called by the autograder

    # Testing for Part A
    # testcase 1
    warehouse = ['1#2',
                '.#.',
                '..@']

    todo =  ['1','2'] 

    partA = DeliveryPlanner_PartA(warehouse, todo)
    partA.plan_delivery(debug=True)

    # Testing for Part B
    # testcase 1
    warehouse = ['1..',
                 '.#.',
                 '..@']

    warehouse_cost = [[0, 5, 2],
                      [10, math.inf, 2],
                      [2, 10, 2]]

    todo = ['1']

    partB = DeliveryPlanner_PartB(warehouse, warehouse_cost, todo)
    partB.plan_delivery(debug=True)





