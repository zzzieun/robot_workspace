#minial_pub이 발행하는 것을 구독
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry       #nav_msgs/msg/Odometry
#발행한  type이 String 때문에 String객체를 import해야 함

class SubOdom(Node):

    def __init__(self):                                 #멤버 함수(변수 초기화), 생성자 아님
        super().__init__('odometry_subscriber')          #super : 상속  #minimal_subscriber: 노드 이름, 
        sub = self.create_subscription(Odometry, '/odom', self.get_odom, 10)       #ros2 node list (똑같은 이름의 노드 생성x, 덮어 씌어짐)
        self.odom = Odometry()

    def get_odom(self, msg):
        self.odom = msg
        
        #print(self.odom.pose.pose.position.x)


def main(args=None):
    rclpy.init(args=args)

    node = SubOdom()            #class 가지고 객체 생성
    
    while rclpy.ok():
        #rclpy.spin(node)           => 구독x
        rclpy.spin_once(node,timeout_sec=0.1)
        print(round(node.odom.pose.pose.position.x,2))
        
        
    #rclpy.spin(node)
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
