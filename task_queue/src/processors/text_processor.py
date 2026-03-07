import io
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from task_queue.src.constants import PREVIEW_SIZES, SUPPORTED_TEXT_PREVIEW_TYPES
from task_queue.src.processors.image_processor import preview_processing


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

    CHUNK_SIZE = 1024 * 1024 * 2

    BASE_WIDTH = 1080
    BASE_HEIGHT = 1920
    MARGINY = 48
    MARGINX = 48
    FONT_NAME = "task_queue/public/Roboto-VariableFont_wdth,wght.ttf"
    FONT_SIZE = 28

    def load_font(size: int):
        try:
            return ImageFont.truetype(FONT_NAME, size)
        except Exception:
            return ImageFont.load_default()

    def render_with_font(size: int) -> Optional[io.BytesIO]:
        font = load_font(size)
        img = Image.new("RGB", (BASE_WIDTH, BASE_HEIGHT), "white")
        draw = ImageDraw.Draw(img)

        line_height = font.getlength("A")
        line_spacing = int(line_height * 0.7)

        writable_width = BASE_WIDTH - MARGINX * 2
        writable_height = BASE_HEIGHT - MARGINY * 2

        x = MARGINX
        y = MARGINY

        try:
            with open(tempfile, "r", encoding="utf-8", errors="replace") as f:
                line = ""
                while y <= writable_height:
                    chunk = f.read(CHUNK_SIZE)
                    if chunk == "":
                        break

                    words = chunk.split(" ")

                    for word in words:
                        for letter in word:
                            if letter == "\n":
                                if line:
                                    draw.text((x, y), line, fill="black", font=font)
                                y += line_height + line_spacing
                                line = ""
                                continue

                            w = draw.textlength(line + letter, font=font)
                            if w > writable_width:
                                draw.text((x, y), line, fill="black", font=font)
                                y += line_height + line_spacing
                                line = ""

                            if y > writable_height:
                                break

                            line += letter
                        line += " "

                if line:
                    draw.text((x, y), line, fill="black", font=font)

        except Exception as r:
            return None

        return img

    rendered = render_with_font(FONT_SIZE)
    if not rendered:
        return None

    previews = preview_processing(rendered, "image/jpg")
    return previews
