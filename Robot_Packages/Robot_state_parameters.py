from dataclasses import dataclass


@dataclass
class RobotParameters:
    class Battery:
        bat_max_volt: float  # example -> 36.00 is MAX (V)
        bat_min_volt: float  # example -> 32.00 is MIN (V)
        bat_curr_volt: float  # example  -> 34.64 is current (V)

        bat_max_capacity: float  # example -> 6 Ah is MAX (Ah)
        bat_min_capacity: float  # example -> 0 Ah is MIN (Ah)
        bat_curr_capacity: float  # example -> 3.65 Ah is current (Ah)

        bat_percent_value: float  # example -> percents is 34 (%)

        class ConfigBattery:
            parallel_connection: int
            serial_connection: int

    class Sizes:
        lenght: float
        width: float
        height: float

    class MotorWheels:
        wheel_radius: float
        dist_between_wheels: float
        max_rpm: int
        min_rpm: int
        curr_rpm: int

    class DistanceSensor:
        max_distance_ds: float
        min_distance_ds: float
        cur_value_ds: float

        def __init__(self, num_name: int) -> None:
            name = num_name
