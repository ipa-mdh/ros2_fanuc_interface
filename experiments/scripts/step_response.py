import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from controller_manager_msgs.srv import SwitchController
import numpy as np


class ForwardPositionStep(Node):
    def __init__(self):
        super().__init__('forward_position_step')

        self.joint_index = 0  # Joint to command
        self.step_value = np.deg2rad(0)

        self.switch_controllers()

        self.publisher_ = self.create_publisher(Float64MultiArray, '/position_commands', 10)

        # Give the controller a moment to activate before publishing
        self.timer = self.create_timer(0.5, self.send_step_command)

    def switch_controllers(self):
        self.cli = self.create_client(SwitchController, '/controller_manager/switch_controller')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for controller_manager service...')

        req = SwitchController.Request()
        req.start_controllers = ['forward_position_controller']
        req.stop_controllers = ['manipulator_controller']
        req.strictness = SwitchController.Request.STRICT
        req.activate_asap = True

        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        if future.result() and future.result().ok:
            self.get_logger().info('Switched controllers successfully.')
        else:
            self.get_logger().error('Failed to switch controllers.')

    def send_step_command(self):
        msg = Float64MultiArray()
        msg.data = [0.0, np.deg2rad(30), 0.0, 0.0, np.deg2rad(-60), 0.0]
        msg.data[self.joint_index] = self.step_value
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent step command: joint {self.joint_index + 1} = {self.step_value}')
        
        # Shut down after sending the command
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = ForwardPositionStep()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
