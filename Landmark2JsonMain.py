#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 09:38:04 2019

@author: chenys
"""

import cv2
import numpy as np
import sys
sys.path.insert(0, cafferoot)
import caffe
import glob
import os
from Landmark2Json import WriteJson

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



root= imgrootfolder
dir_list = os.listdir(root)


for name in dir_list:
    imgRoot = root+name+'/'
    imgPaths = glob.glob(imgRoot+"*.jpg")
    for imgpath in imgPaths:
        img = cv2.imread(imgpath)
        h,w = img.shape[0],img.shape[1]
        
        res =postprocessDepth(img)[0,:] 
        
        WriteJson(res,imgpath,h,w,imgRoot)
