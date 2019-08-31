#coding= utf-8
"""
功能：滑动窗口
输入：图像、步长、滑动窗大小
输出：图像窗口
"""
def sliding_window(image, step, window_size):
  for y in range(0, image.shape[0], step):
    for x in range(0, image.shape[1], step):
      yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])