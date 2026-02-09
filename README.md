# PanImg Models

Data models for medical image processing and management.

## Overview

This module provides Pydantic dataclasses and enums for handling medical imaging data, including support for various image formats, metadata, and processing results.

## Core Components

### Enums

**ImageBuilderOptions**: Supported image builder formats
- MHD, NIFTI, NRRD, DICOM, TIFF, OCT, FALLBACK

**PostProcessorOptions**: Post-processing formats
- DZI (Deep Zoom Image)

**ColorSpace**: Image color spaces
- GRAY, RGB, RGBA, YCBCR

**ImageType**: Output image types
- MHD, TIFF, DZI

**EyeChoice**: Eye selection for ophthalmology images
- OD (Oculus Dexter - right eye)
- OS (Oculus Sinister - left eye)
- U (Unknown)
- NA (Not Applicable)

### Data Models

**PanImg**: Immutable image metadata
```python
PanImg(
    pk=uuid4(),
    name="scan.mhd",
    width=512,
    height=512,
    depth=100,
    voxel_width_mm=0.5,
    voxel_height_mm=0.5,
    voxel_depth_mm=1.0,
    color_space=ColorSpace.GRAY,
    eye_choice=EyeChoice.OD,
    segments=frozenset({1, 2, 3})
)
```

**PanImgFile**: Image file reference
```python
PanImgFile(
    image_id=uuid4(),
    image_type=ImageType.DZI,
    file=Path("/data/image.dzi"),
    directory=Path("/data/image_files")
)
```

**PanImgResult**: Image processing results
```python
PanImgResult(
    new_images={img1, img2},
    new_image_files={file1, file2},
    consumed_files={Path("/input/scan.mhd")},
    file_errors={Path("/bad.mhd"): ["Invalid header"]}
)
```

**PostProcessorResult**: Post-processing output
```python
PostProcessorResult(
    new_image_files={dzi_file}
)
```

## Constants

- `MAXIMUM_SEGMENTS_LENGTH = 64`: Max segments for int8/uint8 data
- `ITK_COLOR_SPACE_MAP`: Maps ITK channel counts to ColorSpace

## Testing

Run tests with pytest:
```bash
pytest test_module.py -v
```

## Requirements

- Python 3.10+
- pydantic
- pytest (for testing)
