import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from arduino.getchar import Getchar

class PubJob_MSG(Node):

    def __init__(self):
        super().__init__('pub__msg_by_kb')
        self.pub_msg = self.create_publisher(String, 'job_msg', 10)
        self.job_msg = String()
        
    def pub_led_msg(self, job_msg):
        msg = String()
        msg.data = job_msg
        self.pub_msg.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    node = PubJob_MSG()

    #rclpy.spin(node)
    try:
        kb = Getchar()
        key =''
        while rclpy.ok():
            key = kb.getch()
            if key == '1':
                node.pub_led_msg('start')
            elif key == '0':
                node.pub_led_msg('finish')
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
