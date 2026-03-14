import io
import textwrap
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from task_queue.src.constants import PREVIEW_SIZES, SUPPORTED_TEXT_PREVIEW_TYPES
from task_queue.src.processors.image_processor import preview_processing


def load_font(path_: str, size: int):
    try:
        return ImageFont.truetype(path_, size)
    except Exception:
        return ImageFont.load_default()


def create_image(tempfile: str) -> Optional[Image.Image]:
    """
    Create an image from a text file.
    """

    CHUNK_SIZE = 1024 * 1024 * 2  # 2MB

    BASE_WIDTH = 1080
    BASE_HEIGHT = 1920

    TAB_SIZE = 8

    FONT_PATH = "task_queue/public/Roboto-VariableFont_wdth,wght.ttf"
    FONT_SIZE = 28

    x = MARGINX = 48
    y = MARGINY = 76

    font = load_font(FONT_PATH, FONT_SIZE)

    ascending, descending = font.getmetrics()
    LINE_HEIGHT = ascending + descending
    LINE_SPACING = int(LINE_HEIGHT * 0.15)

    writable_width = int((BASE_WIDTH - (MARGINX * 2)) / font.getlength("a"))
    writable_height = BASE_HEIGHT - (MARGINY * 2)

    img = Image.new("RGB", (BASE_WIDTH, BASE_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    try:
        with open(tempfile, "r", encoding="utf-8", errors="replace") as f:
            line = ""
            while y <= writable_height:
                chunk = f.read(CHUNK_SIZE)
                if chunk == "":
                    break

                for char in chunk:
                    if y > writable_height:
                        break

                    if char == "\n":
                        wrapped_line = textwrap.wrap(line, width=writable_width)
                        draw.text(
                            (x, y),
                            "\n".join(wrapped_line),
                            fill="black",
                            font=font,
                        )

                        y += (LINE_HEIGHT + LINE_SPACING) * len(wrapped_line)

                        line = ""
                        continue
                    elif char == "\t":
                        line += " " * TAB_SIZE
                        continue

                    line += char

            if y <= writable_height and line:
                draw.text(
                    (x, y),
                    textwrap.fill(line, width=writable_width),
                    fill="black",
                    font=font,
                )

    except FileNotFoundError:
        return None

    return img


def text_processing(
    tempfile: str, content_type: str
) -> Optional[List[Tuple[PREVIEW_SIZES, io.BytesIO]]]:
    """Convert a text file into portrait preview images.

    Parameters:
    - tempfile: path to the temporary text file
    - content_type: original content-type of the file, used to check if the preview can be generated

    Returns a list of tuples ("large"|"medium"|"small", io.BytesIO).
    """

    if content_type not in SUPPORTED_TEXT_PREVIEW_TYPES:
        return None

    img = create_image(tempfile)

    if not img:
        return None

    previews = preview_processing(img, "image/jpg")
    return previews
