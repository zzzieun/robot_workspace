import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from arduino.getchar import Getchar     #arduino폴더 안에 있는 getchar 파일에 Getchar를 import

class PubLED_MSG(Node):

    def __init__(self):     #노드 이름
        super().__init__('pub_led_msg')      #토픽 타입, 토픽 명, q-size
        self.pub_led = self.create_publisher(String, 'led_msg', 10)
        self.led_msg = String()   #멤버 변수 선언, String 타입
        
    def pub_led_msg(self, led_msg):     #멤버 함수(self 매개 변수)
        msg = String()
        msg.data = led_msg      #msg.data => cf)pose.x
        self.pub_led.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    node = PubLED_MSG()

    #rclpy.spin(node)
    try:
        kb = Getchar()
        key =''
        while rclpy.ok():       #while rclpy.ok():ros가 구동중인 동안 무한 루프
            key = kb.getch()    #while True      :무한 루프
            if key == '1':
                node.pub_led_msg('on')
            elif key == '0':
                node.pub_led_msg('off')
            else:
                pass
    except KeyboardInterrupt:
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
