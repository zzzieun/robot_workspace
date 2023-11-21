import rclpy
#rclpy = ros client library python
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):     #init안에 선언된 변수 :self.  
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'hello', 10)        #self.  :clas 안에서 전역변수 처럼 사용가능
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0                      #주기         #할 일

    def timer_callback(self):  
        #tw = Twist()    
        msg = String()      #msg의 내용이 0.5초마다 바뀜
        msg.data = 'Hello World: %d' % self.i    
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()      #class만 선언함

    rclpy.spin(minimal_publisher)               #spin이  없으면 노드가 종료 되고 shutdown된다
                                                #spin : 종료를 막아준다 why?계속(0.5초 마다) callback이 일어나기 위해, while로 돌려도 된다.

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
