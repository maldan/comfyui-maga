import json

from .constants import get_category, get_name, pil2tensor
import os
from PIL import Image
import torch
import re


class StringRemoveDuplicatedTags:
    NAME = get_name("StringRemoveDuplicatedTags")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "tags": ("STRING", {

                }),
            },
        }

    RETURN_TYPES = ("STRING",)

    def execute(self, tags):
        mylist = [x.strip() for x in tags.split(",")]
        unique = [x for i, x in enumerate(mylist) if i == mylist.index(x)]
        unique = [x for x in unique if x.strip() != ""]
        return (", ".join(unique),)


class StringRemoveTags:
    NAME = get_name("StringRemoveTags")
    CATEGORY = get_category()
    FUNCTION = "execute"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "tags": ("STRING", {

                }),
                "remove": ("STRING", {
                    "multiline": True,
                }),
            },
        }

    RETURN_TYPES = ("STRING",)

    def execute(self, tags, remove):
        input_tags = [x.strip() for x in tags.split(",")]
        input_remove = [x.strip() for x in remove.split(",")]

        filtered = [
            tag for tag in input_tags
            if not any(re.fullmatch(pattern, tag) for pattern in input_remove)
        ]
        filtered = [x for x in filtered if x.strip() != ""]

        return (", ".join(filtered),)


class CharacterDB:
    NAME = get_name("Character DB")
    CATEGORY = get_category()
    FUNCTION = "execute"
    RETURN_TYPES = ("STRING",)

    def __init__(self):
        pass

    # Get characters json file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_path = current_directory + "/characters.json"
    dictas = {}
    with open(json_path, "r") as f:
        dictas = json.load(f)
    dictas['none'] = {}

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "name": (sorted(list(self.dictas.keys())),),
                "is_nude": ("BOOLEAN",),
                "additional": ("STRING", {
                    "multiline": True,
                })
            },
        }

    def execute(self, name, is_nude, additional: str):
        if self.dictas.get(name, '') != '':
            local_tags = []
            local_tags += self.dictas[name]['source'].copy()
            local_tags.append(name)
            local_tags += self.dictas[name]['base'].copy()

            if is_nude and self.dictas[name].get('nude') != None:
                local_tags += self.dictas[name]['nude'].copy()

            local_tags += [x.strip() for x in additional.split(",")]

            return (", ".join(local_tags),)

            """tags = self.dictas[name].copy()

            tags += [x.strip() for x in additional.split(",")]

            if not is_nude:
                input_remove = [x.strip() for x in [".*nipple.*", ".*penis.*", ".*futanari.*", ".*balls.*"]]

                tags = [
                    tag for tag in tags
                    if not any(re.fullmatch(pattern, tag) for pattern in input_remove)
                ]

            return (", ".join(tags),)"""

        return ("",)


class MultiCharacterDB:
    NAME = get_name("Multi Character DB")
    CATEGORY = get_category()
    FUNCTION = "execute"
    RETURN_TYPES = (
        "STRING","STRING","STRING",
        "STRING","STRING","STRING",
        "STRING","STRING","STRING",
    )

    def __init__(self):
        pass

    # Get characters json file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_path = current_directory + "/characters.json"
    dictas = {}
    with open(json_path, "r") as f:
        dictas = json.load(f)
    dictas['none'] = {}

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "preview": (sorted(list(self.dictas.keys())),),
                "names": ("STRING", {
                    "multiline": True,
                }),

                "is_nude": ("BOOLEAN",),

                "join_into_one": ("BOOLEAN",),
                "delimeter": ("STRING",),

                "additional": ("STRING", {
                    "multiline": True,
                })
            },
        }

    def execute(self, preview: str, names: str, is_nude: bool, join_into_one: bool, delimeter: str, additional: str):
        names = [x.strip() for x in names.split(',')]

        tags = []

        for name in names:
            if self.dictas.get(name, '') != '':
                local_tags = []
                local_tags += self.dictas[name]['source'].copy()
                local_tags.append(name)
                local_tags += self.dictas[name]['base'].copy()

                if is_nude and self.dictas[name].get('nude') != None:
                    local_tags += self.dictas[name]['nude'].copy()

                local_tags += [x.strip() for x in additional.split(",")]
                tags += [", ".join(local_tags)]

        print(tags)
        if join_into_one:
            return (delimeter.join(tags),)

        return tuple(tags)


class SplitStrings:
    NAME = get_name("Split Strings")
    CATEGORY = get_category()
    FUNCTION = "execute"
    RETURN_TYPES = (
        "STRING","STRING",
    )
    RETURN_NAMES = ("", "selected")

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                }),
                "delimeter": ("STRING",),
                "index": ("INT",)
            },
        }

    def execute(self, text: str, delimeter: str, index: int):
        tt = text.split(delimeter)
        return (tt[index],)


class EnvironmentDB:
    NAME = get_name("EnvironmentDB")
    CATEGORY = get_category()
    FUNCTION = "execute"
    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("location", "light", "quality")

    def __init__(self):
        pass

    locations = {
        'none': [],
        'bedroom': ["bedroom", "bed", "window"],
        'bathroom': ['bathroom', 'blue tails', 'mirror', 'bathtub', 'glass door', 'steam', 'wet', 'sweat'],
        'japanese bathhouse': ['japanese bathhouse', 'wooden vat', 'wooden bathtub', 'bamboo'],
        'japanese forest': ['japanese forest', 'wooden lanterns'],
        'onsen': ['onsen', 'hot water', 'steam', 'sweat', 'wet', 'stones', 'reflections on water'],
        'beach': ['beach', 'ocean', 'palms', 'wind', 'waves', 'sand'],
        'large royal room': ['large royal room', 'golden details', 'rich furniture'],
        'black': ['black background'],
        'meadown': ['meadow', 'grass', 'flowers', 'wind', 'clouds', 'the grass shimmers in the wind', 'leaves'],
        'rain forest': ['vibrant rainforest', 'bioluminescent fungi', 'rain', 'fog', 'wet', 'glowing mushrooms'],
        'laboratory': ['laboratory', 'flasks', 'test tubes', 'tables']
    }

    lights = {
        'none': [],
        'moonlight': ["moonlight", "cinematic", "rim light", "deep night"],
        'daytime': ["daytime", "cinematic", "rim light", "sunlight"],
        'early morning': ['cinematic', 'rim light', 'early morning', 'god rays'],

        'loop lighting': ['loop lighting', 'broad lighting', 'rembrandt lighting'],
        'chiaroscuro': ['chiaroscuro', 'noir', 'dimly lit'],

        'god rays': ['crepuscular rays', 'god rays', 'light shimmering', 'iridescent lighting', 'luminescent effects']
    }



    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "location": (list(self.locations.keys()),),
                "light": (list(self.lights.keys()),),
                "quality": (["none", "low", "good", "epic"],),
            },
        }

    def execute(self, location, light, quality):
        location_tags = []
        light_tags = []
        quality_tags = []

        if self.locations.get(location, '') != '':
            location_tags = self.locations[location]

        if self.lights.get(light, '') != '':
            light_tags = self.lights[light]

        if quality == "low":
            quality_tags = ["score_4", "score_5", "source anime"]
        if quality == "good":
            quality_tags = ["score_7", "score_8", "source anime", "good quality", "hires"]
        if quality == "epic":
            quality_tags = ["score_8", "score_9", "source anime", "best quality", "hires", "masterpiece", "talented artist", "high detailed"]

        return (", ".join(location_tags), ", ".join(light_tags), ", ".join(quality_tags),)
