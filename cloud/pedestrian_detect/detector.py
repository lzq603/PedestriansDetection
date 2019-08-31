# -*- coding: utf-8 -*-
# @Author: lizhiqag@163.com
# @Date:   2019-04-18 20:18:15
# @Description   [ description ]
# @Last Modified time: 2019-05-31 19:58:58

import cv2 as cv
import numpy as np
import os

dot = ""
try:
	# 外部文件引用
	from .training import svm_train
	from .pyramid import *
	from .sliding_window import sliding_window
	from .non_maximum import non_max_suppression_fast
except Exception as e:
	# 当前文件
	from training import svm_train
	from pyramid import *
	from sliding_window import sliding_window
	from non_maximum import non_max_suppression_fast
	dot = "."

# 参数

# 最佳！
window_step = 2
scaleFactor = 10 			# 1.03
scoreThreshold = 0.021 		# 0.021 		# 0.024
svm_xml = './pedestrian_detect/svm_head_linear_0.001.xml'	# C == 0.001   0个人头

# window_step = 2
# scaleFactor = 20 			# 1.08
# scoreThreshold = 0.01 		# 0.123 / 0.13
# svm_xml = './pedestrian_detect/svm_head_linear_0.003.xml'		# C == 0.003	# 51个人头

# 优先考虑
# window_step = 2
# scaleFactor = 20 			# 1.08
# scoreThreshold = 0.1 		# 0.123 / 0.13
# svm_xml = './pedestrian_detect/svm_head_linear_0.005.xml'		# C == 0.005	# 51个人头

# window_step = 2
# scaleFactor = 20 				# 1.08
# scoreThreshold = 0.2 			# 0.123 / 0.13
# svm_xml = './pedestrian_detect/svm_head_linear_0.01.xml'		# C == 0.01		# 133 个人头

# window_step = 2
# scaleFactor = 20 				# 1.08
# scoreThreshold = 0.2 			# 0.123 / 0.13
# svm_xml = './pedestrian_detect/svm_head_linear_0.03.xml'		# C == 0.03		# 133 个人头

# window_step = 2
# scaleFactor = 20 				# 1.08
# scoreThreshold = 0.56 			# 0.123 / 0.13
# svm_xml = './pedestrian_detect/svm_head_linear_0.05.xml'		# C == 0.05		

svm_xml = dot + svm_xml


# def change_cv_draw(image,strs,local,sizes,colour):
#     cvimg = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#     pilimg = Image.fromarray(cvimg)
#     draw = ImageDraw.Draw(pilimg)  # 图片上打印
#     font = ImageFont.truetype("SIMYOU.TTF",sizes, encoding="utf-8")
#     draw.text(local, strs, colour, font=font)
#     image = cv.cvtColor(np.array(pilimg), cv.COLOR_RGB2BGR)
#     return image

def detect(img,scoreThreshold):

	order = 1

	scale = 1
	w, h = 20, 20
	rectangles = []

	# hog 特征属性
	winSize = (20,20)
	blockSize = (10,10)
	blockStride = (5,5)
	cellSize = (5,5)
	nBin = 9
	hog = cv.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nBin)

	svm = cv.ml.SVM_load(svm_xml)
	# svm = cv.ml.SVM_load('../object-detection/svmhead.xml')

	# _, result = svm.predict(np.array([hist]))
	# a, score = svm.predict(np.array([hist]), flags=cv.ml.STAT_MODEL_RAW_OUTPUT | cv.ml.STAT_MODEL_UPDATE_MODEL)

	for resized in pyramid(img, scaleFactor):
		scale = float(img.shape[1] / float(resized.shape[1]))
		# print('scale:',scale)
		for (x,y,roi) in sliding_window(resized, window_step, (w, h)):
			if roi.shape[0] < w or roi.shape[1] < h:
				continue
			rx, ry, rx2, ry2 = int(x * scale), int(y * scale), int((x + w) * scale), int((y + h) * scale)
			hist = hog.compute(roi,(5,5))[:,0]

			# 计算结果
			_, result = svm.predict(np.array([hist]))
			a, score = svm.predict(np.array([hist]), flags=cv.ml.STAT_MODEL_RAW_OUTPUT | cv.ml.STAT_MODEL_UPDATE_MODEL)
			
			# 过滤过大矩形
			# if (rx2 - rx > 39 or ry2 - ry > 39) and score[0][0] > -0.1:
			# 	continue
			if result[0][0] == 1 and score < -scoreThreshold:
				rectangles.append([rx, ry, rx2, ry2, abs(score[0][0])])
				# 存储检测的样本(到224帧，该225帧)
				# ro = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)
				# cv.imwrite('train/' + str(zhen) + str(order) + '.jpg', ro)
				# order += 1
				# print(rx,ry,rx2-rx,ry2-ry,':',-score[0][0])

	# 非最大抑制
	# print(len(rectangles))
	rectangles = non_max_suppression_fast(np.array(rectangles),0.1)
	return rectangles

if __name__ == '__main__':

	img = cv.imread('../static/TestImages/' + '2.JPG')
	# img = cv.resize(img,(518,960))
	rectangles = detect(img,scoreThreshold=scoreThreshold)
	print('人头数：',len(rectangles))
	for rect in rectangles:
		x,y,x2,y2,score = int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3]), rect[4]
		cv.putText(img, str(round(score,4)), (x, y), cv.FONT_HERSHEY_PLAIN, 1, (0xFF,0xFF,0xFF), 2)
		cv.rectangle(img,(x,y),(x2,y2),(0,0xFF,0),2)
		print(x,y,x2-x,y2-y,':',score)
	cv.putText(img,'counting:' + str(len(rectangles)),(0,15),cv.FONT_HERSHEY_PLAIN, 1.2, (0xFF,0xFF,0xFF), 2)
	cv.imshow('img001',img)
	# imgList = os.listdir('../TestImages')
	# for imgPath in imgList:
	# 	img = cv.imread('../TestImages/' + imgPath)
	# 	# img = cv.resize(img,(518,960))
	# 	rectangles = detect(img)
	# 	# print('人头数：',rectangles.shape[0])
	# 	for rect in rectangles:
	# 		x,y,x2,y2,score = rect
	# 		cv.rectangle(img,(x,y),(x2,y2),(0,255,0),2)
	# 		print(x,y,x2-x,y2-y,':',score)

	# 	cv.imshow(imgPath,img)
	cv.waitKey(0)