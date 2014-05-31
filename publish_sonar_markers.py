import rospy
import numpy as np
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

rospy.init_node('publish_sonar_markers')
marker_pub = rospy.Publisher('sonar_markers', Marker, latch=True)

# create some fake data of the form (x, y, z, got_return) where
# got_return is a bool
data = []
for x in np.arange(-1.0, 1.0, 0.1):
    for y in np.arange(-1.0, 1.0, 0.1):
        for z in np.arange(-1.0, 1.0, 0.1):
            got_return = (x**2 + y**2 + z**2)**0.5 < 0.5
            data.append((x, y, z, got_return))


# create rviz markers for the data
positive_marker = Marker()
positive_marker.type = Marker.SPHERE_LIST
positive_marker.ns = 'positive_readings'
positive_marker.action = Marker.ADD
positive_marker.header.stamp = rospy.Time(0)
positive_marker.header.frame_id = 'map'
positive_marker.pose.orientation.w = 1.0
positive_marker.scale.x = 0.04
positive_marker.scale.y = 0.04
positive_marker.scale.z = 0.04
positive_marker.color.a = 1.0
positive_marker.color.r = 0.0
positive_marker.color.g = 1.0
positive_marker.color.b = 0.0

negative_marker = Marker()
negative_marker.type = Marker.SPHERE_LIST
negative_marker.ns = 'negative_readings'
negative_marker.action = Marker.ADD
negative_marker.header.stamp = rospy.Time(0)
negative_marker.header.frame_id = 'map'
negative_marker.pose.orientation.w = 1.0
negative_marker.scale.x = 0.04
negative_marker.scale.y = 0.04
negative_marker.scale.z = 0.04
negative_marker.color.a = 1.0
negative_marker.color.r = 1.0
negative_marker.color.g = 0.0
negative_marker.color.b = 0.0
for (x, y, z, got_return) in data:
    if got_return:
        print x, y, z
        positive_marker.points.append(Point(x, y, z))
    else:
        print 'neg', x, y, z
        negative_marker.points.append(Point(x, y, z))

# publish the markers
r = rospy.Rate(10)
while not rospy.is_shutdown():
    marker_pub.publish(positive_marker)
    marker_pub.publish(negative_marker)
    r.sleep()

