#!/usr/bin/env python

'''
Script to pick medicine box from storage unit and chand it to the customer

run with:
rosrun mm_movement deliver_box.py -s <slot_number>
or
rosrun mm_movement deliver_box.py -s 0
to make it listen to the DB topic
'''

import argparse
import rospy
import time

from pick_place import EndPoint, makeQuaternion
from gripper import gripper_action
from mm_movement.msg import DB_output, Collect_message

from geometry_msgs.msg import (
    Quaternion,
)

# Orientations
vertical = makeQuaternion(0.00, 0.99, 0.03, 0.00) 
wayptor = makeQuaternion(0.71, 0.70, 0.03, 0.00)         
horizontal = makeQuaternion(0.57, -0.56, -0.45, -0.40)
outofwayor = makeQuaternion(-0.40, 0.91, 0.04, 0.07)         

# Positions
handin = EndPoint(0.80, 0.22, -0.18, vertical)
waypoint = EndPoint(0.21, 0.57, 0.00, wayptor)
outofway = EndPoint(0.47, 0.72, 0.43, outofwayor)
slots = [
    EndPoint(0.0, 0.0, 0.0, vertical),
    EndPoint(0.00, 1.12, 0.14, horizontal),
    EndPoint(0.11, 1.14, 0.14, horizontal),
    EndPoint(0.22, 1.15, 0.14, horizontal),
    EndPoint(0.31, 1.15, 0.13, horizontal)
]

def main():
    parser = argparse.ArgumentParser(description='Deliver medicine from storage slot')

    parser.add_argument('-s', type=int, dest='slot',
        help='the slot number, 1-4')
        
    args = parser.parse_args()

    rospy.loginfo("Initializing node... ")
    rospy.init_node("deliver_box")
    rospy.loginfo("Initializing node... ")
    global pub 
    pub = rospy.Publisher("Collected_Channel", Collect_message, queue_size=10)


    if(args.slot == 0):
        # listen to topics instead
        rospy.Subscriber("DB_Move_Channel", DB_output, pass_slot)
        rospy.spin()
    else:
        # use command line args
        deliver_box(args.slot)

def pass_slot(data):
    if(data.Column == 0):
        # no prescription of user in sight
        return
    deliver_box(data.Column, data.NHSNumber, data.MedicineName)

def deliver_box(slot, NHSNumber=0, MedicineName=''):
    outofway.goTo('left')
    gripper_action('open', 'left')
    waypoint.goTo('left')
    
    slots[slot].goTo('left')
    slots[slot].goToGrab('left')
    gripper_action('close', 'left')
    slots[slot].goToClear('left')
        
    waypoint.goTo('left')
    handin.goTo('left')
    time.sleep(2)
    gripper_action('open', 'left')
    time.sleep(2)
    outofway.goTo('left')

    # publish to topic confirming delivery of prescription to user
    if(NHSNumber != 0 and MedicineName != ''):
        global pub
        msg = Collect_message()
        msg.NHSNumber = NHSNumber
        msg.MedicineName = MedicineName
        pub.publish(msg)
    
    rospy.loginfo("Finished deliver_box")

if __name__ == "__main__":
    main()
