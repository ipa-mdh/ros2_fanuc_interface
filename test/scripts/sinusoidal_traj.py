import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import numpy as np
from controller_manager_msgs.srv import SwitchController

class ForwardPositionSine(Node):
    def __init__(self):
        super().__init__('forward_position_sine')
        
        self.moveing_joint = 0  # Index of the joint to move (0 for J1, 1 for J2, etc.)
        
        self.switch_controllers()
        
        self.publisher_ = self.create_publisher(Float64MultiArray, '/position_commands', 10)
        self.timer = self.create_timer(0.01, self.publish_command)  # 100 Hz
        self.start_time = self.get_clock().now().nanoseconds * 1e-9
        self.freq = 0.5  # Hz
        self.amp = np.deg2rad(30)  # Amplitude in radians (30 degrees)
        
        
    def switch_controllers(self):
        
        self.cli = self.create_client(SwitchController, '/controller_manager/switch_controller')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for controller_manager service...')

        self.req = SwitchController.Request()
        self.req.start_controllers = ['forward_position_controller']
        self.req.stop_controllers = ['manipulator_controller']
        self.req.strictness = SwitchController.Request.STRICT
        self.req.activate_asap = True
        # self.req.timeout = 5.0  # seconds

        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)

        if self.future.result().ok:
            self.get_logger().info('Switched controllers successfully.')
        else:
            self.get_logger().error('Failed to switch controllers.')


    def publish_command(self):
        now = self.get_clock().now().nanoseconds * 1e-9
        elapsed = now - self.start_time
        pos = self.amp * np.sin(2 * np.pi * self.freq * elapsed)

        msg = Float64MultiArray()
        msg.data = [0.0, np.deg2rad(30), 0.0, 0.0, np.deg2rad(-60), 0.0]
        msg.data[self.moveing_joint] = pos
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent: J1 = {pos:.3f}')

def main(args=None):
    rclpy.init(args=args)
    node = ForwardPositionSine()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
