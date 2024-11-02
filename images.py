from .constants import get_category, get_name, pil2tensor
import os
from PIL import Image
import torch
from comfy.utils import ProgressBar


class DirToImages:
    NAME = get_name("DirToImages")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_dir": ("STRING", {
                    "multiline": False,
                    "default": "C:/",
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)

    def get_images(self, folder_path):
        # Список допустимых расширений для изображений
        image_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"}

        # Получаем список всех файлов в папке
        all_files = os.listdir(folder_path)

        # Фильтруем файлы, оставляя только изображения, и возвращаем полные пути
        return [os.path.join(folder_path, f) for f in all_files if os.path.splitext(f)[1].lower() in image_extensions]

    def execute(self, image_dir):
        image_list = [pil2tensor(Image.open(x)) for x in self.get_images(image_dir)]
        batched_images = torch.cat(image_list, dim=0)

        return (batched_images,)


"""
class DirToGrid:
    NAME = get_name("DirToGrid")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_dir": ("STRING", {
                    "multiline": False,
                    "default": "C:/",
                }),

                "offset": ("INT", {
                    "default": 1,
                    "min": 0,
                    "max": 4096,
                    "step": 1,
                    "display": "number",
                }),
                "grid_x": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 6,
                    "step": 1,
                    "display": "number",
                }),
                "grid_y": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 6,
                    "step": 1,
                    "display": "number",
                }),
                "scale": ("FLOAT", {
                    "default": 1, "min": 0.0, "max": 4.0, "step": 0.1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)

    def create_image_grid(self, image_paths, grid_size, offset=0, scale=1.0):
        # Применяем offset и length к списку изображений
        length = grid_size[0] * grid_size[1]
        # Применяем offset и length к списку изображений
        if offset >= len(image_paths):
            image_paths = []  # Если offset выходит за пределы списка, возвращаем пустой список
        else:
            image_paths = image_paths[offset:offset + length] if length else image_paths[offset:]

        if len(image_paths) == 0:
            return Image.new('RGB', (128, 128))

        images = [Image.open(img) for img in image_paths]

        # Определяем количество строк (n) и колонок (m)
        m, n = grid_size

        # Предполагаем, что все изображения одинакового размера
        img_width, img_height = images[0].size

        # Масштабируем размеры каждого изображения
        scaled_width = int(img_width * scale)
        scaled_height = int(img_height * scale)

        # Итоговые размеры для нового изображения (grid)
        grid_width = m * scaled_width
        grid_height = n * scaled_height

        # Создаем новое изображение для сетки
        grid_image = Image.new('RGB', (grid_width, grid_height))

        # Вставляем каждое изображение в нужную позицию с учётом масштаба
        for idx, image in enumerate(images):
            row = idx // m
            col = idx % m

            # Масштабируем изображение
            resized_image = image.resize((scaled_width, scaled_height))

            # Вставляем изображение в сетку
            grid_image.paste(resized_image, (col * scaled_width, row * scaled_height))

        return grid_image

    def get_images(self, folder_path):
        # Список допустимых расширений для изображений
        image_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"}

        # Получаем список всех файлов в папке
        all_files = os.listdir(folder_path)

        # Фильтруем файлы, оставляя только изображения, и возвращаем полные пути
        return [os.path.join(folder_path, f) for f in all_files if os.path.splitext(f)[1].lower() in image_extensions]

    def execute(self, image_dir, offset, grid_x, grid_y, scale):
        image_list = self.get_images(image_dir)
        final_image = self.create_image_grid(image_list[0:len(image_dir)], (grid_x, grid_y), offset, scale)

        return (pil2tensor(final_image),)
"""


class ImagesToGrid:
    NAME = get_name("ImagesToGrid")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {}),
                "grid_x": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 8,
                    "step": 1,
                    "display": "number",
                }),
                "grid_y": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 8,
                    "step": 1,
                    "display": "number",
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)

    def execute(self, images, grid_x, grid_y):
        # Извлекаем размеры входных изображений
        B, H, W, C = images.shape  # Входной формат: (B, H, W, C)

        # Рассчитываем размеры итогового изображения в сетке
        grid_height = grid_y * H
        grid_width = grid_x * W

        # Создаем пустое изображение для всей сетки с черным фоном
        grid_image = torch.zeros((grid_height, grid_width, C), dtype=images.dtype)

        # Заполняем сетку изображениями
        for idx in range(B):
            row = idx // grid_x
            col = idx % grid_x

            # Проверяем, чтобы не выйти за границы сетки
            if row < grid_y:
                top = row * H
                left = col * W
                # Вставляем кадр в нужное место сетки
                grid_image[top:top + H, left:left + W, :] = images[idx]

        # Добавляем размерность batch, чтобы вернуть (1, H', W', C)
        return (grid_image.unsqueeze(0),)  # Формат: (1, grid_y * H, grid_x * W, C)


class SelectImagesFromBatch:
    NAME = get_name("SelectImagesFromBatch")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {}),
                "numbers": ("STRING", {

                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)

    def execute(self, images, numbers: str):
        numbers = [int(x.strip()) for x in numbers.split(",")]
        final = []

        for i, index in enumerate(numbers):
            final.append(images[index-1].unsqueeze(0))

        batched_images = torch.cat(final, dim=0)

        print(batched_images.shape)

        return (batched_images,)