# DoorStatus
**It can be used to trigger alarms if the door is opened at specific times(night or weekends etc.)**


1. Select the video input in Door_Detection_main.py(**line 41**) i.e. Live Camera or Saved Video file.

2. Run **Door_Detection_main.py**.

3. It is assumed that the door is Closed in the 1st frame which is taken as the refrence frame.

4. Select the Region of Interest to monitor for changes by drawing on the frame, press 'c' to select or 'r' to draw again. I'd suggest to select the upper corner of the door and a small region such that no moving object other than the door comes in the region.

5. The Status along with date and time is displayed above the Video feed and the Opening and Closing times are also saved in 'Output.txt' in the working directory.



>This approach uses background subtraction in the ROI with the 1st frame as the reference frame.
>The disadvantage it has is that it responds to all lighting changes, I've set a thresold for change but major changes in lighting such as flashing directly on the camera will still be registered as a DoorOpenEvent but smaller lighting changes such as day-night transition can be taken into account by updating the refrence frame after specific time intervals.
