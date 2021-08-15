import torch
from .network import FINED
import os
import numpy as np
from PIL import Image
import cv2
from PIL import Image
import gc

# CONFIG
weight_file = os.getcwd() + "/app/modules/fined/weights/final-model.pth"

def get_FINED_edge(im,fname):
    ## Multiscale
    scales = [0.5,1.0,1.5]
    images = []
    for scl in scales:
        img_scale = cv2.resize(im, None, fx=scl, fy=scl, interpolation=cv2.INTER_LINEAR)
        images.append(img_scale.transpose(2, 0, 1)) # (H x W x C) to (C x H x W)

    # CREATE MODEL
    model = FINED(pretrain=weight_file, isTrain=False)
    model.cuda()
    model.eval()

    ## FEED FORWARD
    h, w, _ = im.shape
    ms_fuse = np.zeros((h, w))
    retn = None

    with torch.no_grad():
        for img in images:
            img = img[np.newaxis, :, :, :]
            img = torch.from_numpy(img)
            img = img.cuda()
            img = img.float()
            out = model(img)
            fuse = out[-1].squeeze().detach().cpu().numpy()
            fuse = cv2.resize(fuse, (w, h), interpolation=cv2.INTER_LINEAR)
            ms_fuse += fuse
            del img
            del out
            torch.cuda.empty_cache()
        ms_fuse /= len(scales)
        retn = 255 - (ms_fuse * 255).astype(np.uint8)
    model._clear_params(torch.device('cpu'))
    del model
    gc.collect()
    torch.cuda.empty_cache()
    
    return retn


