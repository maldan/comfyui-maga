from .images import (ImagesToGrid, DirToImages, SelectImagesFromBatch, GridToImages,
                     ImagesToVideo, ImageRGBToMasks, ImageSaveWithFormat, OneImageToGrid)
from .videos import VideoToImages
from .strings import (StringRemoveTags, StringRemoveDuplicatedTags, CharacterDB,
                      EnvironmentDB, MultiCharacterDB, SplitStrings)
from .realesrgan import RealESRGANDenoise
from .conditions import ConditionMultipleMaskArea, ConditionMultipleGridArea

NODE_CLASS_MAPPINGS = {
    CharacterDB.NAME: CharacterDB,
    MultiCharacterDB.NAME: MultiCharacterDB,
    EnvironmentDB.NAME: EnvironmentDB,
    SplitStrings.NAME: SplitStrings,

    GridToImages.NAME: GridToImages,
    ImagesToVideo.NAME: ImagesToVideo,
    VideoToImages.NAME: VideoToImages,
    ImagesToGrid.NAME: ImagesToGrid,
    DirToImages.NAME: DirToImages,
    ImageSaveWithFormat.NAME: ImageSaveWithFormat,
    OneImageToGrid.NAME: OneImageToGrid,

    SelectImagesFromBatch.NAME: SelectImagesFromBatch,

    StringRemoveTags.NAME: StringRemoveTags,
    StringRemoveDuplicatedTags.NAME: StringRemoveDuplicatedTags,

    RealESRGANDenoise.NAME: RealESRGANDenoise,

    ConditionMultipleMaskArea.NAME: ConditionMultipleMaskArea,
    ConditionMultipleGridArea.NAME: ConditionMultipleGridArea,
    # ConditionMultipleGridMask.NAME: ConditionMultipleGridMask,

    ImageRGBToMasks.NAME: ImageRGBToMasks,
}

