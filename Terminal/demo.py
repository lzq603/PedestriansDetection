#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import multiprocessing
import os
import threading
from timeit import time
import warnings
import sys
import cv2
import numpy as np
from PIL import Image
from yolo import YOLO

from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from deep_sort.detection import Detection as ddet
warnings.filterwarnings('ignore')

def detect(yolo,videoChoice,site,ip):

   # Definition of the parameters
    max_cosine_distance = 0.3
    nn_budget = None
    nms_max_overlap = 1.0
    
   # deep_sort 
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename,batch_size=1)
    
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    writeVideo_flag = True






    video_capture = cv2.VideoCapture(videoPath)
    starttime = time.time()


    if writeVideo_flag:
    # Define the codec and create VideoWriter object
        w = int(video_capture.get(3))
        h = int(video_capture.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('output%d.avi'%(site), fourcc,30, (w, h))
        list_file = open('detection.txt', 'w')
        frame_index = -1 
        
    fps = 0.0
    while True:
        ret, frame = video_capture.read()  # frame shape 640*480*3
        if ret != True:
            break
        t1 = time.time()

       # image = Image.fromarray(frame)
        image = Image.fromarray(frame[...,::-1]) #bgr to rgb
        boxs = yolo.detect_image(image)

        print("box_num",len(boxs))



        # 调用http协议，传输数据
        import requests
        # 这里需要加上异常处理
        try:
            url = ip+'/peoplecount/insert?num=%d&site=%d'%(len(boxs),site)
            print(url)
            req = requests.get(url)
            print(req.text)
        except requests.exceptions.RequestException as e:
            print('error')

        features = encoder(frame,boxs)
        # score to 1.0 here).
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]

        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]

        # Call the tracker
        tracker.predict()
        tracker.update(detections)

        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 2)
            cv2.putText(frame, str(track.track_id),(int(bbox[0]), int(bbox[1])),0, 5e-3 * 200, (0,255,0),2)

        for det in detections:
            bbox = det.to_tlbr()
            cv2.rectangle(frame,(int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,0,0), 2)
            
        cv2.imshow('', frame)
        
        if writeVideo_flag:
            # save a frame
            out.write(frame)
            frame_index = frame_index + 1
            list_file.write(str(frame_index)+' ')
            if len(boxs) != 0:
                for i in range(0,len(boxs)):
                    list_file.write(str(boxs[i][0]) + ' '+str(boxs[i][1]) + ' '+str(boxs[i][2]) + ' '+str(boxs[i][3]) + ' ')
            list_file.write('\n')

        fps  = ( fps + (1./(time.time()-t1)) ) / 2
        print("fps= %f"%(fps))
        
        # Press Q to stop!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    if writeVideo_flag:
        out.release()
        list_file.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print('请输入云端主机的ip(本机请输入127.0.0.1):')
    host = input()
    host = 'http://'+host

    print('请输入端口(默认为80):')
    port = input()
    host += ":"+port
    print('云端主机:', host)

    print('请输入站点编号:')
    site = int(input())

    videoPath = ''
    videoChoice = 4

    while videoChoice is not 5:
        print('请选择摄像头或示例视频:')
        print('1.示例视频1\t2.示例视频2\t3.示例视频3\t4.摄像头\t5.退出')
        videoChoice = int(input())
        if videoChoice == 1:
            print('示例视频1')
            videoPath = 'testVideo/1.mp4'
        elif videoChoice == 2:
            print('示例视频2')
            videoPath = 'testVideo/2.mp4'
        elif videoChoice == 3:
            print('示例视频3')
            videoPath = 'testVideo/3.mp4'
        elif videoChoice == 4:
            print('摄像头')
            videoPath = 0
        else:
            print('错误,请重新输入')
            continue
        detect(YOLO(),videoChoice,site,host)


