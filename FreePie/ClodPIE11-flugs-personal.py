############################################################################
##ClodPIE: Cliffs of Dover/EDTracker View & Movement Enhancement with FreePIE
##by Brent Hugh
##
##Version 1.1
##
##brent@brenthugh.com - or contact via the forums at http://twcclan.com - flug
##
##See this file, included in the distribution, for detailed instructions,
##including installation, use, and customization:
##
##  README-CLOD-FreePIE-EDTracker-vJoy.txt
##
##See numerous important user customization options below.
##
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
##
##
import random, time
from System import Int16
from threading import Timer
import ctypes  # An included library with Python install.

global yaw
global pitch
global roll
global lastYaw
global x
global y
global z
global edtracker, joystickinput, jipov, enabled
global xmove, ymove, zmove, savexmove, saveymove, savezmove, savevibmovetime, ZoomInKey, ZoomOutKey, saveME109Toggle, ME109Toggle
    
if starting:

	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	#system.setThreadTiming(TimingTypes.ThreadYield)
	system.threadExecutionInterval = 1
	
	enabled = 1
	
	###########START OF USER CUSTOMIZATION OPTIONS####################
	##
	##
	############USER CUSTOMIZATION: JOYSTICK/EDTRACKER CONFIGURATION
	##
	##This is the most important customization section. You must enter the exact
	##name of your devices as shown in the "Game Controllers" section in your
	##system settings. "EDTracker Pro" is probably the same for every EDTracker.
	##But you will need to look up any other Joystick you want to use as input
	##and enter its name in place of "Sidewinder Force Feedback 2 Joystick"
	##
	##Alternatively, you can simply use integers 0,1,2 etc to specify the 
	##joystick. In that case you are at the mercy of Windows, which decides 
	##which is numbered 0,1,2,3 etc.
	##
	##If  you don't have an input joystick, you can still use the program--
	##you just won't have access to the joystick buttons or hat for input. 
	##You can use the keyboard instead.
	##
	##If you don't have an EDTracker you can still use the program--you will
	##still have access to the key and joystick button movement features, just 
	##none of the special EDTracker movement features
	##
	##Note that EDTracker is considered internally by Windows to be a type 
	##of joystick. This means you could specify any other joystick here 
	##and use it as a pseudo headtracker
	##
	inputtracker="EDTracker Pro" #edtracker to use.  Enter name as found in "Game Controllers" system settings. Note that windows sees EDTracker as a "joystick"		
	inputjoystick="SideWinder Force Feedback 2 Joystick" #joystick to use for input (use for button input etc).  Enter name as found in "Game Controllers" system settings			
	
	#inputtracker=0 #Example of specifying inputtracker as an integer index
	#inputjoystick=0 #Example of specifying input joystick as an integer index
	
	############USER CUSTOMIZATION: KEYBOARD SHORTCUTS 
	##
	##You can change keys below--for example, the current Reset Key is F1,
	##which is shown in the code this way:
	##
	##    return keyboard.getKeyDown(Key.F1)
	##
	## If you'd like to use F2 instead, simply type "F2" in place of F1, like this:
	##     return keyboard.getKeyDown(Key.F2)
	## 
	##A full list of available inputs, including the names for all keyboard keys
	##and joystick buttons, is online here:
	##
	##  https://github.com/AndersMalmgren/FreePIE/wiki/Reference
  ##
  ## If you want to completely disable a function--so that it isn't associated with
  ## any keyboard key or joystick button--just return the value 0, like this:
  ##
	##   PreventLeantoKey(): return 0
  ##
	#Note that you can use a keyboard key, a joystick button, OR both/either
	##to trigger. See examples below under JOYSTICK/KEYBOARD SHORTCUTS
	##
	def ResetKey(): return keyboard.getKeyDown(Key.F1) #resets all modes (except ME109 mode); I set this to be the same as my Opentrack reset key
	def LeantoKey(): return keyboard.getKeyDown(Key.A)
	def PreventLeantoKey(): return keyboard.getKeyDown(Key.S)
	def PreventLeantoToggleKey(): return keyboard.getPressed(Key.LeftShift)
	def VibrateLeantoToggleKey(): return ( keyboard.getKeyDown(Key.LeftControl) and keyboard.getKeyDown(Key.LeftAlt) and keyboard.getPressed(Key.D0))
	def Tab71Key(): return keyboard.getPressed(Key.F4)
	def Tab41Key(): return keyboard.getPressed(Key.F5)			
	def Tab42Key(): return keyboard.getPressed(Key.F6)		
	def Tab411Key(): return keyboard.getPressed(Key.F7)		
	def Tab72Key(): return keyboard.getPressed(Key.F8)		
	def ME109ToggleKey(): return ( keyboard.getKeyDown(Key.LeftControl) and keyboard.getPressed(Key.D9))  #Ctrl-9 for 109 mode
	
	############USER CUSTOMIZATION: JOYSTICK/KEYBOARD SHORTCUTS
	##
	##joystickinput.getPressed(0) gets joystick button 1, etc.  
	##
	##Note use of this programming idiom: (joystickinput and joystickinput.getPressed(0))
	##Reason: If no joystick exists we set joystickinput=0 so that the joystickinput.getPressed(0) is never accessed.
	##This prevents runtime errors when no joystick is present.
	##
	##jipov is "joystick input pov" and ranges from 0 to 35999. 0=up,9000=right, 18000=down, 27000=left, etc.
	##If the joystick hat is not in use, or no joystick exists, jipov is set to -1
	##
	##Key.D1 is the digit '1' on the top row of the keyboard. Key.NumberPad1 is
	##the '1' key on the number pad.  Full list at 
	##  
	##  https://github.com/AndersMalmgren/FreePIE/wiki/Reference
	##
	##Combine keys/buttons simply using logical 'or', as below. Scripting is in python.  More info at:
	##
	##   https://github.com/AndersMalmgren/FreePIE/wiki
	##  
	def LeantoToggleKey(): return keyboard.getPressed(Key.CapsLock) or (joystickinput and joystickinput.getPressed(0) and not joystickinput.getDown(2) and not joystickinput.getDown(3))
	def UpKey(): return keyboard.getKeyDown(Key.D1)# or jipov >= 31500 or ( jipov <= 4500 and jipov >=0 )
	def DownKey(): return keyboard.getKeyDown(Key.D2)# or (jipov >= 13500 and jipov <= 22500)
	
	def LeftKey(): return keyboard.getKeyDown(Key.Q)# or (jipov >= 22500 and jipov <= 31500)
	def RightKey(): return keyboard.getKeyDown(Key.W)#  or (jipov >= 4500 and jipov <= 13500)
	
	def ZoomInKeyStart(): return (joystickinput and joystickinput.getPressed(3))
	def ZoomInKeyHold(): return (joystickinput and joystickinput.getDown(3))
	ZoomInKey=Key.Equals
	def ZoomOutKeyStart(): return (joystickinput and joystickinput.getPressed(2))
	def ZoomOutKeyHold(): return (joystickinput and joystickinput.getDown(2))
	ZoomOutKey=Key.Minus
	
	

	############USER CUSTOMIZATION: ME109 MODE
	##
	ME109Toggle = 0 #ME109 mode is off initially (0).  Turn turn ME109 mode ON by default, just change 0 to 1.
	##ME109 mode moves your viewport slightly rightwards, so that 
	##the pilot is aligned with the ME109 gunsight. You can adjust the 
	##relevant parameters here:
	##

	ME109xcenter = -200 #amount to shift right in ME109 leaned-back position
	ME109xmove = -700 #amount to shift right in ME109 leaned-in-to-gunsight position


	############USER CUSTOMIZATION: ADVANCED OPTIONS
	##
	##Most users won't need to change the options below, but they are easy
	##to adjust if you would like.
	##
	##These options adjust how far the movement is in up/down/left/right/forward
	##/back directions, where the centerpoint is located, how far the 
	##ME109 right-offset is, what angles various left/right/up/down/etc movements
	##trigger at, what multiplier is used to translate edtracker to vJoy, 
	##and so on.
	##
	##If you would like to use a different input device than EDTracker, a 
	##different output devices than vJoy (combined with Opentrack), or other
	##more complex mods, you can probably set all that up in this section,
	##or a combination of changes here and in the main code below.
	##
 
	
	xmove = 1500 #amount to shift in R/L direction; varies -xmove to xmove
	ymove = 600 #amount to shift in up/down direction; varies -ymove to ymove
	zmove = 3000 #amount to shift in forward/back direction; varies 0 to -zmove
	VibrateLeantoFramerate = 0.03 #1/60 seconds is same as target frame rate for most CLOD users/most monitors. Use a decimal number here as a fraction like 1/20 will round to 0.
	
  
	#center position
	def xcenter(): 		
	    if (ME109Toggle): return ME109xcenter
	    else: return 0
	def ycenter(): return 0
	def zcenter(): return 0
	savexmove = zcenter()
	saveymove = ycenter()
	savezmove = zcenter()
	savevibmovetime = 0
	saveME109Toggle=ME109Toggle
	
	edtrackerScaleFactor = 16 #Scale factor required when transferring from EdTracker to vJoy inputs.  Probably just 8 bit vs 16 bit values.
	
	def LeftTrigger(): return (trackIR.yaw < -60)
	def RightTrigger(): return (trackIR.yaw > 60)	
	 
	#We trigger up at a certain point in lean into gunsight so that we can see over the nose a bit better
	def UpTrigger(): return (trackIR.pitch < -10)	
	#def UpTrigger(): return 0 # Use this to disable UpTrigger
	def DownTrigger(): return 0	
	
	#def LeantoForwardTrigger(): return  ( (trackIR.pitch < -1.2) ) # lean forward into gunsite
	def LeantoForwardTrigger(): return  0 # disabling this for now because the joystick button works so much better!
	def LeantoBackwardTrigger(): return  ( abs(trackIR.yaw) > 150 ) # look backward - we can see around the backplate better if we lean forward while looking back
	def PreventLeantoTrigger(): return ( abs(trackIR.yaw)>60 and abs(trackIR.yaw) < 150)   # same as Left/RightTriggers on the low side & LeantoBackwardTrigger yaw on the high side
	LeantoToggle = 0
	PreventLeantoToggle = 0
	VibrateLeantoToggle = 0

	###########END OF USER CUSTOMIZATION OPTIONS####################
	##
	##You are welcome to customize the code below, but warning! All the 
	##easy stuff is above this line!
	##
	try:
		edtracker = joystick[inputtracker] 
	except:
		ctypes.windll.user32.MessageBoxW(0, "No EDTracker was found. You can edit the .py file near line 67 to identify your EDTracker, or simply proceed without an EDTracker", "No EDTracker", 1)
		edtracker = 0
	try:	
		joystickinput = joystick [inputjoystick]
	except:
		try:
	  		joystickinput = joystick [0]  #Use default joystick
	  		ctypes.windll.user32.MessageBoxW(0, "Using the default joystick as the input joystick. To change this, edit the .py file near line 63.", "Default Input Joystick", 1)
		except:	
			ctypes.windll.user32.MessageBoxW(0, "No input joystick was found. You can edit the .py file near line 67 to identify your joystick, or simply proceed without joystick input", "No joystick", 1)
			joystickinput=0
#diagnostics.watch(ZoomOutKeyHold())
#diagnostics.watch(ZoomInKeyHold())
#diagnostics.watch(joystickinput.getDown(2))
#diagnostics.watch(LeftTrigger())
#diagnostics.watch(RightTrigger())
#diagnostics.watch(ME109Toggle)
#diagnostics.watch(saveME109Toggle)
#diagnostics.watch(LeantoToggle)
#diagnostics.watch(PreventLeantoToggle)
#diagnostics.watch(VibrateLeantoToggle)
#diagnostics.watch(savexmove)
#diagnostics.watch(savevibmovetime)
diagnostics.watch(trackIR.x)
diagnostics.watch(trackIR.y)
diagnostics.watch(trackIR.z)
diagnostics.watch(trackIR.yaw)
diagnostics.watch(trackIR.pitch)
diagnostics.watch(trackIR.roll)
diagnostics.watch(freeTrack.x)
diagnostics.watch(freeTrack.y)
diagnostics.watch(freeTrack.z)
diagnostics.watch(freeTrack.yaw)
diagnostics.watch(freeTrack.pitch)
diagnostics.watch(freeTrack.roll)
#diagnostics.watch(edtracker.x)
#diagnostics.watch(edtracker.y)
#diagnostics.watch(edtracker.z)
diagnostics.watch(vJoy[0].x)
diagnostics.watch(vJoy[0].y)
diagnostics.watch(vJoy[0].z)
diagnostics.watch(vJoy[0].rx)
diagnostics.watch(vJoy[0].ry)
diagnostics.watch(vJoy[0].slider)
diagnostics.watch(vJoy[0].rz)

# EDTRACKER TO	 to vJoy
if edtracker: 
	vJoy[0].x = edtracker.x * edtrackerScaleFactor 
	vJoy[0].y = edtracker.y * edtrackerScaleFactor 
	vJoy[0].z = edtracker.z * edtrackerScaleFactor
	#trackIR.yaw = edtracker.x 
	#trackIR.pitch = edtracker.y 
	#trackIR.roll = edtracker.z
	#freeTrack.yaw = edtracker.x 
	#freeTrack.pitch = edtracker.y 
	#freeTrack.roll = edtracker.z
	
#if trackIR and vJoy[1]:
	
	#vJoy[1].x = trackIR.x
	#vJoy[1].y = trackIR.y
	#vJoy[1].z = trackIR.z
	#vJoy[1].rx = trackIR.yaw
	#vJoy[1].ry = trackIR.pitch
	#vJoy[1].slider = trackIR.pitch
	#vJoy[1].rz = trackIR.roll
	

#pov values: U 0, 4500, R 9000, 13500, D 18000, 22500, L 27000, 31500, 0
#if input joystick doesn't exist, we set joystickinput=0, so we test for that first & if =0, just return -1 always
if (joystickinput): jipov = joystickinput.pov[0]
else: jipov=-1

#diagnostics.watch(jipov)

#move left/right
vjrx = xcenter()
if (LeftKey() or LeftTrigger() and not RightKey()): vjrx = xmove
elif (RightKey() or (RightTrigger() and not LeftKey()) ): vjrx = -xmove

vjry = ycenter()

#up/down
if (UpKey()): vjry = ymove
if (UpTrigger() and not LeantoToggle): vjry = ymove #UpTrigger is separate from UpKey so can adjust upward move during lean-in here separately if necessary
if (DownKey() or DownTrigger()): vjry = -ymove

#lean to gunsight
# lean to gunsight is activated by tab OR leaning in and negated by leftshift. Also if 1 is pressed (to move up) lean in is suppressed, bec. leaning in gets your head stuck on the roof, keeping it from moving up
# Lean to gunsight also restricts from moving R or L to keep centered on the gunsights
if (LeantoKey() or  LeantoToggle or ( ((LeantoForwardTrigger() and not UpKey()) or LeantoBackwardTrigger()) and not PreventLeantoTrigger() ) and not PreventLeantoKey() and not PreventLeantoToggle): 
    vjrz = -zmove
    if (not DownKey() and vjry < ycenter() ): vjry = ycenter() #lean into gunsight & duck don't really work together
    if (not LeftKey() and not RightKey() and not LeantoBackwardTrigger()): #when we lean to gunsight, we want to stay centered, but if user is pressing keys that takes precedence 
    	if (ME109Toggle): vjrx = ME109xmove;
    	else: vjrx = xcenter()
else: vjrz = zcenter()  

#vibrate - idea is to emulate the "transparent" quality narrow window dividers etc have when viewed with two eyes (vs "solid" when viewed with one eye)
if VibrateLeantoToggle:
  currtime=time.time()
  #diagnostics.watch(currtime)
  if ((currtime - savevibmovetime) > VibrateLeantoFramerate):
     if (savexmove >= xmove/4):
     	vjrx = vjrx - xmove/4
     	vjry = vjry - ymove/4
     	vjrz = vjrz - zmove/4
     else:
     	vjrx = vjrx + xmove/4
     	vjry = vjry + ymove/4
     	vjrz = vjrz + zmove/4
     savexmove=vjrx
     saveymove=vjry
     savezmove=vjrz
     savevibmovetime=currtime
  else:
	vjrx=savexmove
	vjry=saveymove
	vjrz=savezmove	
	
  
#prevents lean to gunsight/leanforward
#(There isn't any point in actually moving backwards as there is no room to do so. Instead, we just prevent forward movement,
#which is useful in some situations, because normal TrackIR/EdTracker movements lean us forward sometimes when we don't want it.
if (PreventLeantoKey() or PreventLeantoToggle): vjrz = zcenter()    

vJoy[0].rx = vjrx
vJoy[0].ry = vjry
vJoy[0].slider = vjry
vJoy[0].rz = vjrz 
   
#toggle ME109 mode on or off
#this does a slight right lean when leaning to gunsight to line up with the ME109 gunsights
#Note that "saveME109Toggle" is the real mode, as selected by user. ME109Toggle is the 'operational' condition but certain things (like a requested reset) will switch it off temporarily
if ME109ToggleKey(): 
	saveME109Toggle = not saveME109Toggle
	ME109Toggle=saveME109Toggle
   
#toggle LeantoGunsight on or off
if LeantoToggleKey(): 
	LeantoToggle = not LeantoToggle
	if (LeantoToggle): 
		PreventLeantoToggle=0 #can't have them both toggled simultaneously
		VibrateLeantoToggle = 0


#toggle PreventLeantoGunsight on or off
if PreventLeantoToggleKey(): 
	PreventLeantoToggle = not PreventLeantoToggle
	if (PreventLeantoToggle): 
		LeantoToggle=0 #can't have them both toggled simultaneously
		VibrateLeantoToggle = 0

#toggle PreventLeantoGunsight on or off
if VibrateLeantoToggleKey():
	VibrateLeantoToggle = not VibrateLeantoToggle
	if (VibrateLeantoToggle): 
		LeantoToggle=0 #can't have them both toggled simultaneously
		PreventLeantoToggle = 0

def restoreME109Toggle ():
	ME109Toggle=saveME109Toggle
	ME109Toggle=1
	vJoy[0].rx = xcenter()
	vJoy[0].ry = ycenter()
	vJoy[0].slider = ycenter()
	vJoy[0].rz = zcenter()

if ResetKey():
	PreventLeantoToggle = 0
	LeantoToggle = 0
	VibrateLeantoToggle = 0
	
	#whatever the current state of the joystick is, Opentrack will consider to be the "center" when
	#the reset key is pressed.  So we make sure this is 0,0,0 and not something else
	#If we don't do this, strange bugs ensue
	
	#OK, there is a bug here because Opentrack assumes that current position is 0,0,0 and resets to that.  BUT if we are in ME109 mode, our current position is something like -700,0,0.  So it resets that to 0,0,0.  Result is that the more times we hit F1 in ME109 mode, the further left we move in the cockpit.  Solution is the turn off ME109 mode temporarily in Reset, then turn it back on a bit later.
	#saveME109Toggle= (ME109Toggle or saveME109Toggle)  #don't need to save it as now saveME109Toggle is the 'real' ME109 mode as requested by user.  We can fiddle with ME109 as needed, then just set it back to reflect saveME109Toggle
	ME109Toggle=0
		
	vJoy[0].rx = xcenter()
	vJoy[0].ry = ycenter()
	vJoy[0].slider = ycenter()
	vJoy[0].rz = zcenter()
	time.sleep (0.6) #give some time for the recenter, freezing everything in place
	ME109Toggle=saveME109Toggle
	#restore the ME109mode 1 second later
	#Note that there are potential bugs here if F1 is pressed more often than once per second
	#t = Timer(.1, restoreME109Toggle)
	#t.start()
	
	
#Tab-7-1 with one key 
#Also, this is an example of how keys can be reprogrammed using FreePIE
if Tab71Key():
	KeyDownUp(Key.Tab)	
	def D7(): KeyDownUp(Key.D7)
	def D1(): KeyDownUp(Key.D1)	
	t = Timer(0.1, D7)
	t.start()
	u = Timer(0.2, D1)
	u.start()

#Tab-7-1 with one key 
#Also, this is an example of how keys can be reprogrammed using FreePIE
if Tab72Key():
	KeyDownUp(Key.Tab)	
	def D7(): KeyDownUp(Key.D7)
	def D2(): KeyDownUp(Key.D2)	
	t = Timer(0.1, D7)
	t.start()
	u = Timer(0.2, D2)
	u.start()


#Tab-4-1 with one key 
#Also, this is an example of how keys can be reprogrammed using FreePIE
if Tab411Key():
	KeyDownUp(Key.Tab)	
	def D4(): KeyDownUp(Key.D4)
	def D1(): KeyDownUp(Key.D1)	
	def D2(): KeyDownUp(Key.D2)	
	def Tab(): KeyDownUp(Key.Tab)	
	t = Timer(0.1, D4)
	t.start()
	t = Timer(0.2, D1)
	t.start()
	t = Timer(0.3, D1)
	t.start()
	#t = Timer(0.4, Tab)
	#t.start()

#A few variants, because different servers . . . 
if Tab41Key():
	KeyDownUp(Key.Tab)	
	def D4(): KeyDownUp(Key.D4)
	def D1(): KeyDownUp(Key.D1)	
	def D2(): KeyDownUp(Key.D2)	
	def Tab(): KeyDownUp(Key.Tab)	
	t = Timer(0.1, D4)
	t.start()
	t = Timer(0.2, D1)
	t.start()
	#t = Timer(0.3, D1)
	#t.start()
	t = Timer(0.4, Tab)
	t.start()

#A few variants, because different servers . . . 
if Tab42Key():
	KeyDownUp(Key.Tab)	
	def D4(): KeyDownUp(Key.D4)
	def D1(): KeyDownUp(Key.D1)	
	def D2(): KeyDownUp(Key.D2)	
	def Tab(): KeyDownUp(Key.Tab)	
	t = Timer(0.1, D4)
	t.start()
	t = Timer(0.2, D2)
	t.start()
	#t = Timer(0.3, D1)
	#t.start()
	t = Timer(0.4, Tab)
	t.start()
	
def KeyDownUp(K):
	keyboard.setKeyDown(K)
	keyboard.setKeyUp(K)	
		
if ZoomInKeyStart():
	def KeyPressIf(): 
		if (ZoomInKeyHold()): KeyDownUp(ZoomInKey)
	for x in range (1,20):
			diagnostics.watch(x)			
			t = Timer(0.02*x + 0.1, KeyPressIf)
			t.start()
	
if ZoomOutKeyStart():	
	def KeyPressIf(): 
		if (ZoomOutKeyHold()): KeyDownUp(ZoomOutKey)
	for x in range (1,20):
			diagnostics.watch(x)			
			t = Timer(0.02*x + 0.1, KeyPressIf)
			t.start()
	#def D4(): KeyDownUp(Key.D4)
	#def D1(): KeyDownUp(Key.D1)	
	#t = Timer(0.1, D4)
	#t.start()
	#u = Timer(0.2, D1)
	#u.start()
	#KeyDownUp(Key.F7)
	