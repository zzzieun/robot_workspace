#서비스를 제공하는 서비스 파일(1회성 통신(q size 필요 없음,12번 line))
from example_interfaces.srv import AddTwoInts   #share -> example_interfaces

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
                                            #서비스 타입(유형)   서비스 이름        콜백
    def add_two_ints_callback(self, request, response):     #request : a,b response: sum
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

        return response #where? 서비스 요청 한 곳


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
