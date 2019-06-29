import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Read in the image
image = mpimg.imread('test.png')
image = image[:,:,:-1]
#print(image.shape)

ysize = image.shape[0]
xsize = image.shape[1]
color_select= np.copy(image)
line_image = np.copy(image)
region_select = np.copy(image)

# Define our color criteria
red_threshold = 200/255
green_threshold = 200/255
blue_threshold = 200/255
rgb_threshold = [red_threshold, green_threshold, blue_threshold]

# Define a triangle region of interest
left_bottom = [150, 628]
right_bottom = [1000, 628]
apex = [600, 300]
# left_bottom = [0, 539]
# right_bottom = [900, 539]
# apex = [475, 320]

fit_left = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), 1)
fit_right = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)

# Mask pixels below the threshold
color_thresholds = (image[:,:,0] < rgb_threshold[0]) | \
                    (image[:,:,1] < rgb_threshold[1]) | \
                    (image[:,:,2] < rgb_threshold[2])

# Find the region inside the lines
XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
region_thresholds = (YY > (XX*fit_left[0] + fit_left[1])) & \
                    (YY > (XX*fit_right[0] + fit_right[1])) & \
                    (YY < (XX*fit_bottom[0] + fit_bottom[1]))
# Mask color selection
color_select[color_thresholds] = [0,0,0]
region_select[region_thresholds] = [1, 0, 0]
plt.imshow(region_select)
plt.show()
# Find where image is both colored right and in the region
line_image[~color_thresholds & region_thresholds] = [1,0,0]

# Display our two output images
plt.imshow(color_select)
plt.show()
plt.imshow(line_image)
plt.show()
