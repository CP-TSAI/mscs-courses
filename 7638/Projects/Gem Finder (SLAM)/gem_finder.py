"""
 === Introduction ===

   The assignment is broken up into two parts.
   Part A:
        Create a SLAM implementation to process a series of landmark (gem) measurements and movement updates.
        The movements are defined for you so there are no decisions for you to make, you simply process the movements
        given to you.
        Hint: A planner with an unknown number of motions works well with an online version of SLAM.
    Part B:
        Here you will create the action planner for the robot.  The returned actions will be executed with the goal
        being to navigate to and extract a list of needed gems from the environment.  You will earn points by
        successfully extracting the list of gems from the environment. Extraction can only happen if within the
        minimum distance of 0.15.
        Example Actions (more explanation below):
            'move 3.14 1'
            'extract B 1.5 -0.2'
    Note: All of your estimates should be given relative to your robot's starting location.
    Details:
    - Start position
      - The robot will land at an unknown location on the map, however, you can represent this starting location
        as (0,0), so all future robot location estimates will be relative to this starting location.
    - Measurements
      - Measurements will come from gems located throughout the terrain.
        * The format is {'landmark id':{'distance':0.0, 'bearing':0.0, 'type':'D'}, ...}
      - Only gems that have not been collected and are within the horizon distance will return measurements.
    - Movements
      - Action: 'move 1.570963 1.0'
        * The robot will turn counterclockwise 90 degrees and then move 1.0
      - Movements are stochastic due to, well, it being a robot.
      - If max distance or steering is exceeded, the robot will not move.
    - Needed Gems
      - Provided as list of gem types: ['A', 'B', 'L', ...]
      - Although the gem names aren't real, as a convenience there are 26 total names, each represented by an
        upper case letter of the alphabet (ABC...).
      - Action: 'extract'
        * The robot will attempt to extract a specified gem from the current location..
      - When a gem is extracted from the terrain, it no longer exists in the terrain, and thus won't return a
        measurement.
      - The robot must be with 0.15 distance to successfully extract a gem.
      - There may be gems in the environment which are not required to be extracted.
    The robot will always execute a measurement first, followed by an action.
    The robot will have a time limit of 5 seconds to find and extract all of the needed gems.
"""

from typing import Dict, List


class SLAM:
    """Create a basic SLAM module.
    """

    def __init__(self):
        """Initialize SLAM components here.
        """
        # TODO

    # Provided Functions
    def get_coordinates_by_landmark_id(self, landmark_id: str):
        """
        Retrieves the x, y locations for a given landmark

        Args:
            landmark_id: The id for a processed landmark

        Returns:
            the coordinates relative to the robots frame with an initial position of 0.0
        """
        # TODO:

        return 0.0, 0.0

    def process_measurements(self, measurements: Dict):
        """
        Process a new series of measurements.

        Args:
            measurements: Collection of measurements
                in the format {'landmark id':{'distance':0.0, 'bearing':0.0, 'type':'B'}, ...}

        Returns:
            x, y: current belief in location of the robot
        """
        # TODO:

        return 0.0, 0.0

    def process_movement(self, steering: float, distance: float):
        """
        Process a new movement.

        Args:
            steering: amount to turn
            distance: distance to move

        Returns:
            x, y: current belief in location of the robot
        """
        # TODO:

        return 0.0, 0.0


class GemExtractionPlanner:
    """
    Create a planner to navigate the robot to reach and extract all the needed gems from an unknown start position.
    """

    def __init__(self, max_distance: float, max_steering: float):
        """
        Initialize your planner here.

        Args:
            max_distance: the max distance the robot can travel in a single move.
            max_steering: the max steering angle the robot can turn in a single move.
        """
        # TODO

    def next_move(self, needed_gems: List[str], measurements: Dict):
        """Next move based on the current set of measurements.
        Args:
            needed_gems: List of gems remaining which still need to be found and extracted.
            measurements: Collection of measurements from gems in the area.
                                {'landmark id': {
                                                    'distance': 0.0,
                                                    'bearing' : 0.0,
                                                    'type'    :'B'
                                                },
                                ...}
        Return: action: str, points_to_plot: dict [optional]
            action (str): next command to execute on the robot.
                allowed:
                    'move 1.570963 1.0'  - Turn left 90 degrees and move 1.0 distance.
                    'extract B 1.5 -0.2' - [Part B] Attempt to extract a gem of type D from your current location.
                                           This will succeed if the specified gem is within the minimum sample distance.
            points_to_plot (dict): point estimates (x,y) to visualize if using the visualization tool [optional]
                            'self' represents the robot estimated position
                            <landmark_id> represents the estimated position for a certain landmark
                format:
                    {
                        'self': (x, y),
                        '<landmark_id_1>': (x1, y1),
                        '<landmark_id_2>': (x2, y2),
                        ....
                    }
        """
        # TODO

        return '', {}
