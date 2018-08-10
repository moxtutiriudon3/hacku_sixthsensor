#!/usr/bin/python
# coding:utf-8


import rospy
from std_msgs.msg import UInt8


def write_freq(number=0):
    bfile = '/dev/myled_cls0'
    try:
        with open(bfile, "w") as f:
	    f.write(str(number) + "\n")
    # 入出力に関するエラー
    except IOError:
        rospy.logerr("can't write to " + bfile)


def recv_led(data):
    #rospy.loginfo(type(data))
    #rospy.loginfo(data.data)
    write_freq(data.data)


if __name__ == '__main__':
    rospy.init_node('led_controller')
    # トピックの名前, トピックの型, 購読した時に起動する関数
    rospy.Subscriber("led", UInt8, recv_led)
    rospy.spin()

