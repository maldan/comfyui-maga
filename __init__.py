from maga.example import Example, GridToImages, ImagesToVideo
from maga.images import ImagesToGrid, DirToImages, SelectImagesFromBatch
from maga.video_to_images import VideoToImages
from maga.string_nodes import StringRemoveTags, StringRemoveDuplicatedTags, CharacterDB

from maga.realesrgan import RealESRGANDenoise

NODE_CLASS_MAPPINGS = {
    Example.NAME: Example,
    CharacterDB.NAME: CharacterDB,

    GridToImages.NAME: GridToImages,
    ImagesToVideo.NAME: ImagesToVideo,
    VideoToImages.NAME: VideoToImages,
    ImagesToGrid.NAME: ImagesToGrid,
    DirToImages.NAME: DirToImages,

    SelectImagesFromBatch.NAME: SelectImagesFromBatch,

    StringRemoveTags.NAME: StringRemoveTags,
    StringRemoveDuplicatedTags.NAME: StringRemoveDuplicatedTags,

    RealESRGANDenoise.NAME: RealESRGANDenoise,
}

