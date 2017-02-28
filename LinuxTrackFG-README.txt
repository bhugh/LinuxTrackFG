LinuxTrackFG - README

brent@brenthugh.com 

LinuxTrackFG is a script that allows just about any headtracking type device to 
be used in Flightgear.

Specifically, it allows any headtracking type device that can output position 
and rotation as a virtual joystick, to be used in FlightGear.  However, below
techniques are described that allow most any common headtracker (TrackIR,
EDTracker, etc etc etc) to translate its output to a virtual joystick device.

LinuxTrackFG may or may not be the BEST way to accomplish this task, but it is 
A way, and it works.

LinuxTrackFG is a fork of the portions of the LinuxTrack software related to 
FlightGear. Note the the files from LinuxTrack included and modified here are 
just a very, very small portion of the overall LinuxTrack progrect.  The only 
files included here are those related directly to the FlightGear interface.

LinuxTrack by uglyDwarf can be found here:

  https://github.com/uglyDwarf/linuxtrack

The headtracking devices and software that could work with this type of setup 
include:

 EDTracker - appears as a joystick device, making it very easy to work with
 OpenTrack - used with many different types of headtracking systems
 FreePIE + vJoy - can taken a variety of different input from Headtrackers, 
   keyboard, joystick, whatever, and turn it all into joystick output giving 
   head position)
 Probably lots more
 
 Ideas about how to set up various specific systems below.
 
 BASIC SETUP
 
 1. Copy directories Input, Nasal, and Protocol to your FGDATA directory 
(similar directories should already exist in FGDATA).
 
 2. Add these lines to your Flightgear command line (most of us now do 
this in 'Start Flightgear' application, tab "Settings" and section 
"Additional Options"):

--prop:/sim/linuxtrack/enabled=1
--prop:/sim/linuxtrack/track-all=1

 3. In the Input\Joysticks\LinuxTrack directory find the file 
uinput-LinuxTrack.xml and edit it with a text editor.  You will see 
lines like this:
 
 	<name>vJoy Device</name>
  <name>EDTracker Pro</name>
  
Edit this section so that you have just one name, and it is the name of the 
joystick device that carries your headtracking data.  For instance I use 
EDTracker but then I massage the data in various ways in FreePIE, which outputs 
it to vJoy.  So my <name> section looks like this:

	<name>vJoy Device</name>

4. WARNING: Flightgear now auto-creates its own joystick config files and saves 
them in a place like this: 
  C:\Users\YOURCOMPUTERNAME\AppData\Roaming\flightgear.org\Input\Joysticks 
  
(Under Linux & Mac it is in a different specific location, but is a similar 
type app data directory.)

This joystick config file, if it exists, will take precedence over the file 
you just installed in <FGdata>\Input\Joysticks\LinuxTrack.  So you may need 
to delete or remove the relevant auto-created joystick file in 
C:\Users\YOURCOMPUTERNAME\AppData\Roaming\flightgear.org\Input\Joysticks 
in order to get the FGData version to work correctly.

Note that simply renaming the file won't help--move it to another directory 
or delete it altogether.

As I was setting up my system, files of this type kept getting re-created by 
FlightGear--presumably when I went into the Joystick menu and accidentally 
clicked something.  Just be aware of this and check/remove these files if there 
is interference.


BASIC EDTRACKER SETUP

Set up as above, except that joystick name in uinput-LinuxTrack.xml will be:
 
 	<name>EDTracker Pro</name>
  
This will allow only pitch/roll/yaw movements with your EDTracker--no x/y/z 
movements.  However, it is very simple and it works.


ADVANCED EDTRACKER SETUP

1. Set up as Basic Setup above, including "<name>vJoy Device</name>".

2. Set up vJoy.  See info here: https://forum.flightgear.org/viewtopic.php?f=24&t=28718

3A. Set up OpenTrack. Input = joystick (EDTracker Pro). Output=vjoystick.  
Then you'll need to edit the <name> line above to be "<name>vjoystick</name>" 
or whatever the exact name of that device is in windows joystick setup.

3B. OR Set up OpenTrack. Input = joystick (EDTracker Pro). Output = FlightGear. 
Follow the directions in the OpenTrack program directory contrib\FlightGear 
(and actually this doesn't even require or use LinuxTrack at all . . . )

3C. OR Set up OpenTrack Input = joystick (EDTracker Pro). Output = freetrack 2.0 
Enhanced. Set up FreePIE (info here: https://forum.flightgear.org/viewtopic.php?f=24&t=28718 ). 
Run FreePIE with the trackIR2vJoy.py script included in the FreePIE directory.

I have successfully gotten 3C to work, but not 3A or 3B.  


TRACKIR SETUP

First, do Basic Setup as described above.

Then you can install FreePIE and vJoy, as described here:

https://forum.flightgear.org/viewtopic.php?f=24&t=28718

This setup is similar to the one described in that forum article, except that in 
place of FGCamera, we use LinuxTrackFG.  (I tried to use FGCamera but couldn't
get it to work.  LinuxTrackFG is my replacement solution.) 

In the FreePIE folder, you will find a FreePIE script, trackIR2vJoy.py, that 
will translate TrackIR to vJoy.  So your setup is:

 1. TrackIR
 2. FreePIE running ClodPIE11-generic.py
 3. vJoy
 4. LinuxTrack - set up as above, joystick name in uinput-LinuxTrack.xml will be:
 
 	<name>vJoy Device</name>


REALLY ADVANCED SETUP

I personally use a combo of these items and utilities:

 1. EDTracker Pro
 
 2. FreePIE - reads EDTracker Pro plus keyboard commands and outputs nice, 
useful head movements in 6 degrees of freedom, using script ClodPIE11-flugs-personal.py 
(included in FreePIE folder)
 
 3. vJoy - accepts FreePIE output & makes it available as as Windows standard joystick device
  
 4. OpenTrack - Joystick input set to vJoy, output set to freetrack 2.0 Enhanced; 
the freetrack output feeds back to FreePIE, allowing use of OpenTrack's very nice 
mapping & filtering options while also allowing some really nice movement tweaks 
and keyboard-controlled movement by FreePIE that OpenTrack can't do.
 
 5. LinuxTrack - set up as above under Basic Settings, joystick name in uinput-LinuxTrack.xml will be:
 
 	<name>vJoy Device</name>    
   
This seems complicated, but I use the same setup in IL2 Cliffs of Dover, DCS, 
Flightgear, and other similar games.  It adds really useful 6-degrees-of-
freedom capability to the 3-degrees-of-freedom EDTracker naturally has, and 
makes flying a lot more fun and less frustrating because you can move your head
a bit to look around posts and other obstacles in the cockpit.  You can use
keys 1,2,a,s etc to move your head, but the system also does 'auto-movements'. 
For example, if you look left, it auto-moves your head left.  Look right, 
auto-move to the right, etc.  So 99% of the time you can see what you need to
just by moving your head--no keys required.

The whole system and associated programs needed to run it (aside from LinuxTrackFG) 
are described here:

http://theairtacticalassaultgroup.com/forum/showthread.php?t=23974

If you want to try a similar setup but don't necessarily like my specific keyboard 
setup, you can try the included FreePIE script ClodPIE11-generic.py

 
-----

Many portions of this package are assembled from various freely available scripts 
and programs. For the portions written by me:

##Copyright (c) 2016 Brent Hugh
##
##The MIT License (MIT)
##
##Permission is hereby granted, free of charge, to any person obtaining a copy
##of this software and associated documentation files (the "Software"), to deal
##in the Software without restriction, including without limitation the rights
##to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the Software is
##furnished to do so, subject to the following conditions:
##
##The above copyright notice and this permission notice shall be included in
##all copies or substantial portions of the Software.  