import torch
import torch.nn.functional as F
import torchvision.transforms.v2 as T
from PIL import Image, ImageOps
import os
import numpy as np

NAMESPACE = 'maga'


def get_name(name):
    return '{} ({})'.format(name, NAMESPACE)


def get_category(sub_dirs=None):
    if sub_dirs is None:
        return NAMESPACE
    else:
        return "{}/utils".format(NAMESPACE)


# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))


# Convert PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)