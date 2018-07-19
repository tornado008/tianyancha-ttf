# coding=utf-8

from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont
import os

# 将ttf字体转换成图片
def chismiocr(fontpath):
    chinese_dir = 'chis'
    if not os.path.exists(chinese_dir):
        os.mkdir(chinese_dir)

    # 获取ttf的编码范围
    font = TTFont(fontpath)
    cmap = font['cmap']
    cmap_dict = cmap.getBestCmap()
    cmap_list = list(cmap_dict.keys())
    chis = []
    for codepoint in cmap_list:
        word = chr(codepoint)
        chis.append(word)
        im = Image.new("RGB", (150, 150), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(fontpath, 72)
        dr.text((50, 50), word, font=font, fill="#000000")
        dr.getfont()
        # 图片保存路径
        im.save(os.path.join(chinese_dir, word + ".png"))

    print(chis)

# 将所有被替换字体合成一张图片
def merge():
    path = os.path.join('chis')
    image_paths = [Image.open(path + '/' + fn) for fn in os.listdir(path)]

    w, h = image_paths[0].size

    merge_ims = Image.new(image_paths[0].mode, (w, h*len(image_paths)))

    for i, im in enumerate(image_paths):
        merge_ims.paste(im, box=(0, i *h))

    merge_ims.save('merge.png')

if __name__=='__main__':
    chismiocr('./tyc-num.ttf')
    merge()