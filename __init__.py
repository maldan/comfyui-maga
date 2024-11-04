from .images import ImagesToGrid, DirToImages, SelectImagesFromBatch, GridToImages, ImagesToVideo, ImageRGBToMasks
from .videos import VideoToImages
from .strings import StringRemoveTags, StringRemoveDuplicatedTags, CharacterDB, EnvironmentDB
from .realesrgan import RealESRGANDenoise
from .conditions import ConditionMultipleMaskArea

NODE_CLASS_MAPPINGS = {
    CharacterDB.NAME: CharacterDB,
    EnvironmentDB.NAME: EnvironmentDB,

    GridToImages.NAME: GridToImages,
    ImagesToVideo.NAME: ImagesToVideo,
    VideoToImages.NAME: VideoToImages,
    ImagesToGrid.NAME: ImagesToGrid,
    DirToImages.NAME: DirToImages,

    SelectImagesFromBatch.NAME: SelectImagesFromBatch,

    StringRemoveTags.NAME: StringRemoveTags,
    StringRemoveDuplicatedTags.NAME: StringRemoveDuplicatedTags,

    RealESRGANDenoise.NAME: RealESRGANDenoise,

    ConditionMultipleMaskArea.NAME: ConditionMultipleMaskArea,
    ImageRGBToMasks.NAME: ImageRGBToMasks,
}

