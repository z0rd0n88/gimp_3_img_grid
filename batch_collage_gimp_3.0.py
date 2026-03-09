import os
import glob
import math
import random
import gi

# Require GIMP 3.0 API
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, Gio

# ── Configuration ──────────────────────────────────────────────
FOLDER   = "./img"  # image folder path
COLUMNS  = 3    # grid columns, 0 = auto square grid
OVERLAP  = 0    # cell overlap ratio, e.g. 0.15 = 15%
NUM_PICS = 0    # max images to include, 0 = all
# ───────────────────────────────────────────────────────────────

SUPPORTED_EXTENSIONS = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff", "*.webp")


def collect_image_paths(folder, extensions):
    """Collect unique image paths from folder for all supported extensions."""
    paths = set()
    for pattern in extensions:
        paths.update(glob.glob(os.path.join(folder, pattern)))
        paths.update(glob.glob(os.path.join(folder, pattern.upper())))
    return list(paths)


def get_image_size(path):
    """Load an image temporarily to read its dimensions, then discard it."""
    gfile = Gio.File.new_for_path(path)
    temp_img = Gimp.file_load(Gimp.RunMode.NONINTERACTIVE, gfile)
    try:
        return temp_img.get_width(), temp_img.get_height()
    finally:
        temp_img.delete()


def build_collage(paths, columns, overlap):
    """Create a GIMP image with all provided images arranged in a grid."""
    count = len(paths)
    rows = math.ceil(count / columns)

    # Compute uniform cell size from the average dimensions
    print(f"Measuring {count} images...")
    sizes = [get_image_size(p) for p in paths]
    cell_w = sum(w for w, _ in sizes) // count
    cell_h = sum(h for _, h in sizes) // count

    step_x = int(cell_w * (1 - overlap))
    step_y = int(cell_h * (1 - overlap))

    canvas_w = step_x * (columns - 1) + cell_w
    canvas_h = step_y * (rows - 1) + cell_h

    # Create canvas and display
    image = Gimp.Image.new(canvas_w, canvas_h, Gimp.ImageBaseType.RGB)
    display = Gimp.Display.new(image)
    image.undo_disable()

    for idx, path in enumerate(paths):
        col = idx % columns
        row = idx // columns

        gfile = Gio.File.new_for_path(path)
        layer = Gimp.file_load_layer(Gimp.RunMode.NONINTERACTIVE, image, gfile)

        image.insert_layer(layer, None, -1)
        layer.scale(cell_w, cell_h, False)
        layer.set_offsets(col * step_x, row * step_y)

        name = os.path.splitext(os.path.basename(path))[0]
        layer.set_name(f"{idx + 1:02d}_{name}")

        if (idx + 1) % 10 == 0 or idx + 1 == count:
            print(f"  Placed {idx + 1}/{count}")

    image.undo_enable()
    Gimp.displays_flush()

    return image, columns, rows


def main():
    print("Starting collage generation...")

    # Collect and deduplicate paths
    paths = collect_image_paths(FOLDER, SUPPORTED_EXTENSIONS)

    if not paths:
        raise FileNotFoundError(f"No images found in: {FOLDER}")

    # Limit to NUM_PICS random images if configured
    if 0 < NUM_PICS < len(paths):
        paths = random.sample(paths, NUM_PICS)
    else:
        random.shuffle(paths)

    # Auto-calculate columns for a roughly square grid
    columns = COLUMNS if COLUMNS > 0 else math.ceil(math.sqrt(len(paths)))

    image, cols, rows = build_collage(paths, columns, OVERLAP)
    print(f"Done! {len(paths)} images in {cols}x{rows} grid")


main()
