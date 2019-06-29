import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

image = mpimg.imread('exit-ramp.jpg')
image = image[:,:,:-1]

gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) #grayscale conversion
plt.imshow(gray)
plt.savefig("gray.png", cmap='gray')
plt.show()
# Define a kernel size for Gaussian smoothing / blurring
# cv2.Canny() applies a 5x5 Gaussian internally
kernel_size = 3
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)

low_threshold = 50
high_threshold = 150
edges = cv2.Canny(gray, low_threshold, high_threshold)

#region detection
imshape = image.shape
region_img = np.zeros(edges.shape)
region_img = np.array(region_img,dtype='uint8')
vertices = np.array([[(0,imshape[0]),(450, 290), (490, 290), (imshape[1],imshape[0])]], dtype=np.int32)
cv2.fillPoly(region_img, vertices, 1, 1)

#indicate what kind of lines to detect
#rho and theta are the distance and angular resolution of our grid in Hough space
#threshold parameter specifies the minimum number of votes
#(intersections in a given grid cell) a candidate line needs to have to make it into the output.
#min_line_length is the minimum length of a line (in pixels) that you will accept in the output
#max_line_gap is the maximum distance (again, in pixels) between segments that you will allow to be connected into a single line.
rho = 2
theta = np.pi/180
threshold = 15
min_line_length = 40
max_line_gap = 20
line_image1 = np.copy(image)*0 #creating a blank to draw lines on
line_image2 = np.copy(image)*0
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
sublines = cv2.HoughLinesP(region_img, rho, theta, threshold, np.array([]),
                           min_line_length, max_line_gap)

region_img = np.dstack((region_img, region_img, region_img))

for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image1,(x1,y1),(x2,y2),(255,0,0),10)

for line in sublines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image2,(x1,y1),(x2,y2),(255,0,0),10)

plt.imshow(line_image1)
plt.savefig("line1.png")
plt.show()
plt.imshow(line_image2)
plt.savefig("line2.png")
plt.show()

line_image = line_image1 - (~line_image2 & line_image1)
plt.imshow(line_image)
plt.savefig("filename.png")
plt.show()

#Create a "color" binary image to combine with line image
color_edges = np.dstack((edges, edges, edges))#same size with line_image
# Draw the lines on the edge image
combo = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0)
plt.imshow(combo)
plt.savefig("combo.png")
plt.show()
