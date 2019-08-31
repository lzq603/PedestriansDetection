# -*- coding: utf-8 -*-
# @Author: lizhiqag@163.com
# @Date:   2019-04-18 19:16:23
# @Description   [ description ]
# @Last Modified time: 2019-05-28 20:03:44

import cv2 as cv
import numpy as np
import os
# from sklearn import svm, datasets

# hog 特征属性
winSize = (20,20)
blockSize = (10,10)
blockStride = (5,5)
cellSize = (5,5)
nBin = 9
hog = cv.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nBin)
C = 0.001

def svm_train(posPath,negPath,featureNum):

	# 数据准备
	posList = os.listdir(posPath)
	negList = os.listdir(negPath)
	PosNum = len(posList)		# 正样本数量
	NegNum = len(negList)		# 负样本数量

	featureNum = 324	# hog特征向量维数

	# 特征与标签
	featureArray = np.zeros((PosNum + NegNum, featureNum),np.float32)
	labelArray = np.zeros(PosNum + NegNum,np.int32)

	# HOGDescriptor

	# 将HOG特征、标签分别加入featureArray，labelArray数组

	for i in range(PosNum):
		img = cv.imread(posPath + '/' + posList[i])
		hist = hog.compute(img,(5,5))[:,0]
		featureArray[i] = hist
		# print(i)
		labelArray[i] = 1 # 正样本 label 1

	for j in range(NegNum):
		img = cv.imread(negPath + '/' + negList[j])
		hist = hog.compute(img,(5,5))[:,0]
		featureArray[j + PosNum] = hist
		# print(j)
		labelArray[j + PosNum] = -1 # 负样本 label -1

	# svm分类器，设置svm参数
	svm = cv.ml.SVM_create()
	svm.setType(cv.ml.SVM_C_SVC)
	svm.setKernel(cv.ml.SVM_LINEAR)
	svm.setC(C)

	print(featureArray.shape)
	print(labelArray.shape)

	# 训练
	# svm.train()
	svm.train(featureArray,cv.ml.ROW_SAMPLE,labelArray)
	# clf = svm.SVC(kernel='linear').fit(featureArray, labelArray)	#sklearn库的svm
	return svm

	# 保存训练结果
	# svm.save('svmhead_linear.xml')

# 进行测试
if __name__ == '__main__':
	svm = svm_train('../pos','../neg',324)
	svm.save('svm_head_linear_%f_temp.xml' % C)
	
	# svm = cv.ml.SVM_load('svm_head_linear_5.xml')
	# img = cv.imread('../object-detection/1.jpg')
	# hist = hog.compute(img,(5,5))[:,0]
	# print(hist.shape)

	# _, result = svm.predict(np.array([hist]))
	# a, score = svm.predict(np.array([hist]), flags=cv.ml.STAT_MODEL_RAW_OUTPUT | cv.ml.STAT_MODEL_UPDATE_MODEL)

	# print(result,score)