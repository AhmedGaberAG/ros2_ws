import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy
from std_msgs.msg import String

class SimpleQosPublisher(Node):
    def __init__(self):
        super().__init__('simple_qos_publisher')
        self.qos_profile_pub = QoSProfile(depth=10)

        self.declare_parameter("counter", 0)
        self.declare_parameter("frequency", 1.0)
        self.declare_parameter('reliability', 'system_default')
        self.declare_parameter('durability', 'system_default')

        self.counter_ = self.get_parameter("counter").value
        self.frequency_ = self.get_parameter("frequency").value
        reliability = self.get_parameter('reliability').get_parameter_value().string_value
        durability = self.get_parameter('durability').get_parameter_value().string_value

        if reliability == 'best_effort':
            self.qos_profile_pub.reliability = QoSReliabilityPolicy.BEST_EFFORT
            self.get_logger().info('[Reliability] : Best Effort')
        elif reliability == 'reliable':
            self.qos_profile_pub.reliability = QoSReliabilityPolicy.RELIABLE
            self.get_logger().info('[Reliability] : Reliable')
        elif reliability == 'system_default':
            self.qos_profile_pub.reliability = QoSReliabilityPolicy.SYSTEM_DEFAULT
            self.get_logger().info('[Reliability] : System Default')
        else:
            self.get_logger().error('Selected Reliability QoS: %s doesn\'t exist!' % reliability)
            return

        if durability == 'volatile':
            self.qos_profile_pub.durability = QoSDurabilityPolicy.VOLATILE
            self.get_logger().info('[Durability] : Volatile')
        elif durability == 'transient_local':
            self.qos_profile_pub.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
            self.get_logger().info('[Durability] : Transient Local')
        elif durability == 'system_default':
            self.qos_profile_pub.durability = QoSDurabilityPolicy.SYSTEM_DEFAULT
            self.get_logger().info('[Durability] : System Default')
        else:
            self.get_logger().error('Selected Durability QoS: %s doesn\'t exist!' % durability)
            return

        self.publisher_ = self.create_publisher(String, "chatter", qos_profile=self.qos_profile_pub)
        self.timer_ = self.create_timer(1.0 / self.frequency_, self.timerCallback)   
        self.get_logger().info("Publishing messages at a frequency of %f Hz"
                                % self.frequency_)
        
    def timerCallback(self):
        msg = String()
        msg.data = "Hello, ROS 2! %d" % self.counter_
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing: '%s'" % msg.data)
        self.counter_ += 1

def main(args=None):
    rclpy.init(args=args)
    simple_qos_publisher = SimpleQosPublisher()
    rclpy.spin(simple_qos_publisher)
    simple_qos_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()