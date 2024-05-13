from Robot_Packages.Robot_state_parameters import RobotParameters as robpar

class DistanceSensorUnit(robpar.DistanceSensor):

    def __init__(self, name_ds) -> None:
        super().__init__(num_name=name_ds)
        self.max_distance_ds = None
        self.min_distance_ds = None
        self.cur_value_ds = None
    
    def get_ds_values(self):
        ...
        return self.name
