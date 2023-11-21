import rclpy
from rclpy.node import Node
import math
from geometry_msgs.msg import Twist


class MoveTurtle(Node):

    def __init__(self):
        super().__init__('move_turtle')       #node명

def main(args=None):
    rclpy.init(args=args)       #기본 형식
    node= MoveTurtle()          #class에서는 self. , mian문안에서는 클래스명.(node.)
    pub = node.create_publisher(Twist, '/turtle1/cmd_vel', 10)      #Twist메세지를 publish함
    tw = Twist()                        #topic이름(topic list name)
    try:
        while rclpy.ok():
                #원
             tw.linear.x = 0.4
             tw.angular.z = 0.2
             pub.publish(tw)
                #사각형
             #for _ in range(4):
                # 직진 (한 변의 길이)
                #tw.linear.x = 3.0
                #tw.angular.z = 0.0
                #pub.publish(tw)
                #rclpy.spin_once(node, timeout_sec=1.0)

                # 90도 회전 (라디안으로 변환)
                #tw.linear.x = 0.0
                #tw.angular.z = math.pi / 2.0  # 90도를 라디안으로 변환
                #pub.publish(tw)
                #rclpy.spin_once(node, timeout_sec=1.0)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()
        
if __name__ == '__main__':
    main()
