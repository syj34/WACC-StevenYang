import numpy as np
import cv2 as cv
class Image:
    def __init__(self, img):
        self.img = img
        self.mask = None

    def save_image(self):
        cv.imwrite("answer.png", self.img)

    def display_image(self):
        """
        Displays the current image until a key is pressed.
        :return: None
        """

        cv.imshow("finalAnswer",self.img)
        cv.waitKey()
        cv.destroyAllWindows()

    def display_mask(self):
        """
        Displays the mask that was used in the creation of the final product
        :return: None
        """
        cv.imshow("mask", self.mask)
        cv.waitKey()
        cv.destroyAllWindows()

    def detect(self):
        """
        Identifies the cones based on their HSV properties and generates lines through each
        lane of them that extend to the boundary of the image.
        :return: None
        """
        #Converts the image to HSV instead of BGR as HSV allows easier manipulation of color
        hsv = cv.cvtColor(self.img, cv.COLOR_BGR2HSV)

        #Create the range of color that we want to filter for
        #In HSV there are two different ranges of red values, so we have to include them both
        lower_red = np.array([0, 195, 100])
        upper_red = np.array([10, 255, 255])
        lower_red2 = np.array([160, 195, 100])
        upper_red2 = np.array([179, 255, 255])

        #Create the masks based on our above filters
        mask1 = cv.inRange(hsv, lower_red, upper_red)
        mask2 = cv.inRange(hsv, lower_red2, upper_red2)

        #Combine the masks
        combined_mask = cv.bitwise_or(mask1, mask2)
        self.mask = combined_mask

        #Use contours to define the border of the cones in our image
        contours, _ = cv.findContours(combined_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        centroidsLeft = []
        centroidsRight = []

        #Iterate through the contours and find their centroids
        for contour in contours:

            #Calculates the center of the contours (cones)
            M = cv.moments(contour)

            #M["m00"] represents the entire area of the cone, while M["m10"] and M["m01"] represent
            #the sum of the X and Y coordinates (weighted by fit). By dividing the total area by the
            #sum of these weighted X and Y values, we can determine the centroids of the cones
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                #Filters out objects far away that could interfere with cone detection
                if(cY<550):
                    continue

                #Split the cone lanes down the middle of the image
                if (cX>908):
                    centroidsRight.append([cX,cY])
                else:
                    centroidsLeft.append([cX, cY])

        maxLeft = 0
        minLeft= 5000
        maxRight = 0
        minRight = 5000
        botRight = None
        botLeft = None
        topRight = None
        topLeft = None

        #This loop determines the left cones that are closest and furthest away from the camera/car
        for i in range(len(centroidsLeft)):
            if(centroidsLeft[i][1]>maxLeft):
                botLeft = centroidsLeft[i]
                maxLeft = centroidsLeft[i][1]
            if(centroidsLeft[i][1]<minLeft):
                topLeft = centroidsLeft[i]
                minLeft = centroidsLeft[i][1]

        #Draws a line from the first left cone through the last left cone
        cv.line(self.img, botLeft, topLeft, (0, 0, 255), 2)

        # This loop determines the right cones that are closest and furthest away from the camera/car
        for i in range(len(centroidsRight)):
            if (centroidsRight[i][1] > maxRight):
                botRight = centroidsRight[i]
                maxRight = centroidsRight[i][1]
            if (centroidsRight[i][1] < minRight):
                topRight = centroidsRight[i]
                minRight = centroidsRight[i][1]

        #Draws a line from the first right cone through the last right cone
        cv.line(self.img, botRight, topRight, (0, 0, 255), 2)

        #Calculates the slope between the first and last left cone
        dx = botLeft[0] - topLeft[0]
        dy = botLeft[1] - topLeft[1]

        #Assigns the x and y coordinates of the top left cone to variables
        x = topLeft[0]
        y = topLeft[1]

        #Calculates the extension of the line from the last left cone to the end of the frame
        factor = y / dy
        x = x - factor * dx


        #Calculates the slope between the first and last right cone
        dx2 = botRight[0] - topRight[0]
        dy2 = botRight[1] - topRight[1]

        #Assigns the x and y coordinates of the top right cone to variables
        x2 = topRight[0]
        y2 = topRight[1]

        #Calculates the extension of the line from the last right cone to the end of the frame
        factor2 = y2 / dy2
        x2 = x2 - factor2 * dx2


        #Draws the lines from the end of each top cone to the end of the frame
        cv.line(self.img, (topLeft[0], topLeft[1]), (int(x), int(factor)), (0, 0, 255), 2)
        cv.line(self.img, (topRight[0], topRight[1]), (int(x2), int(factor2)), (0, 0, 255), 2)

        return self.img






