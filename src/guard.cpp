#include <ros/ros.h>
#include <tf/tf.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <tf/transform_listener.h>
#include <actionlib/server/simple_action_server.h>
#include "geometry_msgs/Pose.h"
#include "geometry_msgs/PoseArray.h"
#include "geometry_msgs/PoseWithCovarianceStamped.h"

#include <vector>
#include <iostream>
#include <fstream>
#include <assert.h>
#include <ctime>
#include <unistd.h>
#include <ros/package.h>

#include "people_msgs/PositionMeasurementArray.h"

bool iKnowWhereIAm = false;
geometry_msgs::Pose bot_pose;
std::ofstream peoplePositions;
move_base_msgs::MoveBaseGoal patrolGoal;

std::vector<move_base_msgs::MoveBaseGoal> locations;
int currLocation = 0;
int numLocations = 0;
ros::Publisher turn_pub;


void botPosCallBack(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr &msg) {
  bot_pose = msg->pose.pose;
  iKnowWhereIAm = true;
}


bool whereTheFAmI() {
  ros::Rate loop_rate(100);
  while(ros::ok()) {
    ros::spinOnce();
    loop_rate.sleep();
    if (iKnowWhereIAm) {
      break;
    }
  }

  return true;
}

void rotateBot()
{
	ROS_INFO("INSIDE ROTATE BOT\n");
	for (int i = 0; i < 3; i++) {
		ros::spinOnce();
		ROS_INFO("ROTATE #: %d\n", i);
		

		actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> ac("move_base", true);
		ac.waitForServer();
		move_base_msgs::MoveBaseGoal rotateGoal;
		rotateGoal.target_pose.header.stamp = ros::Time::now();
	    rotateGoal.target_pose.header.frame_id = "/map";
	    
	    rotateGoal.target_pose.pose.position.x = bot_pose.position.x;
	    rotateGoal.target_pose.pose.position.y = bot_pose.position.y;
	    rotateGoal.target_pose.pose.position.z = 0.0;
	    rotateGoal.target_pose.pose.orientation = tf::createQuaternionMsgFromYaw(
	    				tf::getYaw(bot_pose.orientation)+(2*3.14)/3);

	    ac.sendGoal(rotateGoal);
	    ac.waitForResult();

	  	std::string package_path = ros::package::getPath("guardbot");
		std::string command = "python3 " + package_path + "/src/recognizer.py";
	    const char* conv_command = command.c_str();
	    system(conv_command);
	}


}

int move_turtle_bot ()
  
  {
  	while(ros::ok()) {
  		

	actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> ac("move_base",true);
	ac.waitForServer(); //wait to make sure the service is there -- tihs has to be here even if you're use the service is already running

	ac.sendGoal(locations[currLocation]);
	    
    //block until the action is completed
    ROS_INFO("Going to location: %d\n", currLocation);
    bool finished_before_timeout = ac.waitForResult(ros::Duration(60.0));

   if (finished_before_timeout)
    {
      actionlib::SimpleClientGoalState state = ac.getState();
      ROS_INFO("Patrol Action finished: %s",state.toString().c_str());
    }
    else {
      ROS_INFO("Patrol Action did not finish before the time out.");
    }

	  if (currLocation + 1 == numLocations) {
	  	currLocation = 0;
	  } else {
	  	currLocation++;
	  }
	  rotateBot();
		
	}
  return 0;
}


int main(int argc, char **argv)
{
  	ros::init(argc, argv, "guard");
  	ros::NodeHandle n;
    
	std::string package_path = ros::package::getPath("guardbot");
    std::string location_path = package_path + "/locations.txt";
	std::ifstream infile(location_path.c_str());
	double x, y;
	while(infile >> x >> y) 
	{
		numLocations++;
		move_base_msgs::MoveBaseGoal location;
		location.target_pose.header.stamp = ros::Time::now();
	    location.target_pose.header.frame_id = "/map";
	    
	    location.target_pose.pose.position.x = x;
	    location.target_pose.pose.position.y = y;
	    location.target_pose.pose.position.z = 0.0;
	    location.target_pose.pose.orientation = tf::createQuaternionMsgFromYaw(0);
	    locations.push_back(location);
	}



  bool saw_person = false; 
  actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> ac("move_base",true);
  ac.waitForServer(); 

  ros::Subscriber me_sub     = n.subscribe("amcl_pose", 1000, botPosCallBack);

  whereTheFAmI();
  move_turtle_bot();

  return 0;
}

