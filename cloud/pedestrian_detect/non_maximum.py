#coding= utf-8
# import the necessary packages
import numpy as np

# Malisiewicz et al.
# Python port by Adrian Rosebrock
"""
功能：非极大抑制
输入：目标框、重合率
输出：最后目标框
"""
def non_max_suppression_fast(boxes, overlapThresh):
  # 如果目标框列表为空，返回空
  if len(boxes) == 0:
    return []

  # 如果目标框参数是整型，转换成浮点型
  # 这很重要，因为后面有一系列除法
  if boxes.dtype.kind == "i":
    boxes = boxes.astype("float")

  # 初始化筛选列表
  pick = []

  # 获得目标框坐标
  x1 = boxes[:,0]
  y1 = boxes[:,1]
  x2 = boxes[:,2]
  y2 = boxes[:,3]
  scores = boxes[:,4]
  # 计算所有目标框面积
  # 并将所有目标框按照score重新排列
  area = (x2 - x1 + 1) * (y2 - y1 + 1)
  idxs = np.argsort(scores)[::-1]

  # keep looping while some indexes still remain in the indexes
  # list
  while len(idxs) > 0:
    # 获得最大得分目标框索引，并放入筛选结果中
    last = len(idxs) - 1
    i = idxs[last]
    pick.append(i)

    # 获得得分最高目标框与其他目标框最大起始坐标和最小终止坐标
    xx1 = np.maximum(x1[i], x1[idxs[:last]])
    yy1 = np.maximum(y1[i], y1[idxs[:last]])
    xx2 = np.minimum(x2[i], x2[idxs[:last]])
    yy2 = np.minimum(y2[i], y2[idxs[:last]])

    # 计算最小目标框长、宽
    w = np.maximum(0, xx2 - xx1 + 1)
    h = np.maximum(0, yy2 - yy1 + 1)

    # 计算除得分最高外的所有目标框与最小目标框的重合度
    overlap = (w * h) / area[idxs[:last]]

    # 删除得分最高（已保存在筛选结果列表）、重合度大于阈值的目标框的索引
    idxs = np.delete(idxs, np.concatenate(([last],
      np.where(overlap > overlapThresh)[0])))

  # return only the bounding boxes that were picked using the
  # integer data type
  
  # print('pick: ',pick)

  return boxes[pick]