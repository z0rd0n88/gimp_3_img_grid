# Batch Collage Generator for GIMP 3.0

A Python-Fu script that arranges images from a folder into a grid collage inside GIMP 3.0.

## Features

- Loads all supported images from a specified folder
- Arranges them into a configurable grid layout
- Uniform scaling — each image is resized to the average dimensions of all inputs
- Configurable overlap between cells for a layered effect
- Optional limit on the number of images included
- Auto-calculates grid dimensions when columns is set to `0`
- Randomized image order
- Each layer is named with its index and original filename

## Requirements

- **GIMP 3.0** (uses the `gi.repository` GObject Introspection API)
- Python 3 (bundled with GIMP 3.0)

## Supported Image Formats

`jpg`, `jpeg`, `png`, `bmp`, `tiff`, `webp` (case-insensitive)

## Configuration

Edit the constants at the top of the script:

| Variable   | Default | Description                                                                  |
|------------|---------|------------------------------------------------------------------------------|
| `FOLDER`   | `./img` | Path to the folder containing your images                                    |
| `COLUMNS`  | `3`     | Number of columns in the grid. Set to `0` for an auto-calculated square grid |
| `OVERLAP`  | `0`     | Overlap ratio between cells. `0` = no overlap, `0.15` = 15% overlap         |
| `NUM_PICS` | `0`     | Max number of images to include. `0` = use all images in the folder          |

## Usage

1. Place your images in a folder (e.g., `./img`).
2. Open **GIMP 3.0**.
3. Go to **Filters > Python-Fu > Console**.
4. Run the script:
   ```python
   exec(open("/path/to/batch_collage_gimp_3.0.py").read())
   ```
5. A new image will open with all photos arranged in a grid.

## How It Works

1. **Collect** — Scans the target folder for all matching image files and deduplicates them.
2. **Select** — If `NUM_PICS > 0`, randomly samples that many images. Otherwise shuffles all images.
3. **Measure** — Opens each image temporarily to read its dimensions, then computes the average width and height. This becomes the uniform cell size.
4. **Layout** — Calculates the number of rows from the image count and column count. Canvas size is derived from cell size, grid dimensions, and overlap.
5. **Build** — Creates a new GIMP image, then for each input file:
   - Loads it as a layer
   - Scales it to the uniform cell size
   - Positions it at the correct grid offset
   - Names the layer `{index}_{filename}`
6. **Display** — Flushes the GIMP display so the result is visible.

## Grid Layout

```
 col 0      col 1      col 2
┌──────────┬──────────┬──────────┐
│  img 01  │  img 02  │  img 03  │  row 0
├──────────┼──────────┼──────────┤
│  img 04  │  img 05  │  img 06  │  row 1
├──────────┼──────────┼──────────┤
│  img 07  │  img 08  │  img 09  │  row 2
└──────────┴──────────┴──────────┘
```

With `OVERLAP > 0`, adjacent cells partially overlap. Later images (higher index) appear on top.

## Example

To create a 4-column collage with 10% overlap using at most 20 images:

```python
FOLDER   = "./my_photos"
COLUMNS  = 4
OVERLAP  = 0.10
NUM_PICS = 20
```

## Notes

- Images are scaled non-proportionally to fit the uniform cell size. For best results, use images with similar aspect ratios.
- The last row may have fewer images than the column count.
- Undo is disabled during generation for performance, then re-enabled after completion.
