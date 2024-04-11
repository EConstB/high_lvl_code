from Robot_Packages.Robot_state_parameters import RobotParameters


class BatteryUnit(RobotParameters.Battery):

    def __init__(self, max_v=None, min_v=None,
                 curr_v=None, precent=None) -> None:
        super().__init__()
        self.bat_max_volt = max_v
        self.bat_min_volt = min_v
        self.bat_curr_volt = curr_v
        self.bat_percent_value = precent

        self.bat_max_capacity = None
        self.bat_min_capacity = None
        self.bat_curr_capacity = None

    def get_bat_data(self, curr_value):
        ...
        self.bat_curr_volt = curr_value
        return self.bat_curr_volt

    def battery_monitoring(self):
        delta_min_max = self.bat_max_volt - self.bat_min_volt
        curr_delta_min = self.bat_curr_volt - self.bat_min_volt
        self.bat_percent_value = (curr_delta_min / delta_min_max) * 100
        return self.bat_percent_value
