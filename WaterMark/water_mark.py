# @Time : 2020/7/23 17:25
# @Author : Xuki
# @File : water_mark.py
# @Annotation : 
# coding:utf-8

from PIL import Image, ImageDraw, ImageFont
import argparse
import os


def add_text_to_image(image, text):
    font = ImageFont.truetype('simsun.ttc', 50)

    # 添加背景
    new_img = Image.new('RGBA', (image.size[0] * 3, image.size[1] * 3), (0, 0, 0, 0))
    new_img.paste(image, image.size)

    # 添加水印
    font_len = len(text)
    rgba_image = new_img.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (0, 0, 0, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    for i in range(0, rgba_image.size[0], font_len * 40 + 300):
        for j in range(0, rgba_image.size[1], 300):
            image_draw.text((i, j), text, font=font, fill=(255, 255, 255, 70))
    text_overlay = text_overlay.rotate(-45)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    # 裁切图片
    image_with_text = image_with_text.crop((image.size[0], image.size[1], image.size[0] * 2, image.size[1] * 2))
    return image_with_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='图片路径')
    parser.add_argument('txt', help='水印文字')
    args = parser.parse_args()
    _path = args.path
    _txt = args.txt
    if _path and _txt:
        _, image_name = os.path.split(_path)
        image_name_no_suffix, _ = os.path.splitext(image_name)
        img = Image.open(_path)
        im_after = add_text_to_image(img, _txt)
        im_after.save(f'{image_name_no_suffix}_water_mark.png')
    else:
        raise ValueError('必须输入图片路径和水印文字')

