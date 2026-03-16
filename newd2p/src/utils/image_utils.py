"""
newd2p - Image Processing Helpers
"""

from PIL import Image
import io


def resize_image(image_bytes: bytes, max_width: int = 800, max_height: int = 600) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img.save(output, format=img.format or "PNG")
    return output.getvalue()


def get_image_dimensions(image_bytes: bytes) -> tuple:
    img = Image.open(io.BytesIO(image_bytes))
    return img.size
