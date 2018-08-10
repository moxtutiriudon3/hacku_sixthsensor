#!/usr/bin/python
# coding:utf-8


import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import UInt8, UInt32
from std_srvs.srv import Trigger


class RealTimeFace():
    def __init__(self):
        sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.get_image)
        self.pub_image = rospy.Publisher("face", Image, queue_size=1)
        self.pub_led = rospy.Publisher("led", UInt8, queue_size=1)
        self.bridge = CvBridge()   # ROSのImage型とOpenCVの画像フォーマットを相互変換
	self.sound_count = 0
	rospy.wait_for_service("/sound_on")
	self.srv_sound = rospy.ServiceProxy("/sound_on", Trigger)
        self.image_org = None

    def monitor(self, rect, org):
        if rect is not None:
            cv2.rectangle(org, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]),
                          (0, 255, 255), 4)
        self.pub_image.publish(self.bridge.cv2_to_imgmsg(org, "bgr8"))

    def get_image(self, img):
        try:
            # Image型をOpenCVのbgr8フォーマットに変換
            self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

    def region_extraction(self):
        r = self.detect_face()
	if r is None:
	    self.pub_led.publish(0)
            return 0.0
        self.sound_call(20)
	wid = self.image_org.shape[1] /3
	if r[0] <= wid:
            self.pub_led.publish(1)
        elif wid <= r[0] <= wid*1.7:
	    self.pub_led.publish(2)
        else:
	    self.pub_led.publish(3)
	return r, wid

    def sound_call(self, timer):
        if self.sound_count == timer:
            self.srv_sound() 	
	    self.sound_count = 0
        self.sound_count += 1

    def detect_face(self):
        if self.image_org is None:
            return None

        org = self.image_org

        # 画像をグレースケールに変換
        gimg = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
        classifier = '/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml'

        # 顔を検出
        cascade = cv2.CascadeClassifier(classifier)
        face = cascade.detectMultiScale(gimg, 1.3, 2, cv2.CASCADE_FIND_BIGGEST_OBJECT)
        
        if len(face) == 0:
            self.monitor(None, org)
            return None

        r = face[0]
        self.monitor(r, org)
        return r


if __name__ == '__main__':
    rospy.init_node("face_to_face")
    fd = RealTimeFace()

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        rospy.loginfo(fd.region_extraction())
        rate.sleep()
