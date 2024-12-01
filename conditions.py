from .constants import get_category, get_name, pil2tensor
import os
from PIL import Image
import torch
import re
import node_helpers
import torchvision.transforms.functional as TF


class ConditionMultipleMaskArea:
    NAME = get_name("ConditionMultipleMaskArea")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip_1": ("CLIP", {}),
                "clip_2": ("CLIP", {}),
                "clip_3": ("CLIP", {}),

                "mask_1": ("MASK", {}),
                "area_text_1": ("STRING", {  "multiline": True }),
                "strength_1": ("FLOAT", { "default": 1, "min": -4.0, "max": 4.0, "step": 0.1 }),

                "mask_2": ("MASK", {}),
                "area_text_2": ("STRING", { "multiline": True }),
                "strength_2": ("FLOAT", { "default": 1, "min": -4.0, "max": 4.0, "step": 0.1 }),

                "mask_3": ("MASK", {}),
                "area_text_3": ("STRING", { "multiline": True }),
                "strength_3": ("FLOAT", { "default": 1, "min": -4.0, "max": 4.0, "step": 0.1 }),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("cond_1",)

    def execute(self, clip_1, clip_2, clip_3, mask_1, area_text_1, strength_1, mask_2, area_text_2, strength_2, mask_3, area_text_3, strength_3):
        final_cond = []

        # Mask 1
        if area_text_1 != "":
            output_1 = clip_1.encode_from_tokens(clip_1.tokenize(area_text_1), return_pooled=True, return_dict=True)
            cond_1 = output_1.pop("cond")
            conditioning_1 = [[cond_1, output_1]]
            final_cond += node_helpers.conditioning_set_values(conditioning_1, {"mask": mask_1,
                                                                    "set_area_to_bounds": False,
                                                                    "mask_strength": strength_1})

        # Mask 2
        if area_text_2 != "":
            output_2 = clip_2.encode_from_tokens(clip_2.tokenize(area_text_2), return_pooled=True, return_dict=True)
            cond_2 = output_2.pop("cond")
            conditioning_2 = [[cond_2, output_2]]
            final_cond += node_helpers.conditioning_set_values(conditioning_2, {"mask": mask_2,
                                                                       "set_area_to_bounds": False,
                                                                       "mask_strength": strength_2})

        # Mask 3
        if area_text_3 != "":
            output_3 = clip_3.encode_from_tokens(clip_3.tokenize(area_text_3), return_pooled=True, return_dict=True)
            cond_3 = output_3.pop("cond")
            conditioning_3 = [[cond_3, output_3]]
            final_cond += node_helpers.conditioning_set_values(conditioning_3, {"mask": mask_3,
                                                                       "set_area_to_bounds": False,
                                                                       "mask_strength": strength_3})

        return (final_cond,)



class ConditionMultipleGridArea:
    NAME = get_name("ConditionMultipleGridArea")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_clip": ("CLIP", {}),
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
                "strength": ("FLOAT", { "default": 1, "min": -4.0, "max": 4.0, "step": 0.1 }),
                "base_text": ("STRING", { "multiline": True }),
                "area_texts": ("STRING", { "multiline": True }),
                "text_delimiter": ("STRING", { "multiline": False }),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("cond",)

    def execute(self, base_clip, grid_x, grid_y, strength: float, base_text: str, area_texts: str, text_delimiter: str):
        final_cond = []

        item_w = 1 / grid_x
        item_h = 1 / grid_y
        x = 0
        y = 0

        area_tuples = area_texts.split(text_delimiter)
        print(area_tuples)

        for area_text in area_tuples:
            print(area_text)
            if area_text != "":
                output_1 = base_clip.encode_from_tokens(
                    base_clip.tokenize(area_text + ", " + base_text), return_pooled=True, return_dict=True
                )
                cond_1 = output_1.pop("cond")
                conditioning_1 = [[cond_1, output_1]]
                final_cond += node_helpers.conditioning_set_values(conditioning_1, {
                    "area": ("percentage", item_h, item_w, y, x),
                    "set_area_to_bounds": False,
                    "strength": strength,
                })
                print(("percentage", item_h, item_w, y, x))

                # Shift area
                x += item_w
                if x >= 1:
                    x = 0
                    y += item_h

        return (final_cond,)


"""
class ConditionMultipleGridMask:
    NAME = get_name("ConditionMultipleGridMask")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK", {}),
                "base_clip": ("CLIP", {}),
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
                "base_text": ("STRING", { "multiline": True }),
                "area_texts": ("STRING", { "multiline": True }),
                "text_delimiter": ("STRING", { "multiline": False }),
            },
        }

    RETURN_TYPES = ("CONDITIONING","MASK")
    RETURN_NAMES = ("cond","masks")

    def execute(self, mask, base_clip, grid_x, grid_y, base_text: str, area_texts: str, text_delimiter: str):
        final_cond = []
        masks = []

        _, H, W = mask.shape

        item_w = W // grid_x
        item_h = H // grid_y
        x = 0
        y = 0

        area_tuples = area_texts.split(text_delimiter)
        print(area_tuples)

        for area_text in area_tuples:
            print(area_text)
            if area_text != "":
                output_1 = base_clip.encode_from_tokens(
                    base_clip.tokenize(area_text + ", " + base_text), return_pooled=True, return_dict=True
                )
                cond_1 = output_1.pop("cond")
                conditioning_1 = [[cond_1, output_1]]

                x_end = x + item_w
                y_end = y + item_h
                submask = mask[:, y:y_end, x:x_end]
                print(x, y, x_end, y_end)

                new_mask = torch.zeros_like(mask)
                new_mask[:, y:y_end, x:x_end] = submask

                final_cond += node_helpers.conditioning_set_values(conditioning_1, {
                    "mask": new_mask,
                    "set_area_to_bounds": False,
                    "mask_strength": 1 / len(area_tuples)
                })

                masks.append(new_mask)

                # Shift area
                x += item_w
                if x >= W:
                    x = 0
                    y += item_h

        return (final_cond, torch.cat(masks, dim=0), )
"""