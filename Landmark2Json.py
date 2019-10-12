#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:02:45 2019

@author: chenys
"""


import json
import base64
def WriteJson(landmark,imgPath,h,w,save_root=None):
    points_list=[]
    for i in range(106):
        x = landmark[2*i] * w 
        y = landmark[2*i+1] * h 
        points_list.append({
                   'fill_color':None,
                   'flag':{},
                   'label': str(i),
                   'line_color': None,
                   'points':[[x,y]],
                   'shape_type': 'point'
                   })
    
    name = imgPath.split('/')[-1].split('.')[0]
    with open(imgPath, "rb") as f:
        data = f.read()
    encoded_string = base64.b64encode(data)
    encoded_string = str(encoded_string, encoding = "utf-8")
    info = {
            "version": "3.16.7",
            'flags' : {},
            'imagePath' : name+".jpg",
            'imageData' : encoded_string,
            'lineColor' : [0,255,0,128],
            'fillColor' : [255,0,0,128], 
            'imageWidth' : w, 
            'imageHeight' : h,
            'shapes' : points_list
            }
    j = json.dumps(info, indent=4)
    with open(save_root+name+'.json', 'w') as f:
        f.write(j)
    print('Done!!!')


    