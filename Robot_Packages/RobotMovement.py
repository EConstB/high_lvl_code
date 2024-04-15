class RobotMovement:
    def __init__(self):
        self.straight_dir = 0  # 0 - forward, 1 - backward
        self.straight_speed = 0  # 0 to 255 carrots
        self.rot_dir = 0  # 0 - left, 1 - right
        self.rot_angle = 0  # 0 to 360 deg
        self.cmds_list = []

    def transform_deltalines_to_cmd(self):
        pass

    def get_user_cmd(self):
        pass

    def create_cmd(self):
        # Example: q0124s1270re - 12 characters
        cmd_str = f'q{self.straight_dir}{self.straight_speed}{self.rot_dir}{self.rot_angle}'
        return cmd_str

    def send_cmd(self):
        pass


class Odometry:
    pass
