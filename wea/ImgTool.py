# -*- coding: utf-8 -*-
import os
import glob
import numpy as np

import cv2
import imageio
from PIL import Image


# PIL
def create_gif_with_PIL( gif_name, image_list, duration=0.5):
    images = []
    if image_list:
        im = Image.open(image_list[0])
        images.append(im)

        for image_name in image_list[1:]:
            images.append(Image.open(image_name))

        im.save(gif_name, save_all=True, append_images=images, duration=duration)


# imageio
def save_as_frame(file, target_dir):
    reader = imageio.get_reader(file)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    ct = 1
    for frame in reader:
        imageio.imwrite(os.path.join(target_dir, '{}.jpg'.format(ct)), frame)
        ct += 1


# imageio, PIL, Numpy
def create_gif(file, source_dir, fps, mode=None, size=None, size_selector=None, key=None):
    # 设置输出位置及源位置
    writer = imageio.get_writer(file, fps=fps)
    image_list = glob.glob(os.path.join(source_dir, '*'))

    if key:
        image_list.sort(key=key)

    for image_name in image_list:
        im = Image.open(image_name)

        # 选择器
        if size_selector:
            if im.size != size_selector:
                continue

        # 格式调整
        if mode and size:
            im_resize = im.convert(mode).resize(size, Image.BILINEAR)
        elif mode:
            im_resize = im.convert(mode)
        elif size:
            im_resize = im.resize(size, Image.BILINEAR)
        else:
            im_resize = im

        writer.append_data(np.array(im_resize))
    writer.close()


# cv2
def save_as_frame_with_cv2(file, target_dir):
    cap = cv2.VideoCapture(file)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    for i in range(10):
        print(cap.get(i))

    ct = 1
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(os.path.join(target_dir, '{}.jpg'.format(ct)), frame)
            ct += 1
        else:
            break

    print('frames:{}'.format(ct-1))
    cap.release()


# cv2
def create_gif_with_cv2(file, source_dir, fps, mode=None, size=None, size_selector=None, key=None):
    # 设置源位置
    image_list = glob.glob(os.path.join(source_dir, '*'))
    if key:
        image_list.sort(key=key)

    # 没有size就使用第一张图的size
    if not size:
        im = cv2.imread(image_list[0])
        size = (im.shape[1], im.shape[0])

    # 设置输出位置
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter(file, fourcc, fps, size)

    for image_name in image_list:
        im = cv2.imread(image_name)
        im = cv2.resize(im, size)
        out.write(im)
    out.release()


def convert_movie(source, target, mul=1):
    reader = imageio.get_reader(source)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(target, fps=fps)
    ct = 0

    for im in reader:
        if ct % mul == 0:
            writer.append_data(im)
        ct += 1
    writer.close()


if __name__ == '__main__':
    pass
