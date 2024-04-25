from dataclasses import dataclass


@dataclass
class RobotParameters:
    class Battery:
        bat_max_volt: float = 36.0  # example -> 36.00 is MAX (V)
        bat_min_volt: float = 28.0  # example -> 32.00 is MIN (V)
        bat_curr_volt: float  

        bat_max_capacity: float = 12.0 # example -> 6 Ah is MAX (Ah)
        bat_min_capacity: float = 0.0 # example -> 0 Ah is MIN (Ah)
        bat_curr_capacity: float  

        bat_percent_value: float 

        class state:
            normal: int = 1
            ctit_low: int = 0

        class ConfigBattery:
            parallel_connection: int = 4
            serial_connection: int = 10

    class Sizes:
        lenght: float = 600
        width: float = 400
        height: float = 300

    class MotorWheels:
        wheel_radius: float = 165
        dist_between_wheels: float
        max_rpm: int = 4000
        min_rpm: int = 280
        curr_rpm: int

    class DistanceSensor:
        max_distance_ds: float = 200
        min_distance_ds: float = 12
        cur_value_ds: float

        def __init__(self, num_name: int) -> None:
            self.name = num_name
