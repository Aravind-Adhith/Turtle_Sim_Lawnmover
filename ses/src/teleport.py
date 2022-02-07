import time

import rospy

from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import Spawn
from std_srvs.srv import Empty as EmptyServiceCall


rospy.init_node("teleporting_node")

clear_background = rospy.ServiceProxy('clear', EmptyServiceCall)

#spawn_turtle = rospy.ServiceProxy('spawn', Spawn)

#spawn_turtle(5,5,45, "turtle2")  #x,y,theta
#time.sleep(10)
#print('wait for 10 seconds...')


turtle1_teleport = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)

turtle1_teleport(2,2,0)

clear_background()

print('teleportation completed')
