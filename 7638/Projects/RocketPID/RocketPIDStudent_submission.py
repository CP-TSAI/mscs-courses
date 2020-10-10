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
from typing import Dict, Tuple


def pressure_pd_solution(delta_t: float, current_pressure: float, target_pressure: float,
                         data: Dict) -> Tuple[float, Dict]:
    """
    Student solution to maintain LOX pressure to the turbopump at a level of 100.

    Args:
        delta_t: Time step length.
        current_pressure: Current pressure level of the turbopump.
        target_pressure: Target pressure level of the turbopump.
        data: Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0
    """
    # TODO: implement PD solution here

    return 0.0, data


def rocket_pid_solution(delta_t: float, current_velocity: float, optimal_velocity: float,
                        data: Dict) -> Tuple[float, Dict]:
    """
    Student solution for maintaining rocket throttle through the launch based on an optimal flight path

    Args:
        delta_t: Time step length.
        current_velocity: Current velocity of rocket.
        optimal_velocity: Optimal velocity of rocket.
        data: Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorI': Integral error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0

    Returns:
        Throttle to set, data dictionary to be passed through run.
    """
    # TODO: implement Rocket PID solution here

    return 0.0, data


def bipropellant_pid_solution(delta_t: float, current_velocity: float, optimal_velocity: float,
                              data: Dict) -> Tuple[float, float, Dict]:
    """
    Student solution for maintaining fuel and oxidizer throttles through the launch based on an optimal flight path

    Args:
        delta_t: Time step length.
        current_velocity: Current velocity of rocket.
        optimal_velocity: Optimal velocity of rocket.
        data: Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorI': Integral error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0

    Returns:
        Fuel Throttle, Oxidizer Throttle to set, data dictionary to be passed through run.
    """
    # TODO: implement Bi-propellant PID solution here

    return 0.0, 0.0, data
