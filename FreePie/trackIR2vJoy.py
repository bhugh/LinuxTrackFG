###############################################################
#TrackIR to vJoy device, using freePie
#
#Source: hamzaalloush, https://forum.flightgear.org/viewtopic.php?f=24&t=28718
#

import sys

def toIntSafe(value):
    if value > sys.maxint: return sys.maxint
    if value < -sys.maxint: return -sys.maxint
    return value

def update():
   yaw = filters.mapRange(trackIR.yaw, -90, 90, -vJoy[0].axisMax, vJoy[0].axisMax)
   pitch = filters.mapRange(trackIR.pitch, -90, 90, -vJoy[0].axisMax, vJoy[0].axisMax)
   roll = filters.mapRange(trackIR.roll, -120, 120, -vJoy[0].axisMax, vJoy[0].axisMax)
   side = filters.mapRange(trackIR.x, -120, 120, -vJoy[0].axisMax, vJoy[0].axisMax)
   zoom = filters.mapRange(trackIR.z, -120, 120, -vJoy[0].axisMax, vJoy[0].axisMax)
   updown = filters.mapRange(trackIR.y, -120, 120, -vJoy[0].axisMax, vJoy[0].axisMax)

   vJoy[0].x = toIntSafe(yaw)
   vJoy[0].y = toIntSafe(pitch)
   vJoy[0].z = toIntSafe(roll)
   vJoy[0].rx = toIntSafe(side)
   vJoy[0].rz = toIntSafe(zoom)
   vJoy[0].ry = toIntSafe(updown)
   vJoy[0].slider = toIntSafe(updown)

if starting:
    trackIR.update += update
    
diagnostics.watch(trackIR.x)
diagnostics.watch(trackIR.y)
diagnostics.watch(trackIR.z)
diagnostics.watch(trackIR.yaw)
diagnostics.watch(trackIR.pitch)
diagnostics.watch(trackIR.roll)