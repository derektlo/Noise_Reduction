# Derek Lo
# February 19, 2016
# A simple implementation of a relaxation labelling network to reduce
# noise in an image.

import scipy.misc

png = scipy.misc.imread('cactus.png')

# 1 - white pixel
# 0 - black pixel

def mask(img):
    n = len(img)
    for i in range(0,n):
        for j in range(0,n):
            if img[i][j] > 200:
                img[i][j] = 1
            else:
                img[i][j] = 0
    return img

def unmask(img):
    n = len(img)
    for i in range(0,n):
        for j in range(0,n):
            if img[i][j] > .5:
                img[i][j] = 255
            else:
                img[i][j] = 0
    return img

def compatibility(pixel, probability):
    if pixel == 1:
        return probability
    else:
        return probability-1

def relaxation(img, iters):
    imageCopy = img
    n = len(img)
    for q in range(0, iters):
        for i in range(0,n):
            for j in range(0,n):
                support = 0
                for k in range(0,2):
                    if i-1 > 0 and j-1 > 0:
                        support = support + compatibility(k,img[i-1][j-1])
                    if i-1 > 0:
                        support = support + compatibility(k,img[i-1][j])
                    if i-1 > 0 and j+1 < n:
                        support = support + compatibility(k,img[i-1][j+1])
                    if j-1 > 0:
                        support = support + compatibility(k,img[i][j-1])
                    if j+1 < n:
                        support = support + compatibility(k,img[i][j+1])
                    if i+1 < n and j-1 > 0:
                        support = support + compatibility(k,img[i+1][j-1])
                    if i+1 < n:
                        support = support + compatibility(k,img[i+1][j])
                    if i+1 < n and j+1 < n:
                        support = support + compatibility(k,img[i+1][j+1])
                new_prob = img[i][j] + support
                if new_prob > 1:
                        new_prob = 1
                elif new_prob < 0:
                    new_prob = 0
                imageCopy[i][j] = new_prob
        img = imageCopy
    return img

png = mask(png)
png = relaxation(png, 5)
png = unmask(png)
scipy.misc.imsave('noise_reduced_cactus.jpg', png)
