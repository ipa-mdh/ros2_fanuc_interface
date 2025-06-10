import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from shape_msgs.msg import SolidPrimitive
from moveit_msgs.msg import PlanningScene, CollisionObject

class AddObj(Node):
    def __init__(self):
        super().__init__('add_obstacle')
        
        self.scene_pub = self.create_publisher(PlanningScene, '/planning_scene', 10)
        self.timer = self.create_timer(2.0, self.run)
        self.has_published = False

    def run(self):
        if not self.has_published:
            self.add_collision_box()
            self.has_published = True
            self.timer.cancel()
            self.get_logger().info("Published collision object, shutting down...")
            rclpy.shutdown()  # This will cause spin() to return

    def add_collision_box(self):
        co = CollisionObject()
        co.id = 'box'
        co.header.frame_id = 'base_link'

        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX
        box.dimensions = [0.8, 0.15, 1.3]  # size of box

        pose = PoseStamped()
        pose.header.frame_id = 'base_link'
        pose.pose.position.x = 0.97
        pose.pose.position.y = 0.0
        pose.pose.position.z = 0.3
        pose.pose.orientation.w = 1.0

        co.primitives.append(box)
        co.primitive_poses.append(pose.pose)
        co.operation = CollisionObject.ADD

        scene = PlanningScene()
        scene.is_diff = True
        scene.world.collision_objects.append(co)

        self.get_logger().info("Publishing collision object...")
        self.scene_pub.publish(scene)

def main(args=None):
    rclpy.init(args=args)
    node = AddObj()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
