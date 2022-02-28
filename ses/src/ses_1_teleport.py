#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import Spawn
from std_srvs.srv import Empty as EmptyServiceCall
import math
import time

yaw = 0
x = 0
y = 0


def poseCallback(pose_message):
    global x
    global y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


#Function for Linear movement
def displace(speed,distance):

    velocity = Twist()

    global x, y
    x0 = x
    y0 = y

    velocity.linear.x = abs(speed)

    distance_traversed = 0.0
    loop_rate = rospy.Rate(10)  # we publish the velocity at 10 Hz (10 times a second)
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    while True:

        velocity_publisher.publish(velocity)

        loop_rate.sleep()

        #print('X:',x,'Y:',y)
        distance_traversed = abs(math.sqrt(((x - x0) ** 2) + ((y - y0) ** 2)))
        if not (distance_traversed < distance):
            break

    # Stopping the motion
    velocity.linear.x = 0
    velocity_publisher.publish(velocity)


#Function for Rotation
def rotate(speed, angle, clockwise):
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    PI = 3.14

    # Converting from angles to radians
    angular_speed = speed * 2 * PI / 360
    relative_angle = angle * 2 * PI / 360


    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # Clockwise or Anticlockwise condition
    if clockwise:
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)

    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while (current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1 - t0)

    # Stopping the motion
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)


# Function to go to the specified(Origin) location
def gotoxy(fin_x, fin_y):
    # declare a Twist message to send velocity commands
    velocity_message = Twist()
    # get current location
    global x, y, yaw

    angle = math.atan2(fin_y - y, fin_x - x)
    angle = (angle - yaw) * 180 / 3.14

    if(angle < 0):
        rotate(90,-angle,True)
    else:
        rotate(90, angle, False)

    distance = math.sqrt(math.pow((fin_x - x),2) + math.pow((fin_y - y),2))

    displace(2,distance)

    if(angle < 0):
        rotate(90,-angle,False)
    else:
        rotate(90,angle,True)

    #print('Current Coordiantes:',x,y)
    

#Function to Form Pattern
def s_pattern(ref_x,ref_y,a,b):

    #Going to the Set Position
    #gotoxy(float(ref_x), float(ref_y))
    clear_background = rospy.ServiceProxy('clear', EmptyServiceCall)
    turtle1_teleport = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
    turtle1_teleport(float(ref_x),float(ref_y),0)
    clear_background()
    
    rospy.sleep(2.0)
    
    displace(1,float(a))
    rotate(90,90,False)
    displace(1,float(b))
    rotate(90,90,False)
    displace(1, float(a))
    rotate(90, 90, True)
    displace(1, float(b))
    rotate(90, 90, True)
    displace(1, float(a))


if __name__ == '__main__':
    try:
       
        rospy.init_node('turtlesim_motion_lawnmover', anonymous=True)
        
        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        time.sleep(2)
               
        print("Simulation Starts")


        ref_x = input("Enter the Starting X-Coordinate : ")
        ref_y = input("Enter the Starting Y-Coordinates : ")

        #To Check if entered coordinated in the region
        if (float(ref_x) >= 0 and float(ref_y) >= 0 and float(ref_x) <= 11.08 and float(ref_y) <= 11.08):

            a = input("Enter the Horizontal Traversal Distance :")
            b = input("Enter the Vertical Traversal Distance :")

            #To Check if the pattern can be formed in the workspace
            if( (float(ref_x)+float(a))>=11.08 and (float(ref_y)+float(b))>=11.08 ):
                print('Entered Traversal Values too Large...! Exiting Simulation')
            else:
                s_pattern(ref_x, ref_y, a, b)
        else:
            print('Entered Coordinates out of bounds...! Exiting Simulation')


        print("Simulation Ends")

    except rospy.ROSInterruptException: pass
    rospy.loginfo("node terminated.")
