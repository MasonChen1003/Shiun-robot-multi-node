   ![image](Shiun_robot_icon.png)
   
# Shiun Robot (Micro:bit Biped robot)
Using Micro:bit + MiniPlan MiniPOW board(Micro:bit power extension board) to control the Shiun Robot

This extension will provide the basic motion for user to control the robot. 

Basic motion : 

Forward / Backward / Turn Left / Turn Right / Stop

## Code Example 
1. Define the offset value for 4-servo motors.  (P0 / P1 /P2)

   Note : Two SG90 motors share the same pin "P1".
   
   ![image](readme_1.jpg)
   
2. Assign the speed & motion to the robot. 

![image](readme_2.jpg)
![image](readme_3.jpg)

Javascipt example code : 
==============================================================================
MiniPOW.set_offset(3, -1, 4)

MiniPOW.motion(MiniPOW.snum.Middle, MiniPOW.dnum.Stop)

basic.forever(function () {
	
})



## License

Non-Commercial license.

Author : Mason Chen
https://www.facebook.com/mason.chen.1420

## Supported targets

* for PXT/microbit
(The metadata above is needed for package search.)

