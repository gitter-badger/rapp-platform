#!/usr/bin/env python

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

from rapp_platform_ros_communications.srv import (
  fetchDataSrv,
  fetchDataSrvResponse,
  writeDataSrv,
  writeDataSrvResponse,
  deleteDataSrv,
  deleteDataSrvResponse,
  updateDataSrv,
  updateDataSrvResponse,
  whatRappsCanRunSrv,
  whatRappsCanRunSrvResponse
  )

from rapp_platform_ros_communications.msg import (
  StringArrayMsg
  )

from std_msgs.msg import (
  String
  )

class MySQLdbWrapper:

  def __init__(self):
    #tblUser services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_user_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_user_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblUserFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_user_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_user_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblUserWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_user_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_user_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblUserDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_user_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_user_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblUserUpdateDataHandler)
    #tblModel services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_model_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_model_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblModelFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_model_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_model_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblModelWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_model_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_model_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblModelDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_model_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_model_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblModelUpdateDataHandler)
    #tblRapp services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_rapp_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_rapp_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblRappFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_rapp_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_rapp_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblRappWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_rapp_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_rapp_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblRappDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_rapp_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_rapp_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblRappUpdateDataHandler)
    #tblRobot services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_robot_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_robot_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblRobotFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_robot_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_robot_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblRobotWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_robot_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_robot_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblRobotDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_robot_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_robot_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblRobotUpdateDataHandler)
    #tblAppsRobots services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_apps_robots_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_apps_robots_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblAppsRobotsFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_apps_robots_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_apps_robots_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblAppsRobotsWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_apps_robots_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_apps_robots_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblAppsRobotsDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_apps_robots_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_apps_robots_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblAppsRobotsUpdateDataHandler)
    #tblUsersOntologyInstances services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_users_ontology_instances_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_users_ontology_instances_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblUsersOntologyInstancesFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_users_ontology_instances_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_users_ontology_instances_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblUsersOntologyInstancesWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_users_ontology_instances_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_users_ontology_instances_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblUsersOntologyInstancesDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_users_ontology_instances_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_users_ontology_instances_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblUsersOntologyInstancesUpdateDataHandler)
    #viewUsersRobotsApps services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_view_users_robots_apps_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_view_users_robots_apps_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.viewUsersRobotsAppsFetchDataHandler)

    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_what_rapps_can_run_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_what_rapps_can_run Not found error")
    self.serv=rospy.Service(self.serv_topic, whatRappsCanRunSrv, self.whatRappsCanRunDataHandler)


  def writeData(self,req,tblName):
    #generic db write function
    try:
      res = writeDataSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      returncols=self.constructCommaColumns(req.req_cols)
      if (len(returncols)>1):
        returncols="("+returncols+")"
      print returncols
      values=""
      for i in range(len(req.req_data)):
        if (i==0):
          values=values+"("+self.constructCommaColumns(req.req_data[i].s)+")"
        else:
          values=values+",("+self.constructCommaColumns(req.req_data[i].s)+")"

      #print values
      query="Insert into "+tblName+" "+ returncols+" values "+values
      #print query
      cur.execute("LOCK TABLES "+tblName+" WRITE")
      cur.execute(query)
      cur.execute("UNLOCK TABLES")
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      print "Error %d: %s" % (e.args[0],e.args[1])
    except IndexError:
      res.trace.append("Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format")
      res.success.data=False
      print "Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format"
    except IOError:
      print "Error: can\'t find login file or read data"
      res.success.data=False
      res.trace.append("Error: can\'t find login file or read data")
    return res

  def deleteData(self,req,tblName):
    #generic db delete function
    try:
      res = deleteDataSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      where=self.constructAndQuery(req.where_data)
      query="Delete from "+tblName+where
      cur.execute("LOCK TABLES "+tblName+" WRITE")
      cur.execute(query)
      cur.execute("UNLOCK TABLES")
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      print "Error %d: %s" % (e.args[0],e.args[1])
    except IndexError:
      res.trace.append("Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format")
      res.success.data=False
      print "Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format"
    except IOError:
      print "Error: can\'t find login file or read data"
      res.success.data=False
      res.trace.append("Error: can\'t find login file or read data")
    return res

  def updateData(self,req,tblName):
    #generic db update function
    try:
      res = updateDataSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      returncols=self.constructCommaColumns(req.set_cols)
      where=self.constructAndQuery(req.where_data)
      query="Update "+tblName+" SET "+returncols+where
      print query
      cur.execute("LOCK TABLES "+tblName+" WRITE")
      cur.execute(query)
      cur.execute("UNLOCK TABLES")
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      print "Error %d: %s" % (e.args[0],e.args[1])
    except IndexError:
      res.trace.append("Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format")
      res.success.data=False
      print "Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format"
    except IOError:
      print "Error: can\'t find login file or read data"
      res.success.data=False
      res.trace.append("Error: can\'t find login file or read data")
    return res

  def fetchData(self,req,tblName):
    #generic db read function
    try:
      res = fetchDataSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      returncols=self.constructCommaColumns(req.req_cols)
      #print returncols
      where=self.constructAndQuery(req.where_data)
      #print where
      query="SELECT "+returncols+" FROM "+tblName+where
      #print "fetch called"
      cur.execute(query)
      result_set = cur.fetchall()
      for i in range(len(result_set)):
        line=StringArrayMsg()
        for j in range(len(result_set[i])):
          temp_s=String(result_set[i][j])
          line.s.append((str(result_set[i][j])))#=line.s+[String(data=temp_s)]
        res.res_data.append(line)

      con.close()
      if (returncols=="*"):
        res.res_cols=self.getTableColumnNames(tblName)
      else:
        res.res_cols=req.req_cols
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      print "Error %d: %s" % (e.args[0],e.args[1])
    except IndexError:
      res.trace.append("Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format")
      res.success.data=False
      print "Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format"
    except IOError:
      print "Error: can\'t find login file or read data"
      res.success.data=False
      res.trace.append("Error: can\'t find login file or read data")
    return res



  def whatRappsCanRun(self,req,tblName):
    #generic db read function
    try:
      res = whatRappsCanRunSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      #returncols=self.constructCommaColumns(req.req_cols)
      #print returncols
      #where=self.constructAndQuery(req.where_data)
      #print where
      #query="SELECT "+returncols+" FROM "+tblName+where
      query="SELECT rapp_id from tblRappsModelsVersion where model_id='"+req.model_id+"' and minimum_coreagent_version<='"+req.core_agent_version+"'";
      #print "fetch called"
      cur.execute(query)
      result_set = cur.fetchall()
      for i in range(len(result_set)):
        line=StringArrayMsg()
        for j in range(len(result_set[i])):
          temp_s=String(result_set[i][j])
          line.s.append((str(result_set[i][j])))#=line.s+[String(data=temp_s)]
        res.res_data.append(line)
      con.close()
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      print "Error %d: %s" % (e.args[0],e.args[1])
    except IndexError:
      res.trace.append("Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format")
      res.success.data=False
      print "Wrong Query Input Format, check for empty required columns list or wrong/incomplete Query data format"
    except IOError:
      print "Error: can\'t find login file or read data"
      res.success.data=False
      res.trace.append("Error: can\'t find login file or read data")
    return res

  def constructCommaColumns(self,cols):
    #assisting function. adds commas between columns
    if (len(cols)<1):
      #print "return cols empty"
      return ""

    elif (cols[0]=="*"):
      return "*"
    else:
      returncols=""
      for i in range(len(cols)):
          if i==0:
            returncols=returncols+cols[i]
          else:
            returncols=returncols+","+cols[i]
      return returncols

  def constructAndQuery(self,cols):
    #assisting function. constructs the where=... and where=... part of a query
    returnquery=""
    if(len(cols)==0):
      return ""
    else:
      for i in range(len(cols)):
        if i==0:
          returnquery=returnquery+cols[i].s[0]+"=\""+cols[i].s[1]+"\""
        else:
          returnquery=returnquery+" AND "+cols[i].s[0]+"=\""+cols[i].s[1]+"\""
      returnquery=" WHERE "+returnquery
      return returnquery

  def getTableColumnNames(self,tblName):
    #returns the column names of a table
    db_username,db_password=self.getLogin()
    try:
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      cur.execute("Show columns from "+tblName)
      result_set = cur.fetchall()
      Columns=[]
      for row in result_set:
        Columns=Columns+[String(str(row[0]))]
      return Columns
    except mdb.Error, e:
      print "Error %d: %s" % (e.args[0],e.args[1])


  def getLogin(self):
    #Loads file with db credentials
    fh = open("/etc/db_credentials", "r")
    db_username=fh.readline()
    db_username=db_username.split( )[0]
    db_password=fh.readline()
    db_password=db_password.split()[0]
    return db_username,db_password


  def checkConnection(self):
    #checks connectivity to the DB
    try:
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore')
      cur = con.cursor()
      cur.execute("SELECT VERSION()")
      ver = cur.fetchone()
      print "Database version : %s " % ver
      con.close()
    except mdb.Error, e:
      print "Error %d: %s" % (e.args[0],e.args[1])

  #tblUser callbacks
  def tblUserFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblUser")
    return res

  def tblUserWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblUser")
    return res

  def tblUserDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"tblUser")
    return res

  def tblUserUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"tblUser")
    return res
  #end tblUser callbacks

  #tblModel callbacks
  def tblModelFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblModel")
    return res

  def tblModelWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblModel")
    return res

  def tblModelDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"tblModel")
    return res

  def tblModelUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"tblModel")
    return res
  #end tblModel callbacks

  #tblRapp callbacks
  def tblRappFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblRapp")
    return res

  def tblRappWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblRapp")
    return res

  def tblRappDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"tblRapp")
    return res

  def tblRappUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"tblRapp")
    return res
  #end tblRapp callbacks

  #tblRobot callbacks
  def tblRobotFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblRobot")
    return res

  def tblRobotWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblRobot")
    return res

  def tblRobotDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"tblRobot")
    return res

  def tblRobotUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"tblRobot")
    return res
  #end tblRapp callbacks


  #tblAppsRobots callbacks
  def tblAppsRobotsFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblAppsRobots")
    return res

  def tblAppsRobotsWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblAppsRobots")
    return res

  def tblAppsRobotsDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"tblAppsRobots")
    return res

  def tblAppsRobotsUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"tblAppsRobots")
    return res
  #end tblAppsRobots callbacks

  #tblUsersOntologyInstances callbacks
  def tblUsersOntologyInstancesFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblUsersOntologyInstances")
    return res

  def tblUsersOntologyInstancesWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblUsersOntologyInstances")
    return res

  def tblUsersOntologyInstancesDeleteDataHandler(self,req):
    res = deleteSrvResponse()
    res=self.deleteData(req,"tblUsersOntologyInstances")
    return res

  def tblUsersOntologyInstancesUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"tblUsersOntologyInstances")
    return res
  #end tblAppsRobots callbacks

  #viewUsersRobotsApps callbacks
  def viewUsersRobotsAppsFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"usersrobotsapps")
    return res
  #viewUsersRobotsApps

  #viewUsersRobotsApps callbacks
  def whatRappsCanRunDataHandler(self,req):
    res = whatRappsCanRunSrvResponse()
    res=self.whatRappsCanRun(req,"tblRappsModelsVersion")
    return res
  #viewUsersRobotsApps

if __name__ == "__main__":
  rospy.init_node('MySQLWrapper')
  MySQLWrapperNode = MySQLdbWrapper()
  rospy.spin()
