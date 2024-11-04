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
