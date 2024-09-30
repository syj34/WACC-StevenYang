# Wisconsin Autonomous Perceptions Coding Challenge

## Methodology

First, I had to find a way to isolate the cone objects in the image. I did this by converting the image to HSV, and creating a mask of red/orange. HSV allows easier manipulation of color which assists in filtering out other aspects of the image that may also be red or orange. Using contours, I was able to outline the cones and locate them within the mask. Then, using moments, I found the centroid of each cone. Dividing the weighted X and Y by the total area of the contour, gives us an approximation of the centroid of the object. Filtering by coordinate values, I split the cones into lists of left and right, while also filtering out the top of the image past where the cones reside. I calculated the highest and lowest Y coordinate centroid on either side, which locates the closest and furthest cones, then drew a line between them. The issue here was that the line did not extend all the way to the frame of the image. To fix this, I calculated the slope of the line for both sides and found the x coordinate where the line should extend to. Finally, I drew a line between the last cone and that point to extend it fully to the frame.

#### Things That Did Not Work
I initially tried to convert the image to grayscale and then find the line along the cones using edges and Houghlines. However, this did not work as the cones do not have a sharp line along them like a lane line would, so it would instead pickup the lines along the floor tiles. Something else that I struggled with was filtering out the brown door on the left side of the image once I began filtering by orange/red. This door was consistently picked up in the mask and led to me having to increase the green threshold to avoid the presence of brown.

#### Libraries
Throughout this challenge I utilized cv2 (OpenCV) and numpy. Opencv was essential in processing the image and creating the mask to find just the cones. Numpy was useful for the HSV values of the mask and any resizing that may have been necessary.

# Final Product

![answer](https://github.com/user-attachments/assets/29882f4b-2c56-48a2-99e7-c0a69a9d73d4)
