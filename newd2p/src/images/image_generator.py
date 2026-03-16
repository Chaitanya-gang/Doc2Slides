"""
newd2p - Simple Image Generator

Generates slide images from text prompts using Pillow.
Can be replaced with a heavier diffusion model if needed.
"""

from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from src.utils.logger import get_logger


logger = get_logger("image_generator")


def generate_image_from_prompt(prompt: str, output_path: str) -> Optional[str]:
    """
    Generate a simple image from a text prompt.

    This implementation uses Pillow to render the prompt text onto
    a colored background. It is intentionally lightweight so it can
    run without GPU or large diffusion models.
    """
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        width, height = 1280, 720
        background_color = (15, 23, 42)
        accent_color = (99, 102, 241)
        text_color = (226, 232, 240)

        img = Image.new("RGB", (width, height), color=background_color)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except Exception:
            font = ImageFont.load_default()

        title = "Visual"
        truncated = (prompt[:140] + "...") if len(prompt) > 140 else prompt

        draw.rectangle([(0, 0), (width, 90)], fill=accent_color)
        draw.text((40, 25), title, font=font, fill=(255, 255, 255))

        text_x, text_y = 80, 140
        max_width = width - 160
        words = truncated.split()
        line = ""
        lines = []

        for word in words:
            test_line = f"{line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            if text_width <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)

        for current_line in lines:
            draw.text((text_x, text_y), current_line, font=font, fill=text_color)
            text_y += 55

        img.save(output_path, format="PNG")
        logger.info(f"Generated slide image: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        return None
