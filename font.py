# coding=utf-8

from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont
import os

from qcloud_image import Client, CIFile

# numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x']
numbers = ['x']

column = 10


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

    return chis


# 将所有被替换字体合成一张图片
def merge(ttf):
    path = os.path.join('chis')
    image_paths = []
    for fn in ttf:
        if fn not in numbers:
            image_paths.append(Image.open(path + '/' + fn + '.png'))

    w, h = image_paths[0].size
    #横向+纵向合并图片 column决定每行多少列
    merge_ims = Image.new(image_paths[0].mode, (w * column, h * (int(len(image_paths) / column) + 1)))

    for i in range(len(image_paths)):
        merge_ims.paste(image_paths[i], box=((i % column) * w, int(i / column) * h))

    merge_ims.save('merge.png')


def qcloud_general(ttf):
    #控制台-访问管理-云API秘钥管理-新建或获取现有
    appid = 'your appid'
    secret_id = 'your secret_id'
    secret_key = 'your secret_key'
    #对象存储
    bucket = 'your bucket'

    client = Client(appid, secret_id, secret_key, bucket)
    client.use_http()
    client.set_timeout(30)
    # 通用印刷体识别
    ocr = client.general_detect(CIFile('./merge.png'))

    ocr_list = []
    if ocr['code'] == 0:
        if len(ocr['data']['items']) > 0:
            for i, item in enumerate(ocr['data']['items']):
                for word in item['words']:
                    if word['character'] != '':
                        ocr_list.append(word['character'])
                    if word['character'] == '':
                        print('第%d行,字符串"%s"中有空字符' % (i, item['itemstring']))

        ocr_ttf = {}
        for n in numbers:
            if n in ttf:
                ttf.remove(n)
        for i, t in enumerate(ttf):
            if i < len(ocr_list):
                print('%s --> %s' % (t , ocr_list[i]))
                ocr_ttf[t] = ocr_list[i]
            else:
                print('%s 没有被匹配' % t)
        print(ocr_ttf)

    else:
        print('ocr识别结果有误，错误码: %d' % ocr['code'])


if __name__ == '__main__':
    ttf = chismiocr('./tyc-num.ttf')
    if len(ttf) > 0:
        merge(ttf)
        qcloud_general(ttf)
