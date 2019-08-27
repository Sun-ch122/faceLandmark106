#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 09:45:57 2019


"""

import cv2
import numpy as np
import sys
sys.path.insert(0, "/media/chenys/fadbfcc0-5795-46c9-9b99-c71dcc8032f9/DeepLearningFrame/caffe-BVLC/python")
import caffe
import glob

net_file = './model/lnet106_112.prototxt'
caffe_model = './model/lnet106_112.caffemodel'
caffe.set_mode_gpu()
net = caffe.Net(net_file,caffe_model,caffe.TEST)  

print("-------load caffe prototxt success")


def data_process(img):
    tempimg = np.zeros((1, 112, 112, 3))
    im = cv2.resize(img, (112, 112))
    im = (im-127.5)/128.0
    tempimg[0 , :, :, :] = im
    tempimg = tempimg.transpose(0, 3, 1, 2)
    return tempimg
    
def postprocessDepth(img):
    inputImg = data_process(img)
    net.blobs['data'].data[...] = inputImg
    out = net.forward()['bn6_3']    
    return out



imgPaths = glob.glob("./testImg/*.jpg")
 
for imgpath in imgPaths:
    img = cv2.imread(imgpath)
    h,w = img.shape[0],img.shape[1]  
    res =postprocessDepth(img)[0,:] 
    for i in range(106):
        x = res[2*i] * w 
        y = res[2*i+1] * h 
        cv2.circle(img, (int(x), int(y)), 1, (0, 255, 0), 3)
cv2.imwrite('./res/'+imgpath.split('/')[-1],img)

    
    
