import scipy.datasets
import matplotlib.pyplot as plt
import numpy as np

# load the ascent image
ascent = scipy.datasets.ascent()
print(ascent.shape)

# Visualize the image
plt.grid(False)
plt.gray()
plt.axis('off')
plt.imshow(ascent)
plt.show()

# Copy image to a numpy array
image_transformed = np.copy(ascent)

# Get the dimensions of the image
size_x = image_transformed.shape[0]
size_y = image_transformed.shape[1]

filter = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]

# A couple more filters to try for fun!
# filter = [ [-1, -2, -1], [0, 0, 0], [1, 2, 1]]
# filter = [ [-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]

# my filters
# filter = [ [0, -1, 0], [-1, 4, -1], [0, -1, 0]]
#filter = [ [-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
#filter = [ [-1, 0, -1], [0, 4, 0], [-1, 0, -1]]

# If all the digits in the filter don't add up to 0 or 1, you
# should probably do a weight to get it to do so
# so, for example, if your weights are 1,1,1 1,2,1 1,1,1
# They add up to 10, so you would set a weight of .1 if you want to normalize them
weight  = 1

# Iterate over the image
for x in range(1, size_x-1):
    for y in range(1, size_y-1):
        convolution = 0.0
        convolution += ascent[x-1][y-1] * filter[0][0]
        convolution += ascent[x - 1][y] * filter[0][1]
        convolution += ascent[x - 1][y+1] * filter[0][2]
        convolution += ascent[x][y - 1] * filter[1][0]
        convolution += ascent[x][y] * filter[1][1]
        convolution += ascent[x][y+1] * filter[1][2]
        convolution += ascent[x+1][y - 1] * filter[2][0]
        convolution += ascent[x + 1][y] * filter[2][1]
        convolution += ascent[x + 1][y+1] * filter[2][2]

        # Multiply by weight
        convolution *= weight

        # Check the boundaries of the pixel values
        if(convolution < 0 ):
            convolution =0
        if(convolution>255):
            convolution=255

        # Load into the transformed image
        image_transformed[x][y] = convolution

# Plot the image. Note the size of the axes -- they are 512 by 512
plt.gray()
plt.imshow(image_transformed)
plt.show()

# Assign dimensions half the size of the original image
new_x = int(size_x/2)
new_y = int(size_y/2)

# Create blank image with reduced dimensions
newImage = np.zeros((new_x, new_y))

# Iterate over the image
for x in range(0, size_x, 2):
    for y in range(0, size_y, 2):
        #Store all the pixel values in the (2,2) pool
        pixels = []
        pixels.append(image_transformed[x][y])
        pixels.append(image_transformed[x][y+1])
        pixels.append(image_transformed[x+1][y])
        pixels.append(image_transformed[x+1][y+1])

        # Get only the largest value and assign to the reduced image
        newImage[int(x/2)][int(y/2)] = max(pixels)

plt.gray()
plt.grid(False)
plt.imshow(newImage)
plt.show()
