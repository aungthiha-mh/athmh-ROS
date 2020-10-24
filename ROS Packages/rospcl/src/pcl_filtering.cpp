#include <ros/ros.h>
#include <pcl/point_cloud.h>
#include <pcl_ros/point_cloud.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/filters/statistical_outlier_removal.h>
#include <pcl/visualization/cloud_viewer.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl/io/pcd_io.h>

class cloudFiltering{
protected:
  ros::NodeHandle nh;
  ros::Subscriber pcl_sub;
  ros::Publisher pcl_pub;
  ros::Timer timer;
  pcl::visualization::CloudViewer viewer;

public:
  cloudFiltering() : viewer("Cloud Viewer Filtering")
  {
    pcl_sub = nh.subscribe("pcl_reading",1,&cloudFiltering::pclCallback,this);
    pcl_pub = nh.advertise<sensor_msgs::PointCloud2>("pcl_filtering",10);
    timer = nh.createTimer(ros::Duration(0.1),&cloudFiltering::timerCallback,this);
  }

  void pclCallback(const sensor_msgs::PointCloud2 &input)
  {
    pcl::PointCloud<pcl::PointXYZ> cloud;
    pcl::fromROSMsg(input,cloud);

    pcl::PointCloud<pcl::PointXYZ> cloud_filtered;

    pcl::StatisticalOutlierRemoval<pcl::PointXYZ> statRemover;
    statRemover.setInputCloud(cloud.makeShared());
    statRemover.setMeanK(10);
    statRemover.setStddevMulThresh(0.2);
    statRemover.filter(cloud_filtered);

    sensor_msgs::PointCloud2 output;
    pcl::toROSMsg(cloud_filtered,output);
    pcl_pub.publish(output);
    viewer.showCloud(cloud_filtered.makeShared());

  }

  void timerCallback(const ros::TimerEvent&){
    if(viewer.wasStopped()){
      ros::shutdown();
    }
  }

};

int main(int argc,char **argv){
  ros::init(argc,argv,"pcl_filtering_node");
  cloudFiltering visualizer;
  ros::spin();

}
