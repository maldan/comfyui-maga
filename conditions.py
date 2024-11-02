from .constants import get_category, get_name, pil2tensor
import os
from PIL import Image
import torch
import re
import node_helpers


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
                "image": ("IMAGE", {}),
                "clip": ("CLIP", {}),

                "area_text_1": ("STRING", {  "multiline": True }),
                "strength_1": ("FLOAT", { "default": 1, "min": -4.0, "max": 4.0, "step": 0.1 }),

                "area_text_2": ("STRING", { "multiline": True }),
                "strength_2": ("FLOAT", { "default": 1, "min": -4.0, "max": 4.0, "step": 0.1 }),

                "area_text_3": ("STRING", { "multiline": True }),
                "strength_3": ("FLOAT", { "default": 1, "min": -4.0, "max": 4.0, "step": 0.1 }),
            },
        }

    RETURN_TYPES = ("CONDITIONING","MASK","MASK","MASK")
    RETURN_NAMES = ("cond_1","mask1","mask2","mask3")

    def execute(self, image, clip, area_text_1, strength_1, area_text_2, strength_2, area_text_3, strength_3):
        B, H, W, C = image.shape  # (B, H, W, C)
        final_cond = []

        mask_1 = torch.zeros((W, H), dtype=torch.float32, device="cpu")
        mask_2 = torch.zeros((W, H), dtype=torch.float32, device="cpu")
        mask_3 = torch.zeros((W, H), dtype=torch.float32, device="cpu")

        # Mask 1
        if area_text_1 != "":
            mask_1 = (image[:, :, :, 0] > 0.9).float()
            mask_1 = mask_1.permute(0, 1, 2)
            output_1 = clip.encode_from_tokens(clip.tokenize(area_text_1), return_pooled=True, return_dict=True)
            cond_1 = output_1.pop("cond")
            conditioning_1 = [[cond_1, output_1]]
            final_cond += node_helpers.conditioning_set_values(conditioning_1, {"mask": mask_1,
                                                                    "set_area_to_bounds": False,
                                                                    "mask_strength": strength_1})

        # Mask 2
        if area_text_2 != "":
            mask_2 = (image[:, :, :, 1] > 0.9).float()
            mask_2 = mask_2.permute(0, 1, 2)
            output_2 = clip.encode_from_tokens(clip.tokenize(area_text_2), return_pooled=True, return_dict=True)
            cond_2 = output_2.pop("cond")
            conditioning_2 = [[cond_2, output_2]]
            final_cond += node_helpers.conditioning_set_values(conditioning_2, {"mask": mask_2,
                                                                       "set_area_to_bounds": False,
                                                                       "mask_strength": strength_2})

        # Mask 3
        if area_text_3 != "":
            mask_3 = (image[:, :, :, 2] > 0.9).float()
            mask_3 = mask_3.permute(0, 1, 2)
            output_3 = clip.encode_from_tokens(clip.tokenize(area_text_3), return_pooled=True, return_dict=True)
            cond_3 = output_3.pop("cond")
            conditioning_3 = [[cond_3, output_3]]
            final_cond += node_helpers.conditioning_set_values(conditioning_3, {"mask": mask_3,
                                                                       "set_area_to_bounds": False,
                                                                       "mask_strength": strength_3})

        return (final_cond, mask_1, mask_2, mask_3)
