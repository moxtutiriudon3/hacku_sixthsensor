#!/usr/bin/python
# coding:utf-8


import rospy
from std_msgs.msg import UInt32
from std_srvs.srv import Trigger, TriggerResponse
import pygame.mixer
import time

mp3file_name = "/home/ubuntu/catkin_ws/src/realtime_face/src/n21.mp3"

class Sound():
    def __init__(self, filename):
        self.sound_file = filename
        self.srv_sound = rospy.Service('sound_on', Trigger, self.callback_sound)

    def callback_sound(self, message):
        d = TriggerResponse()
	d.success = self.sound()
	d.message = "sound_start"
	return d

    def sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load(mp3file_name)
	pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        time.sleep(0.5)
        pygame.mixer.music.stop()
	return True

if __name__ == '__main__':
    rospy.init_node("sound")
    sound = Sound(mp3file_name)
    rospy.spin()
