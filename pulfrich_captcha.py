from PIL import Image, ImageDraw, ImageFont, ImageTransform
import numpy as np
import random
import cv2
import math
import time
import string

# Configuration settings
CONFIG = {
    "image_size": (450, 250),
    "pixel_density": 2,
    "font_size": 40,
    "video_duration": 2,
    "fps": 16,
    "code_length": (5, 7),
    "max_rotation": 10,
    "max_tilt": 0.4,
    "grayscale_range": (50, 200),
    "region_padding": 30,
    "scroll_speed": 1,
    "webp_quality": 60  # New quality parameter (0-100)
}

def generate_code():
    chars = string.ascii_uppercase + string.digits
    length = random.randint(*CONFIG["code_length"])
    return ''.join(random.choices(chars, k=length))

def create_captcha_video(code):
    w, h = [dim * CONFIG["pixel_density"] for dim in CONFIG["image_size"]]
    
    # Generate background and scroll parameters
    bg = np.random.randint(
        CONFIG["grayscale_range"][0],
        CONFIG["grayscale_range"][1] + 1,
        (h, w),
        dtype=np.uint8
    )
    
    # Random scroll parameters
    scroll_angle = random.uniform(0, 360)
    radians_angle = math.radians(scroll_angle)
    dx = CONFIG["scroll_speed"] * math.cos(radians_angle)
    dy = CONFIG["scroll_speed"] * math.sin(radians_angle)
    total_dx, total_dy = 0.0, 0.0

    # Create character mask
    mask = Image.new('L', (w, h), 0)
    font = ImageFont.truetype("arialbd.ttf", CONFIG["font_size"] * CONFIG["pixel_density"])

    # Calculate maximum character width
    max_char_width = max(font.getbbox(c)[2] - font.getbbox(c)[0] for c in code)
    
    # Region validation
    num_chars = len(code)
    region_width = w // num_chars
    available_width = region_width - 2 * CONFIG["region_padding"]
    assert available_width > max_char_width, \
        f"Characters too wide for regions ({max_char_width} > {available_width})"

    # Position characters in non-overlapping regions
    char_mask = np.zeros((h, w), dtype=bool)
    for i, c in enumerate(code):
        # Calculate safe region boundaries
        region_left = i * region_width + CONFIG["region_padding"]
        region_right = (i + 1) * region_width - CONFIG["region_padding"]
        
        # Get character dimensions
        bbox = font.getbbox(c)
        char_w = bbox[2] - bbox[0]
        char_h = bbox[3] - bbox[1]
        
        # Random position within safe area
        x = random.randint(region_left, region_right - char_w)
        y = random.randint(
            CONFIG["region_padding"],
            h - CONFIG["region_padding"] - char_h
        )
        
        # Apply random transformations
        rotation = random.uniform(-CONFIG["max_rotation"], CONFIG["max_rotation"])
        tilt = random.uniform(-CONFIG["max_tilt"], CONFIG["max_tilt"])
        
        # Draw character
        tmp = Image.new('L', (w, h), 0)
        tmp_draw = ImageDraw.Draw(tmp)
        tmp_draw.text(
            (x, y),
            c,
            fill=255,
            font=font,
            transform=ImageTransform.AffineTransform((1, tilt, 0, 0, 1, 0)),
            rotation=rotation
        )
        # Update character mask
        char_mask |= np.array(tmp) > 128

    # Video writer setup for WebM with quality parameter
    fourcc = cv2.VideoWriter_fourcc(*'VP90')
    out = cv2.VideoWriter(
        # CONFIG["output_file"],
        f"./captchas/{code}.webm",
        fourcc,
        CONFIG["fps"],
        (w, h),
        isColor=False
    )
    out.set(cv2.VIDEOWRITER_PROP_QUALITY, CONFIG["webp_quality"])  # Quality setting

    # Generate frames with scrolling background
    total_frames = CONFIG["fps"] * CONFIG["video_duration"]
    for _ in range(total_frames):
        total_dx += dx
        total_dy += dy
        shift_x = int(round(total_dx)) % w
        shift_y = int(round(total_dy)) % h
        
        # Apply background scroll
        scrolled_bg = np.roll(bg, (-shift_x, -shift_y), axis=(1, 0))
        
        # Generate flicker effect
        flicker = np.random.randint(
            CONFIG["grayscale_range"][0],
            CONFIG["grayscale_range"][1] + 1,
            size=(h, w)
        )
        
        # Combine background and flicker
        frame = np.where(char_mask, flicker, scrolled_bg)
        out.write(frame.astype(np.uint8))

    out.release()

if __name__ == "__main__":
    start_time = time.time()
    code = generate_code()
    print(f"CAPTCHA Code: {code}")
    try:
        create_captcha_video(code)
        print(f"Video saved as captchas/{code}.webm")
    except AssertionError as e:
        print(f"Error: {e}. Try increasing image width or reducing characters.")
    finally:
        end_time = time.time()
        print(f"Total time: {end_time - start_time:.2f} seconds")
