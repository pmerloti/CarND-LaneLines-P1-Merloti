# **Finding Lane Lines on the Road**
---

The goals / steps of this project are the following:
1. Create a image processing pipeline that finds lane lines on the road
2. Test the pipeline on static images provided with project material
3. Create a video processor that applies pipeline to a video file and outputs an annotated video
4. Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

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

## Shortcomings and Considerations

## Improvements

Lane departure detection
- what happens when lanes start shifting


## References

[Padu's GitHub](https://github.com/pmerloti/CarND-LaneLines-P1-Merloti) - Source code, documentation and video files


![alt text][image1]
