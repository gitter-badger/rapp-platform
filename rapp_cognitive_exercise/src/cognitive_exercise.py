#!/usr/bin/env python
# -*- encode: utf-8 -*-

#Copyright 2015 RAPP

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# Author: Athanassios Kintsakis
# contact: akintsakis@issel.ee.auth.gr

import rospy
import MySQLdb as mdb
import sys
import xml.etree.ElementTree as ET

import calendar
import time

from datetime import datetime
from os.path import expanduser
from test_selector import TestSelector
from recordUserCognitiveTestPerformance import RecordUserCognitiveTestPerformance
from cognitive_test_creator import CognitiveTestCreator

from rapp_platform_ros_communications.srv import (
  testSelectorSrv,
  testSelectorSrvResponse,
  createOntologyAliasSrv,
  createOntologyAliasSrvRequest,
  createOntologyAliasSrvResponse,
  recordUserCognitiveTestPerformanceSrv,
  recordUserCognitiveTestPerformanceSrvResponse,
  cognitiveTestCreatorSrv,
  cognitiveTestCreatorSrvResponse
  )

from rapp_platform_ros_communications.msg import (
  StringArrayMsg
  )

from std_msgs.msg import (
  String
  )

class CognitiveExercise:

  def __init__(self):
    #tblUser services launch
    self.serv_topic = rospy.get_param("rapp_cognitive_exercise_chooser_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_cognitive_exercise_chooser_topic not found")
    self.serv=rospy.Service(self.serv_topic, testSelectorSrv, self.chooserDataHandler)

    self.serv_topic = rospy.get_param("rapp_cognitive_exercise_record_user_cognitive_test_performance_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_cognitive_exercise_record_user_cognitive_test_performance_topic not found")
    self.serv=rospy.Service(self.serv_topic, recordUserCognitiveTestPerformanceSrv, self.recordUserCognitiveTestPerformanceDataHandler)

    self.serv_topic = rospy.get_param("rapp_cognitive_test_creator_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_cognitive_test_creator_topic not found")
    self.serv=rospy.Service(self.serv_topic, cognitiveTestCreatorSrv, self.rcognitiveTestCreatorDataHandler)

  #tblUser callbacks
  def chooserDataHandler(self,req):
    res = testSelectorSrvResponse()
    it = TestSelector()
    res=it.chooserFunction(req)
    return res

  def recordUserCognitiveTestPerformanceDataHandler(self,req):
    res = recordUserCognitiveTestPerformanceSrvResponse()
    it = RecordUserCognitiveTestPerformance()
    res=it.recordPerformance(req)
    return res

  def rcognitiveTestCreatorDataHandler(self,req):
    res = cognitiveTestCreatorSrvResponse()
    it = CognitiveTestCreator()
    res=it.testCreator(req)
    return res

if __name__ == "__main__":
  rospy.init_node('CognitiveExercise')
  CognitiveExerciseNode = CognitiveExercise()
  rospy.spin()
