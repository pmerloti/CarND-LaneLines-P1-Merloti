# **Finding Lane Lines on the Road**
---

The goals / steps of this project are the following:
1. Create a image processing pipeline that finds lane lines on the road
2. Test the pipeline on static images provided with project material
3. Create a video processor that applies pipeline to a video file and outputs an annotated video
4. Reflect on your work in a written report


[//]: # "Image References"

[image1]: ./LaneDetection/test_images/out_solidWhiteCurve.png
[image2]: ./LaneDetection/test_images/out_solidWhiteRight.png
[image3]: ./LaneDetection/test_images/out_solidYellowCurve.png
[image4]: ./LaneDetection/test_images/out_solidYellowCurve2.png
[image5]: ./LaneDetection/test_images/out_solidYellowLeft.png
[image6]: ./LaneDetection/test_images/out_whiteCarLaneSwitch.png
[image7]: ./tarsnake.jpg
[image8]: ./shadows.jpg

---

## Reflection

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

Here are the processed images for the provided test inputs:

![test 1][image1] 

![test 2][image2]

![test 3][image3]

![test 4][image4]

![test 5][image5]

![test 6][image6]



## Shortcomings and Considerations

- The first and most obvious is that not all roads have nice lane lines painted on the ground. Some roads don't even have lanes painted on the ground.

  ![tarsnake][image7]

- The algorithm assumes an ROI that mimics the shape of the lane lines in perspective, or a triangular shape. Whilst this works well for California highways, it probably will not hold true for narrow and twisted switchbacks.

- Hough transform uses polar coordinates for a good reason. In my solution, to find the best line among several edge lines, I average ```m``` and ```b``` of several lines represented as ```y=mx+b```. This works well for slanted lines like the ones we see on the lane lines, but it will blow on my face if one of lines returning from Hough is perfectly vertical.

- Most of image processing blocks have hardcoded parameters. In general, hardcoded parameters in changing environments (rainy, sunny, cloudy, snowy) is a bad idea. It also creates a dependency on the camera and a requirement for prior calibration of parameters. Some sort of dynamic discovery and self optimization would be ideal.

- Lastly, image processing by itself doesn't solve all problems. Imaging sensors have dynamic range limitations. Cheaper cameras cannot resolve very bright sunlit surfaces and very dark shadow areas at the same time. It will probably use one of the areas for auto-exposure and saturate the other region to either totally white or totally black. A systems engineer has to carefully select the sensor with appropriate characteristics for this problem.

![shadows][image8]

## Improvements

- The state we leave this problem is not very far from detecting where the car is positioned within the lane lines. A relatively simple modification would be to monitor and estimate the position of the car within the lane and issue an audible alarm when the car is departing the lane. If the system is connected to a camera in real time, then it could work as a rudimentary lane departure system.

## References

[Padu's GitHub](https://github.com/pmerloti/CarND-LaneLines-P1-Merloti) - Source code, documentation and video files
