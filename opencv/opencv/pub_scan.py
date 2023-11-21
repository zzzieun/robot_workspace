import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LidarPublisher(Node):
    def __init__(self):
        super().__init__('lidar_publisher')
        self.publisher = self.create_publisher(LaserScan, 'scan', 10)
        self.timer = self.create_timer(1.0, self.publish_lidar_data)
        self.scan = LaserScan()

    def publish_lidar_data(self):
        # 생성한 LiDAR 데이터를 발행
        self.scan.header.stamp = self.get_clock().now().to_msg()
        self.scan.header.frame_id = 'base_link'
        self.scan.angle_min = -3.14159265359
        self.scan.angle_max = 3.14159265359
        self.scan.angle_increment = 0.01745329252
        self.scan.time_increment = 0.00005
        self.scan.scan_time = 0.00001
        self.scan.range_min = 0.0
        self.scan.range_max = 100.0
        # 예시 LiDAR 데이터 (각도에 따른 거리)
        self.scan.ranges = [1.0, 2.0, 3.0, 4.0, 5.0]  # 예시 LiDAR 데이터

        self.publisher.publish(self.scan)

def main(args=None):
    rclpy.init(args=args)
    lidar_publisher = LidarPublisher()
    rclpy.spin(lidar_publisher)
    lidar_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

