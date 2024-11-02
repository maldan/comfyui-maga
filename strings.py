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

    dictas = {
        'none': [],

        'daki': [
            'kimetsu no yaiba', 'daki',
            'white hair', 'tattoo',
            'white skin', 'gray nipples',
            'medium breasts',
            'veins', 'hairpins'
        ],
        'sylvia': [
            'konosuba', 'sylvia',
            'dark skin', 'huge breasts',
            'long penis', 'futanari', 'dark nipples'
        ],
        'flare corona': [
            'fairy tail', 'flare corona',
            'red long hair', 'twin braids',
            'large breasts', 'thin waist', 'wide hips',
        ],
        'zangya': [
            'dragon ball z', 'zangya',
            'green blue skin', 'long orange hair',
            'dark blue nipples', 'large breasts',
            'abs', 'athletic body'
        ],
        'carrot': [
            'one piece', 'carrot',
            'furry', 'bunny ears',
            'funny furry'
        ],
        'squigly': [
            'skullgirls', 'squigly', 'zombie',
            'red eyes', 'blue skin', 'blue hair', 'eyeshadows', 'sewed mouth', 'purple nipples',
        ],
        'ashido mina': [
            'boku no hero academia', 'ashido mina',
            'medium breasts', 'pink skin', 'black sclera', 'yellow eyes'
        ],
        'morrigan aensland': [
            'darkstalkers', 'morrigan aensland', 'large breasts'
        ],
        'kefla': [
            'dragon ball z', 'kefla', 'athletic body', 'abs', 'large breasts'
        ],
        'raven': [
            'teen titans', 'raven dc', 'gray skin', 'purple nipples'
        ],
        'sakuya izayoi': [
            'touhou', 'sakuya izayoi', 'maid', 'white hair'
        ],
        'giselle gewelle': [
            'bleach', 'giselle gewelle',
            'futanari', 'long black hair', 'small breasts', 'long penis'
        ],
        'efanatika': [
            'aku no onna kanbu', 'efanatika', 'dark elf',
            'elf ears',
            'long pink hair', 'blue skin', 'huge breasts',
            'blue nipples', 'black sclera', 'yellow eyes',
            'thin waist', 'thick thighs'
        ],
        'miruko': [
            'boku no hero academia', 'miruko', 'dark skin',
            'bunny ears', 'tan skin', 'athletic body',
            'red eyes', 'white long hair'
        ],
        'tsunade': [
            'naruto shippuuden', 'tsunade',
            'blonde hair', 'large breasts'
        ],
        'kiryuuin satsuki': [
            'kill la kill', 'kiryuuin satsuki',
            'long black hair', 'thick eyebrows', 'blue eyes'
        ],
        'mount lady': [
            'boku no hero academia',
            'mount lady', 'mask', 'horns'
        ],
        'bulma': [
            'dragon ball z', 'bulma', 'long blue hair',
            'large breasts', 'blue eyes'
        ],
        'tatsumaki': [
            'one punch man', 'tatsumaki',
            'small breasts', 'wide thick legs',
            'short green hair', 'green eyes'
        ],
        'fubuki': [
            'one punch man', 'fubuki',
            'large breasts', 'short dark green hair',
            'thin waist', 'long legs', 'wide hips'
        ],
        'matoi ryuuko': [
            'kill la kill', 'matoi ryuuko',
            'short black hair', 'blue eyes'
        ],
        'lust': [
            'fullmetal alchemist', 'lust', 'female',
            'black hair', 'red eyes', 'hair with curls',
            'long black nails', 'tattoo'
        ],
        'asui tsuyu': [
            'boku no hero academia', 'asui tsuyu',
            'saggy breasts', 'slim', 'moles',
            'round eyes', 'long black hair',
            'long tongue'
        ],
        'shihouin yoruichi': [
            'bleach', 'shihouin yoruichi',
            'dark skin', 'dark nipples',
            'dark magenta hair with braid',
            'athletic body'
        ],
        'tier harribel': [
            'bleach', 'tier harribel',
            '1girl', 'big breasts',
            'short blonde hair', 'blonde eyelash', 'blonde brows',
            'thin waist',
            'dark skin', 'dark nipples'
        ],
        'juri han': [
            'street fighter', 'juri han',
            'abs', 'athletic body', 'braids'
        ],
        'aishi san': [
            'koutetsu no majo annerose', 'aishi san',
            'dark skin', 'purple hairs',
            'large breasts', 'purple lips', 'long hairs', 'earrings'
        ],
        'frieren': [
            'sousou no frieren', 'frieren',
            'elf girl', 'red earrings',
            'green eyes', 'elf ears',
            'thick eyebrows', 'small eyes',
            'small chest', 'slim'
        ],
        'android 21': [
            'dragon ball z', 'majin android 21', 'pink skin', 'white hair',
            'black sclera', 'red eyes'
        ],
        'cheelai': [
            'dragon ball z', 'cheelai',
            'green skin', 'green nipples', 'short white hair',
        ],
        'power': ['chainsaw man', 'power', 'long orange hair'],
        'yamato': ['one piece', 'yamato', 'huge breasts', 'tall'],
        'rebecca': ['cyberpunk edgerunners', 'rebecca', 'blue nipples'],
        'yor briar': ['spy x family', 'yor briar', 'large breasts'],
        '2b': ['nier automata', 'yorha no. 2 type b', 'large breast', 'thin waist', 'wide hips', 'long legs'],
        'tohru kobayashi': ['maidragon', 'tohru kobayashi', 'large breasts', 'horns'],
        'videl': ['dragon ball z', 'videl', 'black hair', 'braids'],
    }

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "name": (list(self.dictas.keys()),),
                "is_nude": ("BOOLEAN",),
            },
        }

    def execute(self, name, is_nude):
        if self.dictas.get(name, '') != '':
            tags = self.dictas[name]

            if not is_nude:
                input_remove = [x.strip() for x in [".*nipple.*", ".*penis.*", ".*futanari.*", ".*balls.*"]]

                tags = [
                    tag for tag in tags
                    if not any(re.fullmatch(pattern, tag) for pattern in input_remove)
                ]

            return (", ".join(tags),)

        return ("",)


class EnvironmentDB:
    NAME = get_name("EnvironmentDB")
    CATEGORY = get_category()
    FUNCTION = "execute"
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("Location", "Light")

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
            },
        }

    def execute(self, location, light):
        location_tags = []
        light_tags = []

        if self.locations.get(location, '') != '':
            location_tags = self.locations[location]

        if self.lights.get(light, '') != '':
            light_tags = self.lights[light]

        return (", ".join(location_tags), ", ".join(light_tags),)
