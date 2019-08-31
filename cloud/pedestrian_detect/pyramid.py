#coding= utf-8
import cv2

"""
功能：缩放图像
输入：图片、尺度
输出：缩放后图像
"""
def resize(img, scaleFactor):
  return cv2.resize(img, (int(img.shape[1] * (1 / scaleFactor)), int(img.shape[0] * (1 / scaleFactor))), interpolation=cv2.INTER_AREA)

"""
功能：建立图像金字塔
输入：图片、尺度、最小尺寸
输出：图像金字塔
"""
def pyramid(image, scale=1.5, minSize=(20, 20)):
  yield image
  """
  yield 的作用就是把一个函数变成一个 generator，带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator，
  调用 pyramid() 不会执行 pyramid() 函数，而是返回一个 iterable 对象！在循环执行时，每次循环都会执行 pyramid 函数内部的代码，
  执行到 yield 时，pyramid() 函数就返回一个迭代值，下次迭代时，代码从 yield 的下一条语句继续执行，
  而函数的本地变量看起来和上次中断执行前是完全一样的，于是函数继续执行，直到再次遇到 yield。
  """
  while True:
    image = resize(image, scale)
    if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
      break

    yield image