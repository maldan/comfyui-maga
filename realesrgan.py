from .constants import get_category, get_name, pil2tensor, tensor2pil
import os
from PIL import Image
import torch
import tempfile
import subprocess
from comfy.utils import ProgressBar


class RealESRGANDenoise:
    NAME = get_name("RealESRGANDenoise")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {}),
                "scale": (["x1", "x2", "x4"],)
            },
        }

    RETURN_TYPES = ("IMAGE",)

    def execute(self, images, scale):
        # Получаем путь к папке, где находится файл
        current_directory = os.path.dirname(os.path.abspath(__file__))

        exe_path = current_directory + "/realesrgan/realesrgan-ncnn-vulkan.exe"

        final_images = []

        print(exe_path)

        B, _, _, _ = images.shape
        pbar = ProgressBar(B)

        # Создаем временную директорию
        with tempfile.TemporaryDirectory() as temp_folder:
            print("Temporary folder created:", temp_folder)
            for i, image in enumerate(images):
                img = tensor2pil(image)
                img_path = os.path.join(temp_folder, f"{i}.png")
                img_path_upscale = os.path.join(temp_folder, f"{i}_up.png")
                img.save(img_path)

                # Команда для запуска
                command = [
                    exe_path,
                    "-i", img_path,
                    "-o", img_path_upscale,
                    "-n", "realesrgan-x4plus-anime"
                ]

                # Запуск команды через subprocess
                subprocess.run(command, check=True)

                img = Image.open(img_path_upscale)

                if scale == "x1":
                    img = img.resize((img.width // 4, img.height // 4), resample=Image.BILINEAR)
                if scale == "x2":
                    img = img.resize((img.width // 2, img.height // 2), resample=Image.BILINEAR)

                final_images.append(pil2tensor(img))

                pbar.update(1)

        batched_images = torch.cat(final_images, dim=0)

        return (batched_images,)
