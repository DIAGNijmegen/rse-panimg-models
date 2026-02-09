from dataclasses import FrozenInstanceError
from pathlib import Path
from uuid import uuid4

import pytest

from panimg_models import (
    ITK_COLOR_SPACE_MAP,
    MAXIMUM_SEGMENTS_LENGTH,
    ColorSpace,
    EyeChoice,
    ImageBuilderOptions,
    ImageType,
    PanImg,
    PanImgFile,
    PanImgResult,
    PostProcessorOptions,
    PostProcessorResult,
)


class TestEnums:
    def test_image_builder_options_values(self):
        assert ImageBuilderOptions.MHD == "MHD"
        assert ImageBuilderOptions.DICOM == "DICOM"
        assert len(ImageBuilderOptions) == 7

    def test_post_processor_options(self):
        assert PostProcessorOptions.DZI == "DZI"

    def test_color_space_values(self):
        assert ColorSpace.GRAY == "GRAY"
        assert ColorSpace.RGB == "RGB"
        assert ColorSpace.RGBA == "RGBA"

    def test_image_type_values(self):
        assert ImageType.MHD == "MHD"
        assert ImageType.TIFF == "TIFF"

    def test_eye_choice_values(self):
        assert EyeChoice.OCULUS_DEXTER == "OD"
        assert EyeChoice.OCULUS_SINISTER == "OS"


class TestConstants:
    def test_maximum_segments_length(self):
        assert MAXIMUM_SEGMENTS_LENGTH == 64

    def test_itk_color_space_map(self):
        assert ITK_COLOR_SPACE_MAP[1] == ColorSpace.GRAY
        assert ITK_COLOR_SPACE_MAP[3] == ColorSpace.RGB
        assert ITK_COLOR_SPACE_MAP[4] == ColorSpace.RGBA


class TestPanImg:
    def test_creation_minimal(self):
        pk = uuid4()
        img = PanImg(
            pk=pk,
            name="test.mhd",
            width=512,
            height=512,
            depth=None,
            voxel_width_mm=None,
            voxel_height_mm=None,
            voxel_depth_mm=None,
            timepoints=None,
            resolution_levels=None,
            window_center=None,
            window_width=None,
            color_space=ColorSpace.GRAY,
            eye_choice=EyeChoice.NOT_APPLICABLE,
        )
        assert img.pk == pk
        assert img.name == "test.mhd"
        assert img.segments is None

    def test_creation_with_segments(self):
        img = PanImg(
            pk=uuid4(),
            name="test.mhd",
            width=512,
            height=512,
            depth=100,
            voxel_width_mm=1.0,
            voxel_height_mm=1.0,
            voxel_depth_mm=1.0,
            timepoints=1,
            resolution_levels=5,
            window_center=128.0,
            window_width=256.0,
            color_space=ColorSpace.RGB,
            eye_choice=EyeChoice.OCULUS_DEXTER,
            segments=frozenset({1, 2, 3}),
        )
        assert img.segments == frozenset({1, 2, 3})

    def test_frozen_dataclass(self):
        img = PanImg(
            pk=uuid4(),
            name="test",
            width=100,
            height=100,
            depth=None,
            voxel_width_mm=None,
            voxel_height_mm=None,
            voxel_depth_mm=None,
            timepoints=None,
            resolution_levels=None,
            window_center=None,
            window_width=None,
            color_space=ColorSpace.GRAY,
            eye_choice=EyeChoice.UNKNOWN,
        )
        with pytest.raises(FrozenInstanceError):
            img.width = 200


class TestPanImgFile:
    def test_creation(self):
        img_id = uuid4()
        file_path = Path("/tmp/test.mhd")
        img_file = PanImgFile(
            image_id=img_id,
            image_type=ImageType.MHD,
            file=file_path,
        )
        assert img_file.image_id == img_id
        assert img_file.file == file_path
        assert img_file.directory is None

    def test_with_directory(self):
        img_file = PanImgFile(
            image_id=uuid4(),
            image_type=ImageType.DZI,
            file=Path("/tmp/image.dzi"),
            directory=Path("/tmp/image_files"),
        )
        assert img_file.directory == Path("/tmp/image_files")


class TestPanImgResult:
    def test_creation_empty(self):
        result = PanImgResult(
            new_images=set(),
            new_image_files=set(),
            consumed_files=set(),
            file_errors={},
        )
        assert len(result.new_images) == 0
        assert len(result.file_errors) == 0

    def test_creation_with_data(self):
        img = PanImg(
            pk=uuid4(),
            name="test",
            width=100,
            height=100,
            depth=None,
            voxel_width_mm=None,
            voxel_height_mm=None,
            voxel_depth_mm=None,
            timepoints=None,
            resolution_levels=None,
            window_center=None,
            window_width=None,
            color_space=ColorSpace.GRAY,
            eye_choice=EyeChoice.UNKNOWN,
        )
        result = PanImgResult(
            new_images={img},
            new_image_files=set(),
            consumed_files={Path("/tmp/test.mhd")},
            file_errors={Path("/tmp/bad.mhd"): ["Parse error"]},
        )
        assert len(result.new_images) == 1
        assert len(result.consumed_files) == 1
        assert Path("/tmp/bad.mhd") in result.file_errors


class TestPostProcessorResult:
    def test_creation(self):
        result = PostProcessorResult(new_image_files=set())
        assert len(result.new_image_files) == 0

    def test_with_files(self):
        img_file = PanImgFile(
            image_id=uuid4(),
            image_type=ImageType.DZI,
            file=Path("/tmp/out.dzi"),
        )
        result = PostProcessorResult(new_image_files={img_file})
        assert len(result.new_image_files) == 1
