#!/usr/bin/env python
# -*- coding: utf-8 -*

# general
import rospy
from geometry_msgs.msg import Twist,Pose
import urllib3
import json

BEHAVIOR_URL = "http://172.20.10.3:5000/db/behavior"
ENV_URL = "http://172.20.10.3:5000/db/env"
http = urllib3.PoolManager()

# msgs
from gazebo_msgs.msg import ModelStates

class Rc110x:
    def __init__(self):
        # subscriber
        self.model_sub = rospy.Subscriber('gazebo/model_states',ModelStates, self.getModelCB,queue_size=1)
        self.model_status = 0

        # publisher
        self.cmd_vel_pub = rospy.Publisher('/drive_twist',Twist,queue_size=1)

    def getModelCB(self,msg):
        self.model_states = msg

    def moveRc110(self,x,yaw):
        vel = Twist()
        vel.linear.x  = x
        vel.angular.z = yaw
        self.cmd_vel_pub.publish(vel)

    def mainLoop(self):

        while not rospy.is_shutdown():

            rospy.sleep(1)
            
            # DBから速度/角速度を取得してロボットへ送信
            r = http.request('GET',ENV_URL)
            print r.data
            db_data = json.loads(r.data)
            
            self.moveRc110(
                    float(db_data["linear_x"]),
                    float(db_data["angular_z"]))

            # 環境状態をDBへ保存




if __name__ == '__main__':
    rospy.init_node('rc110x')
    rc110x=Rc110x()
    rc110x.mainLoop()
