#!/usr/bin/python
# coding:utf-8

import rospy
from std_msgs.msg import Int32
from time import sleep, time
import RPi.GPIO as GPIO


TRIG_PORT = 15
ECHO_PORT = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PORT, GPIO.OUT)
GPIO.setup(ECHO_PORT, GPIO.IN)


class DistanceMeasurement():
    def __init__(self, trig_port, echo_port):
        self.trig_port = trig_port
	self.echo_port = echo_port
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(self.trig_port, GPIO.OUT)
	GPIO.setup(self.echo_port, GPIO.IN)
	self.pub = rospy.Publisher("distance", Int32, queue_size=1)
	self.distance = None

    def cleanup(self):
        GPIO.cleanup()
	rospy.loginfo("距離測定終了")

    def read_distance(self):
        GPIO.output(TRIG_PORT, GPIO.LOW)
        sleep(0.001)
        GPIO.output(TRIG_PORT, GPIO.HIGH)
        sleep(0.011)
        GPIO.output(TRIG_PORT, GPIO.LOW)

        sig_start = sig_end = 0
        while GPIO.input(ECHO_PORT) == GPIO.LOW:
            sig_start = time()
        while GPIO.input(ECHO_PORT) == GPIO.HIGH:
            sig_end = time()

        duration = sig_end - sig_start
        distance = duration * 17000
        self.distance = int(distance)
	self.pub.publish(self.distance)
	return self.distance



if __name__ == '__main__':
    rospy.init_node("distance_hcsr04")
    dm = DistanceMeasurement(trig_port=TRIG_PORT, echo_port=ECHO_PORT)
    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        rospy.loginfo(dm.read_distance())
    dm.cleanup()
