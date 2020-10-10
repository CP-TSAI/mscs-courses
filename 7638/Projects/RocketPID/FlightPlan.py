from typing import Tuple, Optional


class TimeStep:
    """
    Expected velocity and height for this time and after.
    """
    def __init__(self, time: int, velocity: Optional[float] = None, height: Optional[float] = None,
                 velocity_variance: Optional[float] = None, height_variance: Optional[float] = None):
        self.time = time
        self.velocity = velocity
        self.velocity_variance = velocity_variance
        self.height_variance = height_variance
        self.height = height
        self.next_step = None
        self.prior_step = None


class FlightPlan:
    """
    Flight plan for rocket.
    """
    def __init__(self):
        self.head_step = TimeStep(0, 0.0, 0.0)

    def add_step(self, time: int, velocity: Optional[float] = None, height: Optional[float] = None,
                 velocity_variance: Optional[float] = None, height_variance: Optional[float] = None):
        """
        Add time to set velocity and height.
        Args:
            time: The time in flight
            velocity: The expected velocity at this time and after.
            height: The expected height at this time and after.
            velocity_variance: Amount velocity allowed to deviate, or none if no restrictions.
            height_variance: Amount height allowed to deviate, or none if no restrictions.
        """
        current_step = self.head_step
        while current_step.time != time:

            if current_step.time > time:
                added_step = TimeStep(time)

                added_step.prior_step = current_step.prior_step
                current_step.prior_step.next_step = added_step
                current_step.prior_step = added_step
                added_step.next_step = current_step

                current_step = added_step

            elif not current_step.next_step:
                added_step = TimeStep(time)

                added_step.prior_step = current_step
                current_step.next_step = added_step

            else:
                current_step = current_step.next_step

        current_step.velocity = velocity
        current_step.height = height
        current_step.velocity_variance = velocity_variance
        current_step.height_variance = height_variance

    def get_current_values(self, time: int) -> Tuple[float, float, float, float]:
        """
        Get the current value based on time.
        Args:
            time: The time for needed values.

        Returns:
            Expected velocity, allowed velocity variance, expected height, allowed height variance
        """
        current_step = self.head_step
        found_velocity = current_step.velocity
        found_velocity_variance = current_step.velocity_variance

        while current_step.next_step is not None:
            if current_step.velocity is not None:
                found_velocity = current_step.velocity
                found_velocity_variance = current_step.velocity_variance

            if current_step.next_step.time > time:
                break
            else:
                current_step = current_step.next_step

        if current_step.time == time:
            found_height = current_step.height
            found_height_variance = current_step.height_variance
        else:
            found_height = None
            found_height_variance = None

        return found_velocity, found_velocity_variance, found_height, found_height_variance

    def get_plan_length(self):
        current_step = self.head_step

        while current_step.next_step is not None:
            current_step = current_step.next_step

        return current_step.time

    def __repr__(self) -> str:
        """
        String representation of Flight Plan
        Returns:
            String of flight plan.
        """
        output = ''
        current_step = self.head_step
        while current_step is not None:
            output += f'Time: {current_step.time}, '
            output += f'target velocity: {current_step.velocity}, '
            output += f'velocity variance: {current_step.velocity_variance}'
            output += f'target height: {current_step.height}, '
            output += f'height variance: {current_step.height_variance}'
            current_step = current_step.next_step

        return output
