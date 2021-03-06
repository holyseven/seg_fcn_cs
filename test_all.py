import caffe
import numpy as np
from PIL import Image
import random as rd
import os
import sys
import datetime

def rdColorImage(grey_img_array):
    rd.seed(555) # each time it generates the same color distribution
    colorlist = np.zeros((34,3), dtype=np.uint8)
    for i in range(34):
        colorlist[i] = [rd.randint(0,255), rd.randint(0,255), rd.randint(0,255)]
    color_image = np.zeros((grey_img_array.shape[0], grey_img_array.shape[1], 3), dtype=np.uint8)
    for r in range(grey_img_array.shape[0]):
        for c in range(grey_img_array.shape[1]):
            color_image[r,c] = colorlist[grey_img_array[r,c]]
    return color_image



#weights = 'fcn32s-heavy-pascal.caffemodel'
weights = './fcn8s_56k.caffemodel'
model = 'deploy.prototxt'

caffe.set_mode_gpu()
caffe.set_device(0)
net = caffe.Net(model, weights, caffe.TEST)


def testoneimage(filename, i):
    print str(datetime.datetime.now()) + ' reading image... ' 
    im = Image.open(filename)
    #im = im.resize(im.size/np.array(2, np.int))
    in_ = np.array(im, dtype=np.float32)
    # RGB convert to BGR
    in_ = in_[:,:,::-1]
    # substract mean
    in_ -= np.array((120, 120, 120))
    # to C * H * W
    in_ = in_.transpose((2,0,1))
    
    net.blobs['data'].reshape(1, *in_.shape)
    net.blobs['data'].data[...] = in_
    
    print str(datetime.datetime.now()) + ' preparing net forwarding... '
    net.forward()
    out = net.blobs['score'].data[0].argmax(axis=0)
    
    # need convert to uint8 to Image
    out = np.array(out, np.uint8)
    
    color_image = rdColorImage(out)
    
    relativepath = filename.split('/')

    if os.path.isdir('./results/' + relativepath[-2]) == False:
        os.mkdir('./results/' + relativepath[-2])
    if os.path.isdir('./results_color/' + relativepath[-2]) == False:
        os.mkdir('./results_color/' + relativepath[-2])

    print str(datetime.datetime.now()) + ' saving images... '
    img = Image.fromarray(out, 'L')
    img.save('./results/' + relativepath[-2] + '/' + relativepath[-1])
    
    cimg = Image.fromarray(color_image, 'RGB')
    cimg.save('./results_color/' + relativepath[-2] + '/' + relativepath[-1])
    
def gttocolor(filename, i):
    gt = Image.open(filename)
    gt_grey = np.array(gt, np.uint8)
    gt_image = rdColorImage(gt_grey)
    gt_cimage = Image.fromarray(gt_image, 'RGB')
    gt_cimage.save('gt/' +str(i) +'.png')


#filenamelist = open('fcn_cs_train_laptop.txt').read().splitlines()
#gtlist = open('fcn_cs_train_label_laptop.txt').read().splitlines()
filenamelist = open('./cs_left8bit_sequence.txt').read().splitlines()
for i in range(int(sys.argv[1]), int(sys.argv[2]), 1):
#for i in range(50):
    #if i%2 == 0:
    #    testoneimage(filenamelist[i], i)
    #if i < 49:
    #    continue
    #if i == 0 or i == 31:
        #testoneimage(filenamelist[i], i)
        #gttocolor(gtlist[i],i)
    testoneimage(filenamelist[i], i)
    print str(datetime.datetime.now()) + ' Done.'
    print filenamelist[i]
