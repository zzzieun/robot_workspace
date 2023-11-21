import rclpy, sys
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan

class SubLaser(Node):
    
    def __init__(self):
        super().__init__('sub_laser')
        
        self.sub_scan = self.create_subscription(
           LaserScan,           
            '/scan',       
            self.get_scan,   
            qos_profile_sensor_data)
        self.scan = LaserScan()
        
        
    def get_scan(self, msg):
        self.scan = msg
      
        
def main(args=None):
    rclpy.init(args=args)
    node = SubLaser()
    
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            if len(node.scan.ranges) == 360:
                # 160에서 200까지의 범위에서 0.1보다 작은 값이 10개 이상이면 "------" 출력
                if sum(value < 0.1 for value in node.scan.ranges[160:201]) >= 10:
                    print("------")
                else:
                    print("aaaaa")
                print(f"            : {node.scan.ranges[180]}")
            
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
if __name__ == '__main__':
    main()
