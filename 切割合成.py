
"""
    两张尺寸相同的图片根据某同一坐标值进行剪切并合并成同一张图片
    可用于京东登录验证拼图（两张缺口位置不一样，且不重叠的同一图片进行拼图，补全缺口）
"""
from PIL import Image
import sys


def main(filename_1, filename_2, filename_new, x=None, y=None):
    """
       两图合并为一张尺寸不发生变化的新图片
       :param filename_1: 取x值左边或y值上边的图片
       :param filename_2: 取x值右边或y值下边的图片
       :param x: 图片的横向色素坐标值
       :param y: 图片的纵向色素坐标值
       :return:  None
    """
    if Image.open(filename_1).size == Image.open(filename_2).size:
        if not x and not y or x and y:
            sys.exit("x,y不可同时为空/只允许一个有值")
        if x:
            try:
                size = Image.open(filename_1).size
                if x > size[0]:
                    sys.exit(f"x最大值为{size[0]},你输入的是x值为{x}")
                img_temp_1 = Image.open(filename_1).crop((0, 0, x, size[1]))
                img_temp_2 = Image.open(filename_2).crop((x, 0, size[0], size[1]))
                img = Image.new('RGB', size)
                img.paste(img_temp_1, (0, 0, x, size[1]))
                img.paste(img_temp_2, (x, 0, size[0], size[1]))
                img.save(filename_new)
            except Exception as e:
                sys.exit(e)
        if y:
            try:
                size = Image.open(filename_1).size
                if y > size[1]:
                    sys.exit(f"y最大值为{size[1]},你输入的是y值为{y}")
                img_temp_1 = Image.open(filename_1).crop((0, 0, size[0], y))
                img_temp_2 = Image.open(filename_2).crop((0, y, size[0], size[1]))
                img = Image.new('RGB', size)
                img.paste(img_temp_1, (0, 0, size[0], y))
                img.paste(img_temp_2, (0, y, size[0], size[1]))
                img.save(filename_new)
            except Exception as e:
                sys.exit(e)
    else:
        sys.exit("图片尺寸不一致")


if __name__ == '__main__':
    main('./image/5-1.png', './image/5-2.png', "./img/5.png", y=80)
    # main('./img/3-1.png','./image/3-2.png', "./img/3.png", x=138)


