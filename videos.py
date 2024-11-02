from .constants import get_category, get_name, pil2tensor, tensor2pil
import os
from PIL import Image
import torch
import tempfile
import subprocess
import numpy as np
from comfy.utils import ProgressBar


class VideoToImages:
    NAME = get_name("VideoToImages")
    CATEGORY = get_category()
    FUNCTION = "execute"
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE",)

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_path": ("STRING", {
                    "multiline": False,
                    "default": "C:/",
                }),
                "start_time": ("STRING", {
                    "multiline": False,
                }),
                "end_time": ("STRING", {
                    "multiline": False,
                }),
                "skip_every_n_frame": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 8,
                    "step": 1,
                    "display": "number",
                }),
                "scale_by": ("FLOAT", {
                    "default": 1,
                    "min": 0.1,
                    "max": 4,
                    "step": 0.1,
                    "display": "number",
                }),
            },
        }

    def execute(self, video_path, start_time, end_time, skip_every_n_frame, scale_by):
        # Создаем временную директорию
        with tempfile.TemporaryDirectory() as temp_folder:
            print("Temporary folder created:", temp_folder)

            # Команда FFmpeg для извлечения кадров из видео
            frame_pattern = os.path.join(temp_folder, "frame_%05d.png")
            command = ["ffmpeg", "-i", video_path]

            if start_time != "":
                command.append("-ss")
                command.append(start_time)

            if end_time != "":
                command.append("-to")
                command.append(end_time)

            command += [
                "-vf", f"scale=iw*{scale_by}:ih*{scale_by}",
                frame_pattern,                  # Шаблон имени для сохранения кадров
                "-q:v", "0"                     # Качество кадров (0 — наилучшее качество, 2 — хорошее качество)
            ]
            subprocess.run(command, check=True)

            # Считываем кадры и конвертируем в тензоры (H, W, C)
            frame_tensors = []
            files = sorted(os.listdir(temp_folder))

            pbar = ProgressBar(len(files))

            for i, filename in enumerate(files):
                if filename.endswith(".png") and (i % skip_every_n_frame == 0):  # Добавляем проверку на шаг
                    frame_path = os.path.join(temp_folder, filename)
                    image = Image.open(frame_path).convert("RGB")
                    image_tensor = pil2tensor(image)
                    frame_tensors.append(image_tensor)

                pbar.update(1)

            batched_images = torch.cat(frame_tensors, dim=0)

            # Собираем все кадры в один тензор (B, H, W, C)
            print("Video tensor shape:", batched_images.shape)

        return (batched_images, )
