import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
import cv2
import numpy as np

class LineDetector(Node):

    def __init__(self):
        super().__init__('img_convert')
        qos_profile = QoSProfile(depth=10)

        self.subscription = self.create_subscription(CompressedImage, 
                'camera/image/compressed', 
                self.get_compressed, 
                10)
        self.bridge = CvBridge()
        self.cv_img = cv2.imread('/home/ji/robot_ws/src/ar_track/artrack/origin.png')

    def get_compressed(self, msg):
        self.cv_img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")

def main(args=None):
    rclpy.init(args=args)
    node = LineDetector()
    
    try:   
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            img = node.cv_img
            if img is not None and not img.size == 0: 
                cv2.imshow('test', img)
                    
            if cv2.waitKey(1) == ord('q'):
                break
    
        cv2.destroyAllWindows()
            
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        
    finally:
        node.destroy_node()
        rclpy.shutdown()
            
if __name__ == '__main__':
    main()
    
    # cv2.rectangle(mask, (cx-3, cy-3), (cx+3,cv+3), (255,255,255), 1, lineType=None, shift=None)
