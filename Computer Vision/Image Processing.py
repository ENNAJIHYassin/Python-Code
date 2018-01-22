# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:55:37 2017

@author: princ
"""

#Importing Libraries
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from pylab import *
import imtools
import pickle
from scipy.ndimage import filters
from scipy.ndimage import measurements,morphology

        """ THE PIL LIBRARY"""

#Import and show the image
pil_im = Image.open('empire.jpg')
pil_im.show()

#convert it into gray scale using numpy
pil_im.convert('L')
plt.imshow(np.array(pil_im), cmap='gray')
plt.show()

#import an image an convert it into gray scale using just PIL
pil_im = Image.open('empire.jpg')
pil_im.convert('L').show()
pil_im.convert('LA').show()

#create a Thumbnail by downgrading the resolution
pil_im = Image.open('empire.jpg')
pil_im.thumbnail((128,128))
plt.imshow(np.array(pil_im))
plt.show() 
'''we can't use Image.show() on this one'''

#select a specefic region from image
pil_im = Image.open('empire.jpg')
box = (100,100,400,400)
region = pil_im.crop(box)
region.show()

#rotate it and paste it back to the original image
pil_im = Image.open('empire.jpg')
region = region.transpose(Image.ROTATE_180)
pil_im.paste(region,box)
pil_im.show()
'''Or'''
pil_im = Image.open('empire.jpg')
region = region.rotate(180)
pil_im.paste(region,box)
pil_im.show()

#resize
pil_im = Image.open('empire.jpg')
out = pil_im.resize((128,128))
plt.imshow(np.array(out))
plt.show()
'''we can use Image.show() on this one'''
out.show() 


        """THE MATPLOTLIB LIBRARY"""

'''Plot ontop of image'''
# read image to array
im = array(Image.open('empire.jpg'))
# plot the image
imshow(im)
# some points
x = [100,100,400,400]
y = [200,500,200,500]
# plot the points with red star-markers
plot(x,y,'ks')
# line plot connecting the first two points
plot(x[:2],y[:2], 'bs:')
# add title and show the plot
title('Plotting: "empire.jpg"')
axis('off')
show()
'''Or'''
# read image to array
im = np.array(Image.open('empire.jpg'))
# plot the image
plt.imshow(im)
# some points
x = [100,100,400,400]
y = [200,500,200,500]
# plot the points with red star-markers
plt.scatter(x,y,c= 'red', marker = '*')
# line plot connecting the first two points
plt.plot(x[:2],y[:2])
# add title and show the plot
plt.title('Plotting: "empire.jpg"')
plt.axis('off')
plt.show()

'''Image contours and histograms'''
        
# read image to array
im = array(Image.open('empire.jpg').convert('L'))
# create a new figure
figure()
# don’t use colors
gray()
# show contours with origin upper left corner
contour(im, origin='image')
axis('equal')
axis('off')
#draw histogram of pixel values in 128 bins
figure()
hist(im.flatten(),128)
show()
'''Or'''
# read image to array
im = np.array(Image.open('empire.jpg').convert('L'))
# create a new figure
plt.figure()
# show contours with origin upper left corner
plt.contour(im, origin='image', cmap ='gray')
axis('equal')
axis('off')
#draw histogram of pixel values in 128 bins
plt.figure()
plt.hist(im.flatten(),128, edgecolor='k')
plt.show()

'''Interactive annotation'''

im = array(Image.open('empire.jpg'))
imshow(im)
print ('Please click 3 points')
x = ginput(3)
print ('you clicked:',x)
show()

'''Array image representation'''
im = array(Image.open('empire.jpg'))
print (im.shape, im.dtype)
im = array(Image.open('empire.jpg').convert('L'),'f')
print (im.shape, im.dtype)


        """NUMPY LIBRARY"""
            
'''Graylevel transforms'''
im = array(Image.open('empire.jpg').convert('L'))
imshow(im)
im2 = 255 - im #invert image
figure()
imshow(im2)
im3 = 100 * (im / 255) + 100 #clamp to interval 100...200 which makes the image brighter
figure()
imshow(im3)
im4 = 255 * (im / 255)**2 #squared makes dark pixels darker
figure()
imshow(im4)
#show the pixel range for every image
print (int(im.min()), int(im.max()))
print (int(im2.min()), int(im2.max()))
print (int(im3.min()), int(im3.max()))
print (int(im4.min()), int(im4.max()))
#bring back/create an array as a PIL Image 
pil_im = Image.fromarray(im)
pil_im.show()
#need to convert back to uint8 before creating the PIL image
pil_im = Image.fromarray(uint8(im3)) 
pil_im.show()

'''Histogram equalization to increase contrast'''
im = array(Image.open('empire.jpg').convert('L'))
im2,cdf,y = imtools.histeq(im)

gray()
subplot(2,3,6)
xlabel('After')
imshow(im2)

gray()
subplot(2,3,4)
xlabel('Before')
imshow(im)

subplot(2,3,3)
hist(im2.flatten(),128, edgecolor ='k')
show()

subplot(2,3,1)
hist(im.flatten(),128, edgecolor ='k')
show()

subplot(2,3,2)
plot(range(256), y)
plot(range(256), range(256), 'r:')
xlabel('Transform')
show()

im = array(Image.open('AquaTermi_lowcontrast.jpg').convert('L'))
im2,cdf,y = imtools.histeq(im)

'''PCA of images'''

imlist = imtools.get_imlist('a_thumbs') #get the list of image names
im = array(Image.open(imlist[0])) # open one image to get size
m,n = im.shape[0:2] # get the size of the images
imnbr = len(imlist) # get the number of images

# create matrix to store all flattened images
immatrix = array([array(Image.open(im)).flatten()
for im in imlist],'f')

# perform PCA
V,S,immean = imtools.pca(immatrix)

# show some images (mean and 7 first modes)
figure()
gray()
subplot(2,4,1)
imshow(immean.reshape(m,n))
for i in range(7):
    subplot(2,4,i+2)
    imshow(V[i].reshape(m,n))
show()

'''Using the Pickle module to save important values for later in files'''
# open file and save
with open('font_pca_modes.pkl', 'wb') as f:
    pickle.dump(immean,f)
    pickle.dump(V,f)
'''or'''
np.savetxt('test.txt',x,'%i') #last parameter specifies that the saved value is an integer
    
# open file and load
with open('font_pca_modes.pkl', 'rb') as f:
    immean_test = pickle.load(f) #it should be loaded at the same order with which it was saved
    V_test = pickle.load(f)
'''or'''
x = np.loadtxt('test.txt')


        """SCIPY LIBRARY"""

'''Blurring images to define an image scale to work in, for interpolation, for
computing interest points, and in many more applications.'''
#blurring a grayscale image
im = array(Image.open('empire.jpg').convert('L'))
for i in range(4):
    subplot(1, 4, i+1)
    # 3*i refers to the standard deviation
    imshow(filters.gaussian_filter(im,3*i))

#blurring a color image
im = array(Image.open('empire.jpg'))
im2 = zeros(im.shape)
for i in range(4):
    subplot(1, 4, i+1)
    for j in range(3): #blur every single color channel
        im2[:,:,j] = filters.gaussian_filter(im[:,:,j],3*i)
    im2 = uint8(im2) #coulad have also used 'im2 = array(im2,’uint8’)'
    imshow(im2) 

'''Image derivatives with Sobel filters'''
im = array(Image.open('empire.jpg').convert('L'))
subplot(1, 4, 1)
imshow(im)
#the x component of Sobel derivative filter
imx = zeros(im.shape)
filters.sobel(im,1,imx) #The intensity change described with the x derivatives Ix of the image
subplot(1, 4, 2)
imshow(imx)
#the y component of Sobel derivative filter
imy = zeros(im.shape)
filters.sobel(im,0,imy) #The intensity change described with the y derivatives Iy of the image
subplot(1, 4, 3)
imshow(imy)
#the magnitude of the image gradient
magnitude = sqrt(imx**2+imy**2)
subplot(1, 4, 4)
imshow(magnitude)

'''Image derivatives with Gaussian filters'''
im = array(Image.open('empire.jpg').convert('L'))
for i in range(4): # 3*i refers to the standard deviation
    #the x component of Guassian derivative filter
    subplot(3, 4, i+1)
    imx = zeros(im.shape)
    filters.gaussian_filter(im, (3*i,3*i), (0,1), imx)
    imshow(imx)
    #the y component of Guassian derivative filter
    subplot(3, 4, i+5)
    imy = zeros(im.shape)
    filters.gaussian_filter(im, (3*i,3*i), (1,0), imy)
    imshow(imy)
    subplot(3, 4, i+9)
    #the magnitude of the image gradient
    magnitude = sqrt(imx**2+imy**2)
    magnitude = 255 - magnitude
    imshow(magnitude)
    
'''Morphology - counting objects'''
# load image and threshold to make sure it is binary
im = array(Image.open('houses.png').convert('L'))
im = 1*(im<128)
labels, nbr_objects = measurements.label(im)
print ("Number of objects:", nbr_objects)

# morphology - opening to separate objects better
im_open = morphology.binary_opening(im,ones((9,5)),iterations=2)
labels_open, nbr_objects_open = measurements.label(im_open)
print ("Number of objects:", nbr_objects_open)

'''Saving arrays as images'''
import scipy.misc
lena = scipy.misc.face() 
scipy.misc.imsave('scipy_saved_test_image.jpg',lena)


        """Rudin-Osher-Fatemi (ROF) DENOISING MODEL"""
        
'''Apply ROF to a synthetic image'''
# create synthetic image with noise
imlist = []
im = np.zeros((500,500))
im[100:400,100:400] = 128
im[200:300,200:300] = 255
imlist.append(im)
im2 = im + 30*np.random.standard_normal((500,500))
imlist.append(im2)
#Apply ROF denoising
U,T = imtools.rof_denoise(im2,im2)
imlist.append(U)
#Apply gaussian filter
G = filters.gaussian_filter(im2,10)
imlist.append(G)
#show results
plt.figure()
for i in range(4):
    plt.subplot(1, 4, i+1)
    plt.imshow(imlist[i])
    
'''Apply ROF to a real image'''
# open image and create its noisy version
im = array(Image.open('empire.jpg').convert('L'))
im2 = im + 30*np.random.standard_normal((800,569))
#Apply ROF denoising
U,T = imtools.rof_denoise(im,im)
#Apply gaussian filter
G = filters.gaussian_filter(im,5)
#plot the results
figure()
gray()
subplot(1, 4, 1)
imshow(im)
subplot(1, 4, 2)
imshow(im2)
subplot(1, 4, 4)
imshow(G)
subplot(1, 4, 3)
imshow(U)

