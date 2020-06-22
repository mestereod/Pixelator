  
import sys
import numpy as np
import os
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

class Pixelator:
    def __init__(self, imageInput):
        self.image = Image.open(imageInput)

    def original(self):
        return self.image
    
    def show(self, image):
        image.show()
        
    def pixelate(self, inputImage, pixel_scale):
        copy = inputImage.copy()
        pixel = copy.load()
        kernel_size = pixel_scale*2+1
        for x in range(pixel_scale,inputImage.width-pixel_scale, kernel_size-1):
            for y in range(pixel_scale, inputImage.height-pixel_scale, kernel_size-1):
                #print('X {} Y {}'.format(x,y))
                sumRed = 0
                sumGreen = 0
                sumBlue = 0
                for kernelX in range(-pixel_scale, pixel_scale+1):
                    for kernelY in range(-pixel_scale,pixel_scale+1):
                        #print('kx {} ky {} kernelx {} kernely {}'.format(kernelX+x, kernelY+y, kernelX, kernelY))
                        sumRed += pixel[x+kernelX, y+kernelY][0]
                        sumGreen += pixel[x+kernelX, y+kernelY][1]
                        sumBlue += pixel[x+kernelX, y+kernelY][2]

                sumRed /= kernel_size**2
                sumGreen /= kernel_size**2
                sumBlue /= kernel_size**2
                
                sumRed = int(sumRed)
                sumGreen = int(sumGreen)
                sumBlue = int(sumBlue)
                for kernelX in range(-pixel_scale, pixel_scale):
                    for kernelY in range(-pixel_scale,pixel_scale):
                        pixel[x+kernelX, y+kernelY] = (sumRed, sumGreen, sumBlue)
        return copy

    def kMeansCompress(self, inputImage, n_colors):
        reduced_matrix = np.reshape(np.array(inputImage), (inputImage.height * inputImage.width, 3))
        image_array_sample = shuffle(reduced_matrix, random_state=0)[:1000]
        kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
        labels = kmeans.predict(reduced_matrix)
        newImageKmeans = np.zeros((inputImage.height, inputImage.width, 3))
        label_idx = 0
        for i in range(inputImage.height):
            for j in range(inputImage.width):
                newImageKmeans[i][j] = kmeans.cluster_centers_[labels[label_idx]]
                label_idx += 1
        newImageKmeans = newImageKmeans.astype(np.uint8)
        return Image.fromarray(newImageKmeans)

    def save(self, image, outputPath, compare=False):
        if compare:
            new_im = Image.new('RGB', (self.image.width, 2*self.image.height+1))
            new_im.paste(self.image, (0,0))
            new_im.paste(image, (0,self.image.height+1))
            new_im.save(outputPath)
            new_im.show()
        else:
            image.save(outputPath)