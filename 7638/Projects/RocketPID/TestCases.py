from FlightPlan import FlightPlan


class PumpTestCases:
    @classmethod
    def test_case1(cls) -> float:
        target_pressure = 100.0

        return target_pressure

    @classmethod
    def test_case2(cls) -> float:
        target_pressure = 50.0

        return target_pressure

    @classmethod
    def test_case3(cls) -> float:
        target_pressure = 97.3

        return target_pressure

    @classmethod
    def test_case4(cls) -> float:
        target_pressure = 78.4

        return target_pressure

    @classmethod
    def test_case5(cls) -> float:
        target_pressure = 84.9

        return target_pressure


class RocketTestCases:
    @classmethod
    def test_case1(cls):
        fuel = 35000
        flight_plan = FlightPlan()

        flight_plan.add_step(1, velocity=0.25)
        flight_plan.add_step(10, velocity=0.25, velocity_variance=0.01)
        flight_plan.add_step(100, velocity=0.5, height=25, height_variance=5.0)
        flight_plan.add_step(110, velocity=0.5, velocity_variance=0.01)
        flight_plan.add_step(150, velocity=-0.5)
        flight_plan.add_step(180, height=50, height_variance=5.0)
        flight_plan.add_step(355, velocity=-0.1)
        flight_plan.add_step(360, velocity=-0.1, velocity_variance=0.01)
        flight_plan.add_step(380, velocity=-0.1)
        flight_plan.add_step(400, velocity=0.0, height=0.0, velocity_variance=0.0, height_variance=0.0)

        return flight_plan, fuel


class BiPropellantTestCases:
    @classmethod
    def test_case1(cls):
        fuel = 35000
        oxidizer = 85000
        flight_plan = FlightPlan()

        flight_plan.add_step(1, velocity=0.25)
        flight_plan.add_step(10, velocity=0.25, velocity_variance=0.01)
        flight_plan.add_step(150, velocity=-0.25)
        flight_plan.add_step(280, velocity=-0.1)
        flight_plan.add_step(290, velocity=-0.1, velocity_variance=0.01)
        flight_plan.add_step(420, velocity=-0.1)
        flight_plan.add_step(445, velocity=0.0, height=0.0, velocity_variance=0.0, height_variance=0.0)

        return flight_plan, fuel, oxidizer
