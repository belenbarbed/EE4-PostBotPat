#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import rospy
import cv2
import cv_bridge

from mm_ui.msg import Face_message
from sensor_msgs.msg import (
    Image,
)
class MedicMikeFace:

    def __init__(self):
        rospy.init_node('Face', anonymous=True)
        rospy.Subscriber("Face_Channel", Face_message, self.__FaceCallback)
        self.pub = rospy.Publisher("/robot/xdisplay", Image, latch=True)
        self.file_loc = os.path.dirname(__file__)
        self.__send_image(self.file_loc + "/FaceImages/sleep.jpg")
        rospy.spin()

    def __send_image(self, path):
        #webbrowser.open(path)

        img = cv2.imread(path)
        msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")

        self.pub.publish(msg)
        # Sleep to allow for image to be published.
        rospy.sleep(1)

    def __FaceCallback(self, data):

        if data.display == "happy":
            self.__send_image(self.file_loc + "/FaceImages/happy.jpg")
            #webbrowser.open("happy.jpg")

        elif data.display == "sleep":
            self.__send_image(self.file_loc + "/FaceImages/sleep.jpg")
            #webbrowser.open("sleep.jpg")

        elif data.display == "worried":
            self.__send_image(self.file_loc + "/FaceImages/worried.jpg")
            
        elif data.display == "confused":
            self.__send_image(self.file_loc + "/FaceImages/confused.jpg")

        else:
            img = Image.new('RGB', (1024, 600), color = (17, 113, 171))#(0, 27, 88)) #(73, 109, 137))

            d = ImageDraw.Draw(img)

            font = ImageFont.truetype('gadugi.ttf', size=100)
            d.text((150,90), ":(", font=font, fill=(255,255,255))#(255,255,0))

            font = ImageFont.truetype('gadugi.ttf', size=30)
            #d.text((150,230), "Hello World this is a test for ", font=font, fill=(255,255,255))#(255,255,0))

            d.multiline_text((150, 230), data.display, font=font, fill=(255,255,255))

            img.save(self.file_loc+'/FaceImages/error.png')
            self.__send_image(self.file_loc+"/FaceImages/error.png")
            #webbrowser.open("error.png")

def main():
    medic_mike_face = MedicMikeFace()

if __name__ == "__main__":
    main()
