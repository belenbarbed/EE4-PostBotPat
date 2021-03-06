#!/usr/bin/env python

'''
Script to move a hand to a specific position and orientation

run with:
rosrun mm_movement pick_place.py -p <x y z position coordinates> -l/-r -horz/-vert
'''

import argparse
import struct
import sys

import rospy

import baxter_interface
import baxter_external_devices
import tf

from baxter_interface import CHECK_VERSION

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

def get_ik(pose, limb):
    ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
    iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
    ikreq = SolvePositionIKRequest()
    hdr = Header(stamp=rospy.Time.now(), frame_id='base')
    ikreq.pose_stamp.append(pose)
    try:
        rospy.wait_for_service(ns, 5.0)
        resp = iksvc(ikreq)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Service call failed: %s" % (e,))
        return None
    resp_seeds = struct.unpack('<%dB' % len(resp.result_type),
                               resp.result_type)
    if (resp_seeds[0] != resp.RESULT_INVALID):
        seed_str = {
                    ikreq.SEED_USER: 'User Provided Seed',
                    ikreq.SEED_CURRENT: 'Current Joint Angles',
                    ikreq.SEED_NS_MAP: 'Nullspace Setpoints',
                   }.get(resp_seeds[0], 'None')
        print("SUCCESS - Valid Joint Solution Found from Seed Type: %s" %
              (seed_str,))
        # Format solution into Limb API-compatible dictionary
        limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
        return limb_joints
    else:
        print("INVALID POSE - No Valid Joint Solution Found.")
        return None

def arm_move_to_pos(xin,yin,zin,arm,orientationin):
    hdr = Header(stamp=rospy.Time.now(), frame_id='base')

    base_pose = PoseStamped(
            header=hdr,
            pose=Pose(
                position=Point(
                    x=xin,
                    y=yin,
                    z=zin,
                ),
                orientation=orientationin
            ),
        )
    base_pos = get_ik(base_pose, arm)
    arm = baxter_interface.Limb(arm)
    arm.move_to_joint_positions(base_pos)
    print "move complete"

class EndPoint:
    def __init__(self, x, y, z, orientation):
        self.x = x
        self.y = y
        self.z = z
        self.orientation = orientation

    def goTo(self, arm):
        arm_move_to_pos(self.x, self.y, self.z, arm, self.orientation)

    def goToGrab(self, arm):
        yin = self.y + 0.05
        arm_move_to_pos(self.x, yin, self.z, arm, self.orientation)

    def goToClear(self, arm):
        yin = self.y - 0.10
        arm_move_to_pos(self.x, yin, self.z, arm, self.orientation)

def makeQuaternion(xin,yin,zin,win):
    return Quaternion(
                x=xin,
                y=yin,
                z=zin,
                w=win,
            )

def main():
    parser = argparse.ArgumentParser(description='Process the x y z coordinates')

    parser.add_argument('-p', type=float, nargs='+',
        help='the x y z coordinates for arm position')

    parser.add_argument('-left', default=False, action='store_true', dest='left',
        help='move the left arm')
    parser.add_argument('-right', default=False, action='store_true', dest='right',
        help='move the right arm')
        
    parser.add_argument('-vert', default=False, action='store_true', dest='vertical',
        help='hand to finish in vertical orientation')
    parser.add_argument('-horz', default=False, action='store_true', dest='horizontal',
        help='hand to finish in horizontal orientation')

    args = parser.parse_args()

    rospy.loginfo("Initializing node... ")
    rospy.init_node("pick_place")
    rospy.loginfo("Initializing node... ")

    arm = 'left'
    orientation = makeQuaternion(0.57, -0.56, -0.45, -0.40)

    if(args.right):
        arm = 'right'
    if(args.vertical):
        orientation = makeQuaternion(0.00, 0.99, 0.03, 0.00)
        
    arm_move_to_pos(args.p[0], args.p[1], args.p[2], arm, orientation)

    rospy.loginfo("Finished pick_and_place")

if __name__ == "__main__":
    main()

