# coding=utf-8

from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont
import pytesseract
import os

# 中文ORC识别(使用 ttf文件提高中文识别成功率)
def numttf(fontpath):
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    numbers_list = {'一':'1', '二':'2', '三':'3', '四':'4', '五':'5', '六':'6', '七':'7', '八':'8', '九':'9', '零':'0'}
    chinese_dir = 'numfont'
    if not os.path.exists(chinese_dir):
        os.mkdir(chinese_dir)

    # 获取ttf的编码范围
    font = TTFont(fontpath)
    cmap = font['cmap']
    cmap_dict = cmap.getBestCmap()
    cmap_list = list(cmap_dict.keys())
    num = {}
    for codepoint in cmap_list:
        word = chr(codepoint)
        if word in numbers:

            im = Image.new("RGB", (150, 150), (255, 255, 255))
            dr = ImageDraw.Draw(im)
            font = ImageFont.truetype(fontpath, 72)
            dr.text((50, 50), word, font=font, fill="#000000")
            dr.getfont()
            # 图片保存路径
            im.save(os.path.join(chinese_dir, word + ".png"))

            fontimage = Image.open(os.path.join(chinese_dir, word + ".png"))
            # psm模式
            chinesechar = pytesseract.image_to_string(fontimage, lang='chi_sim', config="-psm 6")
            if chinesechar != "":
                try:
                    if numbers_list[chinesechar]:
                        chinesechar = numbers_list[chinesechar]
                except:
                    pass
                num[word] = chinesechar
    print(num)

if __name__=='__main__':
    numttf('./tyc-num.ttf')
