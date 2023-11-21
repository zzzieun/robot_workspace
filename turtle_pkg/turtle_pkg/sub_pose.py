import rclpy
from math import degrees
from rclpy.node import Node

from turtlesim.msg import Pose
#import turtlesim.msg 이렇게 쓰면 Pose의 나머지 함수??를 쓸때 복잡해짐
# ==> Pose -> turtlesim.msg.Pose

class SubPose(Node): 

    def __init__(self):     #SubPose의 매개 변수
        super().__init__('sub_turtle_pose')       #node명             클래스의 멤버
        sub = self.create_subscription(Pose, '/turtle1/pose', self.get_pose, 10)
        
        #멤버변수(모든 클래스에서 접급할 수 있는),this->
        self.pose = Pose()      #pose(x,y,theta,linear,angular)
        #self.x = 0.0
        #self.y = 0.0
        #self.theta = 0.0
        
                       #매개변수
    def get_pose(self, msg):        #SubPose의 매개 변수
        self.pose = msg     #msg와 pose가 같은 타입이라면 msg의 데이터가 모두 pose로 들어옴(타입을 맞춰주는것이 중요함)
        
        #self.print_pose()
        
    def print_pose(self):
        print('x = "%s", y="%s", theta="%s"' %(self.pose.x, self.pose.y, self.pose.theta))
                                                #msg.x, msg.y, msg.theta 안됨 msg는 get_pose의 변수이기에
        #pose_x = msg.x
        #print(round(pose_x,2),end= '    ')
        #pose_y = msg.y
        #print(round(pose_y,2),end= '    ')
        #pose_th = msg.theta
        #print(round(pose_th,2))
           
def main(args=None):
    rclpy.init(args=args)       #기본 형식
    node= SubPose()          #class에서는 self. , mian문안에서는 클래스명.(node.)
    
    while rclpy.ok():
        node.print_pose()
    
    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
