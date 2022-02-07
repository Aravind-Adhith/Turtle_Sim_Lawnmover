import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time


PI = 3.1415926535897
x = 0
y = 0
yaw = 0


def poseCallback(pose_message):
    global x
    global y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


# this function is used for linear motion of the turtlesim and requires the speed,distance and direction of motion as input arguments
def move(speed, distance, is_forward):
    # declare a Twist message to send velocity commands
    velocity_message = Twist()
    # get current location
    global x, y
    x0 = x
    y0 = y

    print('x=', x, 'y=', y)
""""    
    # check the direction of motion
    if (is_forward):
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)

    distance_moved = 0.0
    loop_rate = rospy.Rate(10)  # we publish the velocity at 10 Hz (10 times a second)
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    while True:
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)

        loop_rate.sleep()

        # rospy.Duration(1.0)

        distance_moved = abs(0.5 * math.sqrt(((x - x0) ** 2) + ((y - y0) ** 2)))
        print
        distance_moved
        if not (distance_moved < distance):
            rospy.loginfo("reached")
            break

    # finally, stop the robot when the distance is moved
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)


def rotate(speed, angle, clockwise):

    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # Receiveing the user's input
    print("Let's rotate our robot")

    # Converting from angles to radians
    angular_speed = speed * 2 * PI / 360
    relative_angle = angle * 2 * PI / 360

    # We wont use linear components
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # Checking if our movement is CW or CCW
    if clockwise:
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)
    # Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while (current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1 - t0)

    # Forcing our robot to stop
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
"""

if __name__ == '__main__':
    try:

        rospy.init_node('turtlesim_motion_lawnmover', anonymous=True)

        # declare velocity publisher
        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        time.sleep(2)
        print("START")

        move(1.0, 2.0, True)  # forward
        """
        rotate(60, 90, False)
        # rotate((180/pi), 90, False)#anticlockwise rotation

        move(1.0, 1.0, True)  # forward
        rotate(60, 90, False)  # anticlockwise rotation

        move(1.0, 2.0, True)  # forward
        rotate(60, 90, True)  # clockwise rotation

        move(1.0, 1.0, True)  # forward
        rotate(60, 90, True)  # clockwise rotation

        move(1.0, 2.0, True)  # forward
        rotate(60, 90, False)  # anticlockwise rotation
        """
        print("END")


    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
