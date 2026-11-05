#!/usr/bin/env python3
import rospy
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class TurtleFollower:
    def __init__(self):
        # 初始化节点
        rospy.init_node('turtle_follower', anonymous=True)
        
        # 存储两只乌龟的位置信息
        self.turtle1_pose = Pose()
        self.turtle2_pose = Pose()
        
        # 订阅turtle1的位置（命名空间/turtle1下）
        rospy.Subscriber('/turtle1/turtle1/pose', Pose, self.update_turtle1_pose)
        
        # 订阅turtle2的位置（命名空间/turtle2下）
        rospy.Subscriber('/turtle2/turtle2/pose', Pose, self.update_turtle2_pose)
        
        # 发布turtle2的速度指令（命名空间/turtle2下）
        self.vel_pub = rospy.Publisher('/turtle2/turtle2/cmd_vel', Twist, queue_size=10)
        
        # 控制参数（P控制的比例系数）
        self.Ka = 4.0  # 角度比例系数
        self.Kv = 0.5  # 线速度比例系数
        
        # 控制循环频率
        self.rate = rospy.Rate(10)  # 10Hz

    def update_turtle1_pose(self, data):
        """更新turtle1的位置信息"""
        self.turtle1_pose = data

    def update_turtle2_pose(self, data):
        """更新turtle2的位置信息"""
        self.turtle2_pose = data

    def follow(self):
        """实现跟随控制逻辑"""
        vel_msg = Twist()
        
        # 1. 计算位置差
        delta_x = self.turtle1_pose.x - self.turtle2_pose.x
        delta_y = self.turtle1_pose.y - self.turtle2_pose.y
        
        # 2. 计算目标朝向角
        target_theta = math.atan2(delta_y, delta_x)
        
        # 3. 计算角速度（角度控制）
        angle_error = target_theta - self.turtle2_pose.theta
        # 处理角度环绕问题（确保误差在[-π, π]范围内）
        angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi
        vel_msg.angular.z = self.Ka * angle_error
        
        # 4. 计算线速度（距离控制）
        distance = math.sqrt(delta_x**2 + delta_y**2)
        vel_msg.linear.x = self.Kv * distance
        
        # 发布速度指令
        self.vel_pub.publish(vel_msg)
        self.rate.sleep()

if __name__ == '__main__':
    try:
        follower = TurtleFollower()
        while not rospy.is_shutdown():
            follower.follow()
    except rospy.ROSInterruptException:
        pass

