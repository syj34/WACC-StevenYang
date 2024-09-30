from Image import Image
import cv2 as cv
def main():
    img = cv.imread("/Users/syj34/Documents/CodingChallengeWA/answer.png")
    image_test1 = Image(img)
    image_test1.detect()
    image_test1.display_mask()
    image_test1.display_image()


if __name__ == "__main__":
    main()