#minial_pub이 발행하는 것을 구독
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
#발행한  type이 String 때문에 String객체를 import해야 함

class MinimalSubscriber(Node):

    def __init__(self):                                 #멤버 함수(변수 초기화), 생성자 아님
        super().__init__('minimal_subscriber')          #super : 상속  #minimal_subscriber: 노드 이름, 
        sub = self.create_subscription(String, 'hello', self.callback, 10)       #ros2 node list (똑같은 이름의 노드 생성x, 덮어 씌어짐)
        #self.subscription  # prevent unused variable warning                   #callback언제 호출? 정해진 이벤트가 실행

    def callback(self, msg):
        print('"%s"' % msg.data)       #talker가 발행하는 topic (string 타입)


def main(args=None):
    rclpy.init(args=args)

    minimalsubscriber = MinimalSubscriber()            #class 가지고 객체 생성

    rclpy.spin(minimalsubscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimalsubscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
