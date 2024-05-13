from Robot_Packages.Robot_state_parameters import RobotParameters as robpar


class BatteryUnit(robpar.Battery):

    def __init__(self, max_v=None, min_v=None) -> None:
        super().__init__()
        self.bat_max_volt = robpar.Battery.bat_max_volt
        self.bat_min_volt = robpar.Battery.bat_min_volt
        self.bat_curr_volt: float = self.bat_max_volt
        self.bat_percent_value: float = None
        self.bat_state = robpar.Battery.state.normal

    def get_bat_data(self, curr_value):
        ...
        self.bat_curr_volt = curr_value
        return self.bat_curr_volt

    def get_percent_val(self):
        delta_min_max = self.bat_max_volt - self.bat_min_volt
        curr_delta_min = self.bat_curr_volt - self.bat_min_volt
        self.bat_percent_value = (curr_delta_min / delta_min_max) * 100
        self.bat_percent_value = 100 if self.bat_percent_value >= 100 else self.bat_percent_value
        self.bat_percent_value = 0 if self.bat_percent_value <= 0 else self.bat_percent_value
        return self.bat_percent_value
