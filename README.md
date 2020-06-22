# Pixelator
##Use Example
```
#First use Pixelator with image location
pix = Pixelator('C:/Users/meste/Desktop/test4.jpg')

#intensity refers to radius of pixel effect
intensity = 8

#pix.original() refers to original image
image_pixelate = pix.pixelate(pix.original(), intensity)

#after pixel effect you can reduce number of colors
#number of colors
n_colors = 32

#right here we use an image with pixel effect but you can use the original image
image_reduced_colors = pix.kMeansCompress(image_pixelate, n_colors)

#finally you can show your final image
pix.show(image_reduced_colors)

#You can save your final image too
#willcompare is to save new image with the original image side-by-side
willcompare=False
pix.save(image_reduced_colors, 'somelocation', willcompare)
```
