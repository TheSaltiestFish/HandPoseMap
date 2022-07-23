import argparse
import os
import sys
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn

from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync

WEIGHTS_PATH = "./best1.pt"
DATA_PATH = "./data/datasets/hand_pose.yaml"
IMAGE_SIZE = (640, 640)

class Handpose:
    def __init__(self, weights_path, data_path, imgsz):

        # 自动选择设备 模型加载
        self.device = select_device('')
        self.model = DetectMultiBackend(weights_path, device=self.device, dnn=False, data=data_path, fp16=False)
        self.imgsz = check_img_size(imgsz, s=self.model.stride)
        self.stride = self.model.stride
        self.pt = self.model.pt
        self.names = self.model.names

    def detectFromImage(self, path, callback):
        # 读取图片
        dataset = LoadImages(path, img_size=self.imgsz, stride=self.stride, auto=self.pt)
        bs = 1

        self.model.warmup(imgsz=(1 if self.pt else bs, 3, *(self.imgsz)))

        for path, im, im0s, vid_cap, s in dataset:
            im = torch.from_numpy(im).to(self.device)
            im = im.half() if self.model.fp16 else im.float() / 255
            im = im[None]  # expand for batch dim

            pred = self.model(im, augment=False, visualize=False)
            # 非极大值抑制
            pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

            # 每帧处理
            for i, det in enumerate(pred):
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

                if len(det):
                    # 图像缩放
                    det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)  # 识别类别

                        xyxy = torch.tensor(xyxy).view(-1, 4)
                        rect = xyxy2xywh(xyxy)

                        crop = im0[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::1]

                        callback(self.names[c], round(conf.item(), 2), rect.tolist()[0], crop)

    def detectFromCamera(self, callback):

        # imshow可运行检测 加速推理 读取摄像流
        view_img = check_imshow()
        cudnn.benchmark = True
        dataset = LoadStreams('0', img_size=self.imgsz, stride=self.stride, auto=self.pt)
        self.model.warmup(imgsz=(1 if self.pt else bs, 3, *(self.imgsz)))

        for path, im, im0s, vid_cap, s in dataset:
            im = torch.from_numpy(im).to(self.device)
            im = im.half() if self.model.fp16 else im.float() / 255

            pred = self.model(im, augment=False, visualize=False)
            # 非极大值抑制
            pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

            # 每帧处理
            for i, det in enumerate(pred):
                p, im0, frame = path[i], im0s[i].copy(), dataset.count

                if len(det):
                    # 图像缩放
                    det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)  # 识别类别

                        xyxy = torch.tensor(xyxy).view(-1, 4)
                        rect = xyxy2xywh(xyxy)

                        crop = im0[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::1]

                        callback(self.names[c], round(conf.item(), 2), rect.tolist()[0], crop)

def handle(result, conf, rect, img):
    print(result, end=' ')
    print(conf, end=' ')
    print(rect)

    cv2.imshow("result", img)
    cv2.waitKey(1)

def main():
    hd = Handpose(WEIGHTS_PATH, DATA_PATH, IMAGE_SIZE)
    hd.detectFromCamera(handle)
    # hd.detectFromImage("C:/Users/Administrator.LAPTOP-JR38EVVS/Desktop/test.jpg", handle)

if __name__ == "__main__":
    main()