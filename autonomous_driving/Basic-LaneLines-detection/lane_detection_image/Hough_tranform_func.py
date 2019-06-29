#Hough tranform implementation: simple version
import numpy as np
import matplotlib.pyplot as plt

def hough_line(img):
  # Rho and Theta ranges
      thetas = np.deg2rad(np.arange(-90.0, 90.0))
      width, height = img.shape
      max_dist = np.ceil(np.sqrt(width * width + height * height))
      rhos = np.linspace(-max_dist, max_dist, max_dist * 2.0)
      #print(max_dist.dtype)
      # Cache some resuable values
      cos_t = np.cos(thetas)
      sin_t = np.sin(thetas)
      num_thetas = len(thetas)

      # Hough accumulator array of theta vs rho
      x = 2 * max_dist
      x = np.array(x, dtype=np.uint64)
      accumulator = np.zeros((x, num_thetas))

      y_idxs, x_idxs = np.nonzero(img) # (row, col) indexes to edges

      # Vote in the hough accumulator
      for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]

        for t_idx in range(num_thetas):
          # Calculate rho. max_dist is added for a positive index
          rho = round(x * cos_t[t_idx] + y * sin_t[t_idx]) + max_dist
          rho = np.array(rho, dtype=np.uint64)
          accumulator[rho, t_idx] += 1.0

      return accumulator, thetas, rhos

  # Create binary image and call hough_line
image = np.zeros((50,50))
image[10:40, 10:40] = np.eye(30)
plt.imshow(image, cmap='gray')
plt.show()
accumulator, thetas, rhos = hough_line(image)

# Easiest peak finding based on max votes
idx = np.argmax(accumulator)
inx = idx / accumulator.shape[1]
inx = np.array(inx, dtype=np.uint64)
rho = rhos[inx]
theta = thetas[idx % accumulator.shape[1]]
plt.imshow(accumulator, cmap=plt.cm.cool)
plt.show()
print("rho={0:.2f}, theta={1:.0f}".format(rho, np.rad2deg(theta)))
