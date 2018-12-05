#!/usr/bin/env python
import rospy
import rosbag
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from std_msgs.msg import Bool
# from whycon.srv import SetNumberOfTargets
import math
import numpy as np
import glob
import time
import sys
import os
import csv



class drone_hold():
	"""docstring drone_hold me"""
	def __init__(self):
		self.hold_x=-5.63     #-5.63 +- 0.2 
		self.hold_y=-5.63    #-5.63 +- 0.2
		self.hold_z=30    # 30   +- 0.2

		self.loop_time=120
		self.Inside_time=0
		self.outside_time=0
		self.last_time=0
		self.flag=1
		self.previous_x=0
		fn = sys.argv[1]
		self.arm_flag = False
		self.start_x = None
		self.start_y = None
		self.start_z = None
		self.flag_start_val = False
		self.idle_time_bfr = 0
		self.topic_no = 0
		self.idle_measured_flag = False
		# print fn
			# if os.path.exists(fn):
   #  			print os.path.basename(fn)
		rospy.init_node('position_hold')
		# bag=rosbag.bag('*.bag')
		path = str(fn)+"/*.bag"
		# print path
		for filename in glob.glob(path):
			bag = rosbag.Bag(filename)
			self.data =  bag.read_messages_time(topics='whycon/poses')
			self.m_count= bag.read_messages(topics='whycon/poses')
			print self.data, self.m_count
		# rospy.wait_for_service('/whycon/reset')
		# self.target_value = rospy.ServiceProxy('whycon/reset', SetNumberOfTargets)
		#self.target_value(self.default_target)
		rospy.Subscriber('whycon/poses', PoseArray, self.get_pose)

	def get_pose(self, value):
		self.drone_x = value.poses[0].position.x
		self.drone_y = value.poses[0].position.y
		self.drone_z = value.poses[0].position.z

		if self.flag_start_val == False:
			self.start_x = round(-0.0177010912448,3)
			self.start_y = round(-0.0177010912448,3)
			self.start_z = round(54.7306060791,3)
			self.flag_start_val = True

		if(self.idle_measured_flag == False):
			self.idle_time_bfr += 1


		if (((self.start_x != round(self.drone_x,3)) or (self.start_y != round(self.drone_y,3)) or (self.start_z != round(self.drone_z,3))) and self.arm_flag == False):
			print "here"
			self.arm_flag = True
			self.idle_measured_flag = True
			# time.sleep(.2)
			# self.previous_x = self.drone_x
		

		if (self.arm_flag == True):
			self.position_hold()

	def distance_calculation(self, x2, x1, y2, y1):
		distance = math.sqrt(((x2-x1) ** 2) + ((y2 -y1) **2))
		return distance

	def position_hold(self):
			self.topic_no +=1
			print self.topic_no, self.idle_time_bfr,self.m_count
			if((self.topic_no + self.idle_time_bfr)== self.m_count):
				with open("/home/simmu/Documents/testing_cd_grade/grade.csv", "a") as csv_file:
					    writer = csv.writer(csv_file)
					    writer.writerow([self.Inside_time, self.outside_time, self.idle_time_bfr, self.m_count])
					    self.topic_no = 0

			# self.current_time =time.time()


			# time_change = (self.current_time - self.last_time)
			# # print time_change
			# if (time_change>=(self.data - 0.5)):
			# 	# Inside_time = time.
			# 	if (self.flag==0):
			# 		with open("/home/simmu/Documents/testing_cd_grade/grade.csv", "a") as csv_file:
			# 		    writer = csv.writer(csv_file)
			# 		    writer.writerow([self.Inside_time, self.outside_time, self.idle_time_bfr, self.m_count])
			# 		    # csv_file.write(str(self.Inside_time) + "\n")
			# 		    # csv_file.write(str(self.outside_time) + "\n")
			# 		    # csv_file.write(str(self.data) + "\n")

			# 	    # time.sleep(.2)
			# 	# print drone_x
			# 	self.last_time = self.current_time

			else:
				# print "here"
				time_now = time.time()
				point=self.distance_calculation(self.hold_x,self.drone_x,self.hold_y,self.drone_y)
				if (point <=0.4) & (self.hold_z-0.5 < self.drone_z < self.hold_z+0.5):
					
					self.Inside_time+=1
					print "inside time" + str(self.Inside_time)
				else:
					self.outside_time+=1
					print self.outside_time
				# self.last_time = self.current_time
				self.flag=0


		

test = drone_hold()
rospy.spin()
