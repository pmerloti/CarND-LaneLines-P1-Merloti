# # Lane Detector
[image1]: tarsnake.jpg

![tarsnake][image1]

## This is my first project from Udacity's Self Driving Car Nanodegree - Term 1.

This project was developed in Visual Studio 2017 and Python 3.6. With some minor changes it can be easily run in other platforms as well. For example, for saving video files Windows doesn't like the ```cv2.VideoWriter_fourcc(*'XDIV')```. Instead, we save video files using the ```'DIVX'``` encoding.

My project has two main entry points. ```main_OneFrame.py``` loads and processes one single image and makes things easy for debugging. The other is ```main_Video.py``` which loads a video sequence, applies the lane detection algorithm and plays the annotated video, while saving an output video file. All output files are checked in GitHub.

The pipeline is encapsulated in the ```LaneDetector``` class. In order to use it, you instantiate once, and for each image to be processed, call ```set_image(img)``` before calling the desired processing stage on the pipeline. The pipeline is composed of the following stages:

```
smooth()      #converts image to gray and apply gaussian blur
find_edges()  #applies Canny edge detection on smoothed image
find_lines()  #uses probabilistic Hough lines algorithm to find straight lines
find_lanes()  #makes sense of lines to find the two side lines
```

Given that the main use of ```LaneDetector``` class was learning the pipeline, it was designed in a way that by calling any stage of the pipeline causes all prior stages to execute. Each stage also saves a debugging image with raw output for given stage. Respectively, the images are:

```
gray_img      #input image converted to gray scale
blurred_img   #output of gaussian blur
edges_img     #binary image with raw edges_img
lines_img     #source image (color) with annotated raw edges after roi
lanes_img     #source image (color) with annotated lanes
```

Once all Hough lines are filtered, averaging is encapsulated in the ```RoadLanes``` class. The main idea is that once lines are identified to be in the right or left side of the road, we can average them to find the best representation of that line. An additional improvement is that the length of the line is used for a weighted average. One can observe that the most stable lines from a dashed lane line are the longer ones.