This file contains a video reader script that calls on the imageProcessor Script to perform any kind of image processing on a frame by frame basis. Currently appears to run in real time. Would be interesting to see with more complex math operations how slow it could get. 

=========================================IMPORTANT USAGE NOTES=================================================
As the os library is being used, it can mess up your directories if you're not careful. Will be adding error fetching capabilities soon. Here are a few things to note when running this script numerous times. 

1. After every run you will see a __pycache__ folder being generated in your directory. It's just left over memory stuff from the imageProcessor script. Delete that __pycache__ folder **everytime before** you run the main videoreader script.

2. The next thing to remember **for now**, is to delete the **/Frame_Dump/** folder each time **before you run the videoreader script** until I add the logic to just use the folder once it's generated.

3. You might need to empty your trash folder sometimes as it could take up memory. I used the car video as a test video. We can take a video of the actual object we want to track and use that to do image processing.
